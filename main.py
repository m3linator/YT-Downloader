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


AUDIO_KEYWORDS = {"mp3", "sound", "audio", "stimme"}
VIDEO_KEYWORDS = {"mp4", "video", "film"}


def main() -> None:
    fmt = input("mp3 oder mp4: ").strip().lower()
    link = input("Gib die URL von dem YT-Video an: \n").strip()

    if fmt in VIDEO_KEYWORDS:
        vid_download(link)
    elif fmt in AUDIO_KEYWORDS:
        mp3_downloader(link)
    else:
        print("Dieses Format wird nicht unterstützt!!!")
        return

    print("\nDeine Datei(en) wurde(n) erfolgreich heruntergeladen!")
    print("Du findest sie im Download-Ordner.")


if __name__ == "__main__":
    main()
