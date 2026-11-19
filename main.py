#!/usr/bin/env python3
"""
YT-Downloader Einstiegspunkt.

Fragt nach Format (mp3 / mp4) und URL (Einzelvideo oder Playlist) und
delegiert den Download an die passende Funktion. Heruntergeladen wird
in den Standard-Downloads-Ordner des Benutzers.

Das Programm läuft "bare metal" mit dem System-Python. Fehlt ``yt-dlp``,
wird eine klare Installationsanweisung ausgegeben.
"""

from __future__ import annotations

import sys
from typing import Callable


def _ensure_yt_dlp() -> None:
    """
    @brief Bricht mit einer Installationsanweisung ab, falls yt-dlp fehlt.
    """
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        sys.stderr.write(
            "Fehler: 'yt-dlp' ist nicht installiert.\n"
            "Installiere es mit:\n"
            '  python3 -m pip install -U "yt-dlp[default]"\n'
        )
        sys.exit(1)


_ensure_yt_dlp()

# Diese Imports laden yt_dlp – erst nach _ensure_yt_dlp() ausführbar.
from downloader.mp3_downloader import mp3_downloader  # noqa: E402
from downloader.mp4_downloader import vid_download    # noqa: E402
from downloader.playlist import DownloadReport, has_playlist, has_video  # noqa: E402


AUDIO_KEYWORDS = {"mp3", "sound", "audio", "stimme"}
VIDEO_KEYWORDS = {"mp4", "video", "film"}


def ask_whole_playlist(url: str, ask: Callable[[str], str] = input) -> bool:
    """
    @brief Klärt, ob eine ganze Playlist oder nur das Video aus dem Link geladen wird.

    * Reiner Playlist-Link (``playlist?list=``) -> ganze Playlist, keine Frage.
    * Video innerhalb einer Playlist (``watch?v=...&list=``) -> Nachfrage;
      Standard ist nur das Video aus dem Link.
    * Einzelvideo -> nur dieses Video.

    @param url YouTube-URL.
    @param ask Eingabefunktion (für Tests austauschbar).
    @return True, wenn die ganze Playlist geladen werden soll.
    """
    if not has_playlist(url):
        return False
    if not has_video(url):
        return True
    answer = ask(
        "\nDer Link gehört zu einer Playlist.\n"
        "  [1] Nur dieses Video (Standard)\n"
        "  [2] Ganze Playlist\n"
        "Auswahl: "
    )
    return answer.strip() == "2"


def print_report(report: DownloadReport) -> int:
    """
    @brief Gibt das Ergebnis ehrlich aus.
    @param report Ergebnis des Downloads.
    @return Exit-Code: 0 bei Erfolg, sonst 1.
    """
    total = len(report.succeeded) + len(report.failed)
    if report.ok:
        print(f"\n{total} Datei(en) erfolgreich heruntergeladen!")
        print("Du findest sie im Download-Ordner.")
        return 0

    print(f"\nNur {len(report.succeeded)} von {total} Datei(en) heruntergeladen.")
    print("Fehlgeschlagen:")
    for name in report.failed:
        print(f"  - {name}")
    print('Tipp: yt-dlp aktualisieren mit  python3 -m pip install -U "yt-dlp[default]"')
    return 1


def main() -> int:
    """
    @brief Fragt Format, URL und ggf. Playlist-Umfang ab und startet den Download.
    @return Exit-Code für das Betriebssystem.
    """
    fmt = input("mp3 oder mp4: ").strip().lower()
    if fmt in VIDEO_KEYWORDS:
        downloader = vid_download
    elif fmt in AUDIO_KEYWORDS:
        downloader = mp3_downloader
    else:
        print("Dieses Format wird nicht unterstützt!!!")
        return 1

    link = input("Gib die URL von dem YT-Video an: \n").strip()
    whole_playlist = ask_whole_playlist(link)
    return print_report(downloader(link, whole_playlist=whole_playlist))


if __name__ == "__main__":
    sys.exit(main())
