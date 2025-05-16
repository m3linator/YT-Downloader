import os
import ffmpeg
from yt_dlp import YoutubeDL



def mp3_downloader(url):
    """Die Funktion erhällt einen YouTube link.
       Dieser Link wird danach als Audio also .mp3 Datei heruntergeladen
       und im Downloads-Ordner gespeichert"""

    speicherort = ''

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