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

    Zusätzlich werden Titel, Künstler, Datum usw. als ID3-Tags gesetzt und
    das Video-Thumbnail als Cover eingebettet. YouTube liefert Thumbnails
    meist als WebP, das viele Player in mp3 nicht anzeigen – daher vorher
    Konvertierung zu JPG.

    @param outtmpl Dateinamen-Vorlage.
    @return Options-Dictionary.
    """
    opts = base_ydl_opts(outtmpl)
    opts.update(
        {
            "format": "bestaudio/best",
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegThumbnailsConvertor",
                    "format": "jpg",
                    "when": "before_dl",
                },
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {
                    "key": "FFmpegMetadata",
                    "add_metadata": True,
                },
                {
                    # Löscht die Thumbnail-Datei nach dem Einbetten.
                    "key": "EmbedThumbnail",
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
    Metadaten und Cover werden in die mp3 eingebettet.

    @param url YouTube-URL.
    @param whole_playlist True = ganze Playlist parallel laden.
    @return Bericht über den Download.
    """
    return download(url, mp3_options, keep_features=True, whole_playlist=whole_playlist)
