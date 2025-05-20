import os
import ffmpeg
from yt_dlp import YoutubeDL
from pathlib import Path

def vid_download(url):
    """
        Lädt Video von der YT url herunter

	    Die Funktion erhällt einen YouTube link.
        Dieser Link wird danach als Video also .mp4 Datei heruntergeladen
        und im Download-Ordner gespeichert

        """

    speicherort = Path.home() / "Downloads"  #gibt Downloadordner als Speicherort vor

    ydl_opts = {
        'outtmpl': f'{speicherort}/%(title)s.%(ext)s',      #Name von gespeichertem Video
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])

