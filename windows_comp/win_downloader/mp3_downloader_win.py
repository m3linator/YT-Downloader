import os
import ffmpeg
from yt_dlp import YoutubeDL
from pathlib import Path


def mp3_downloader(url):
    """Die Funktion erhällt einen YouTube link.
       Dieser Link wird danach als Audio also .mp3 Datei heruntergeladen
       und im Ordner '/Users/melih/Documents/Privat/Video-Downloads-PY' gespeichert"""

    speicherort  = Path.home() / "Downloads"    # gibt Downloadsordner als Speicherort vor

    ydl_opts = {
        'outtmpl': f'{speicherort}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])