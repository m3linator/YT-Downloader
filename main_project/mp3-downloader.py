import os
import ffmpeg
from yt_dlp import YoutubeDL



def lade_mp3(url, zielverzeichnis="."):

    speicherort = '/Users/melih/Documents/Privat/Video-Downloads-PY'

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