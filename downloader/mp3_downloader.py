"""
@file mp3_downloader.py
@brief Audio-Download als .mp3.
"""

from __future__ import annotations

from .core import download
from .playlist import DownloadReport
from .utils import base_ydl_opts


def mp3_options(outtmpl: str | None = None) -> dict:
    """
    @brief yt-dlp Optionen für bestes Audio, konvertiert zu mp3 (192 kbit/s).
    @param outtmpl Dateinamen-Vorlage.
    @return Options-Dictionary.
    """
    opts = base_ydl_opts(outtmpl)
    opts.update(
        {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
            ],
        }
    )
    return opts


def mp3_downloader(url: str, *, whole_playlist: bool = False) -> DownloadReport:
    """
    @brief Lädt nur das Audio einer YouTube-URL (oder einer ganzen Playlist) als .mp3.

    Der Künstlername sowie Tags wie "Official Audio", "HD" usw. werden
    aus dem Dateinamen entfernt; ein "(feat. ...)"-Hinweis bleibt erhalten.

    @param url YouTube-URL.
    @param whole_playlist True = ganze Playlist parallel laden.
    @return Bericht über den Download.
    """
    return download(url, mp3_options, keep_features=True, whole_playlist=whole_playlist)
