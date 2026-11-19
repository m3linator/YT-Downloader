"""
@file mp4_downloader.py
@brief Video-Download als .mp4.
"""

from __future__ import annotations

from .core import download
from .playlist import DownloadReport
from .utils import base_ydl_opts


def mp4_options(outtmpl: str | None = None) -> dict:
    """
    @brief yt-dlp Optionen für bestes Video + Audio, zusammengeführt als mp4.
    @param outtmpl Dateinamen-Vorlage.
    @return Options-Dictionary.
    """
    opts = base_ydl_opts(outtmpl)
    opts.update(
        {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }
    )
    return opts


def vid_download(url: str, *, whole_playlist: bool = False) -> DownloadReport:
    """
    @brief Lädt ein YouTube-Video (oder eine ganze Playlist) als .mp4 herunter.

    Künstler-Präfixe und Tags wie "Official Video", "HD" usw. werden aus
    dem Dateinamen entfernt; "(feat. ...)"-Zusätze ebenfalls.

    @param url YouTube-URL.
    @param whole_playlist True = ganze Playlist parallel laden.
    @return Bericht über den Download.
    """
    return download(url, mp4_options, keep_features=False, whole_playlist=whole_playlist)
