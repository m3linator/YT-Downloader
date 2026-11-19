"""
@file core.py
@brief Gemeinsame Download-Steuerung für mp3 und mp4.

Entscheidet zwischen Einzelvideo und ganzer Playlist und liefert immer
einen ehrlichen DownloadReport zurück.
"""

from __future__ import annotations

from typing import Callable

from yt_dlp import YoutubeDL

from .playlist import MAX_WORKERS, DownloadReport, PlaylistEntry, download_parallel, fetch_entries
from .utils import CleanTitlePP, build_outtmpl

## Baut aus einer Dateinamen-Vorlage die vollständigen yt-dlp Optionen.
OptionsFactory = Callable[[str], dict]


def download_one(url: str, opts: dict, *, keep_features: bool) -> bool:
    """
    @brief Lädt genau eine URL mit den gegebenen Optionen herunter.
    @param url Video-URL.
    @param opts yt-dlp Optionen.
    @param keep_features "(feat. ...)" im Dateinamen behalten.
    @return True, wenn yt-dlp ohne Fehler fertig wurde.
    """
    with YoutubeDL(opts) as ydl:
        # Titel VOR der Dateinamenserzeugung säubern.
        ydl.add_post_processor(CleanTitlePP(keep_features=keep_features), when="pre_process")
        # Rückgabewert 0 = Erfolg; bei ignoreerrors werden Fehler hier sichtbar.
        return ydl.download([url]) == 0


def download(
    url: str,
    options_factory: OptionsFactory,
    *,
    keep_features: bool,
    whole_playlist: bool,
) -> DownloadReport:
    """
    @brief Lädt ein Einzelvideo oder eine komplette Playlist herunter.
    @param url YouTube-URL.
    @param options_factory Liefert die Format-spezifischen Optionen (mp3/mp4).
    @param keep_features "(feat. ...)" im Dateinamen behalten.
    @param whole_playlist True = alle Videos der Playlist parallel laden,
           False = nur das Video aus dem Link.
    @return Bericht über erfolgreiche und fehlgeschlagene Downloads.
    """
    if not whole_playlist:
        opts = options_factory(build_outtmpl())
        opts["noplaylist"] = True
        if download_one(url, opts, keep_features=keep_features):
            return DownloadReport(succeeded=[url])
        return DownloadReport(failed=[url])

    print("Lese Playlist aus ...")
    entries = fetch_entries(url)
    if not entries:
        return DownloadReport(failed=[url])
    print(f"{len(entries)} Videos gefunden – lade bis zu {MAX_WORKERS} gleichzeitig.\n")

    def worker(entry: PlaylistEntry, width: int) -> bool:
        opts = options_factory(build_outtmpl(entry.index, width))
        # Parallele Fortschrittsbalken würden sich überlagern; Fehler
        # gibt yt-dlp trotzdem aus, den Status meldet download_parallel.
        opts.update(quiet=True, no_warnings=True, noprogress=True, noplaylist=True)
        return download_one(entry.url, opts, keep_features=keep_features)

    return download_parallel(entries, worker)
