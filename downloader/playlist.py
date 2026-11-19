"""
@file playlist.py
@brief Playlist-Erkennung, Auslesen der Einträge und paralleler Download.

Statt eine Playlist Video für Video nacheinander zu laden, wird sie
zuerst "flach" ausgelesen (nur IDs + Titel, sehr schnell) und dann mit
mehreren Threads gleichzeitig heruntergeladen. Die Nummerierung folgt
der Position in der YouTube-Playlist.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Callable
from urllib.parse import parse_qs, urlparse

from yt_dlp import YoutubeDL

## Anzahl gleichzeitiger Video-Downloads bei Playlists.
MAX_WORKERS = 4


@dataclass(frozen=True)
class PlaylistEntry:
    """
    @brief Ein Video einer Playlist.
    """

    index: int  ##< Position in der YouTube-Playlist (1-basiert)
    url: str    ##< URL oder ID des Videos
    title: str  ##< Originaltitel (nur für Statusausgaben)


@dataclass
class DownloadReport:
    """
    @brief Ergebnis eines Downloads: welche Videos geklappt haben und welche nicht.
    """

    succeeded: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """
        @return True, wenn mindestens ein Video und keines fehlerhaft geladen wurde.
        """
        return bool(self.succeeded) and not self.failed


def has_playlist(url: str) -> bool:
    """
    @brief Prüft, ob die URL eine Playlist referenziert (Parameter ``list``).
    @param url YouTube-URL.
    @return True bei Playlist-Bezug.
    """
    return bool(parse_qs(urlparse(url).query).get("list"))


def has_video(url: str) -> bool:
    """
    @brief Prüft, ob die URL auf ein konkretes Video zeigt.

    Erkannt werden ``watch?v=``, ``youtu.be/<id>`` sowie ``/shorts/`` und ``/live/``.

    @param url YouTube-URL.
    @return True, wenn ein einzelnes Video adressiert wird.
    """
    parsed = urlparse(url)
    if parse_qs(parsed.query).get("v"):
        return True
    host = (parsed.hostname or "").lower()
    if host.endswith("youtu.be"):
        return bool(parsed.path.strip("/"))
    return parsed.path.startswith(("/shorts/", "/live/"))


def fetch_entries(url: str) -> list[PlaylistEntry]:
    """
    @brief Liest die Videos einer Playlist aus, ohne sie herunterzuladen.
    @param url Playlist-URL (auch ``watch?v=...&list=...``).
    @return Einträge in YouTube-Reihenfolge; nicht verfügbare Videos fehlen.
    """
    opts = {
        "extract_flat": "in_playlist",
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if not info:
        return []

    entries = []
    for position, entry in enumerate(info.get("entries") or [], start=1):
        if not entry:
            continue
        video_url = entry.get("url") or entry.get("id")
        if video_url:
            entries.append(PlaylistEntry(position, video_url, entry.get("title") or video_url))
    return entries


def download_parallel(
    entries: list[PlaylistEntry],
    worker: Callable[[PlaylistEntry, int], bool],
    max_workers: int = MAX_WORKERS,
) -> DownloadReport:
    """
    @brief Lädt alle Einträge gleichzeitig mit einem Thread-Pool herunter.
    @param entries Zu ladende Playlist-Einträge.
    @param worker Lädt einen Eintrag; erhält (Eintrag, Ziffernbreite) und
           liefert True bei Erfolg.
    @param max_workers Maximale Anzahl gleichzeitiger Downloads.
    @return Bericht mit erfolgreichen und fehlgeschlagenen Videos (nach Position sortiert).
    """
    width = max(2, len(str(max((e.index for e in entries), default=0))))
    results: list[tuple[PlaylistEntry, bool]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(worker, entry, width): entry for entry in entries}
        for done, future in enumerate(as_completed(futures), start=1):
            entry = futures[future]
            try:
                ok = bool(future.result())
            except Exception:  # ein kaputtes Video darf den Rest nicht stoppen
                ok = False
            results.append((entry, ok))
            mark = "OK  " if ok else "FAIL"
            print(f"[{done}/{len(entries)}] {mark} {entry.title}")

    report = DownloadReport()
    for entry, ok in sorted(results, key=lambda r: r[0].index):
        label = f"{entry.index:0{width}d} - {entry.title}"
        (report.succeeded if ok else report.failed).append(label)
    return report
