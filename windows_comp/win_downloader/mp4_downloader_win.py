import os
from yt_dlp import YoutubeDL
from pathlib import Path

def vid_download(url):
    """Die Funktion erhällt einen YouTube link.
       Dieser Link wird danach als Video also .mp4 Datei heruntergeladen
       und im Ordner '/Users/melih/Documents/Privat/Video-Downloads-PY' gespeichert"""

    speicherort = Path.home() / "Downloads"  #gibt Downloadordner als Speicherort vor

    ydl_opts = {
        'outtmpl': f'{speicherort}/%(title)s.%(ext)s',      #Name von gespeichertem Video
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])

