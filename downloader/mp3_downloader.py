import os
from pathlib import Path

import ffmpeg
from yt_dlp import YoutubeDL


def mp3_downloader(url):
    """Die Funktion erhällt einen YouTube link.
    Dieser Link wird danach als Audio also .mp3 Datei heruntergeladen
    und im Download-Ordner gespeichert"""

    speicherort = Path.home() / "Downloads"  # gibt Downloadsordner als Speicherort vor

    ydl_opts = {
        "outtmpl": f"{speicherort}/%(title)s.%(ext)s",
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

