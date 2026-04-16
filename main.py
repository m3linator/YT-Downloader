#!/usr/bin/env python3
"""
YT-Downloader Einstiegspunkt.

Fragt nach Format (mp3 / mp4) und URL (Einzelvideo oder Playlist) und
delegiert den Download an die passende Funktion. Heruntergeladen wird
in den Standard-Downloads-Ordner des Benutzers.

Damit das Programm wirklich "bare metal" – ohne vorherige venv-Aktivierung –
läuft, prüft es beim Start, ob ``yt-dlp`` im aktuell laufenden Python
verfügbar ist. Falls nicht, startet es sich selbst durch den im Projekt
mitgelieferten ``venv``-Interpreter neu (sofern vorhanden). Andernfalls
gibt es eine klare Installationsanweisung aus.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _ensure_yt_dlp() -> None:
    """Stellt sicher, dass ``yt_dlp`` importierbar ist.

    Strategie:
      1. Versuche ``yt_dlp`` zu importieren – wenn es klappt, ist alles gut.
      2. Sonst suche das mitgelieferte ``venv`` neben diesem Skript und
         starte das Skript mit dessen Python neu (``os.execv``). Damit
         läuft alles im venv, ohne dass der Benutzer es aktivieren muss.
      3. Wenn auch das nicht klappt, eine verständliche Fehlermeldung.
    """
    try:
        import yt_dlp  # noqa: F401
        return
    except ImportError:
        pass

    here = Path(__file__).resolve().parent
    venv_pythons = [
        here / "venv" / "bin" / "python",         # macOS / Linux
        here / "venv" / "bin" / "python3",
        here / "venv" / "Scripts" / "python.exe",  # Windows
    ]
    current = Path(sys.executable).resolve()

    for python in venv_pythons:
        if python.exists() and python.resolve() != current:
            # Re-Exec mit dem venv-Python. argv unverändert weitergeben,
            # damit z.B. spätere CLI-Argumente erhalten bleiben.
            os.execv(str(python), [str(python), str(Path(__file__).resolve()), *sys.argv[1:]])

    sys.stderr.write(
        "Fehler: 'yt-dlp' ist nicht installiert.\n"
        "Installiere es mit einem der folgenden Befehle:\n"
        "  pip3 install yt-dlp\n"
        "  python3 -m pip install yt-dlp\n"
        "  brew install yt-dlp     (macOS)\n"
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
