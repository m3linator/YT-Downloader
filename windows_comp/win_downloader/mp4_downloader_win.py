import os
import ffmpeg
from yt_dlp import YoutubeDL

def vid_download(url):
    """Die Funktion erhällt einen YouTube link.
       Dieser Link wird danach als Video also .mp4 Datei heruntergeladen
       und im Downloads-Ordner gespeichert"""

    #speicherort = r'C:\Users\ferba\Downloads'       #gibt Speicherort in Windows vor
    speicherort = r'C:\Users\Melih\Documents'
    
    ydl_opts = {
        'outtmpl': f'{speicherort}/%(title)s.%(ext)s',      #Name von gespeichertem Video
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])

