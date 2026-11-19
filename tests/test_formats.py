"""
@file test_formats.py
@brief Unit-Tests für die Format-spezifischen yt-dlp Optionen (mp3 / mp4).
"""

from downloader.mp3_downloader import mp3_options
from downloader.mp4_downloader import mp4_options


def _keys(opts):
    return [pp["key"] for pp in opts["postprocessors"]]


def test_mp3_converts_to_mp3_and_embeds_metadata_and_cover():
    opts = mp3_options("tmpl")
    assert opts["outtmpl"] == "tmpl"
    assert opts["writethumbnail"] is True
    # Reihenfolge ist wichtig: Cover erst als JPG, Tags nach der Konvertierung.
    assert _keys(opts) == [
        "FFmpegThumbnailsConvertor",
        "FFmpegExtractAudio",
        "FFmpegMetadata",
        "EmbedThumbnail",
    ]
    assert opts["postprocessors"][1]["preferredcodec"] == "mp3"


def test_mp4_merges_best_streams_into_mp4():
    opts = mp4_options("tmpl")
    assert opts["format"] == "bestvideo+bestaudio/best"
    assert opts["merge_output_format"] == "mp4"
