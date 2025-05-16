import os
from yt_dlp import YoutubeDL

def vid_download(url):

    speicherort = '/Users/melih/Documents/Privat/Video-Downloads-PY'       #gibt speicherort vor

    ydl_opts = {
        'outtmpl': f'{speicherort}/%(title)s.%(ext)s',      #Name von gespeichertem Video
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.download([url])

