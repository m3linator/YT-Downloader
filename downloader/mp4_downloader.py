from yt_dlp import YoutubeDL

from .utils import CleanTitlePP, base_ydl_opts


def vid_download(url):
    """
    Lädt ein YouTube-Video als .mp4 herunter.

    Funktioniert sowohl für einzelne Videos als auch für komplette
    Playlists. Bei Playlists werden die Dateien in der YouTube-Reihenfolge
    nummeriert ("01 - <Titel>.mp4", "02 - ..." etc.). Nicht mehr verfügbare
    Videos einer Playlist werden übersprungen, ohne dass der Vorgang
    abbricht. Altersbeschränkte Videos werden ohne Login heruntergeladen.

    Künstler-Präfixe und Tags wie "Official Video", "HD" usw. werden aus
    dem Dateinamen entfernt; "(feat. ...)"-Zusätze werden bei Videos
    ebenfalls entfernt (für Songs siehe ``mp3_downloader``).
    """

    ydl_opts = base_ydl_opts()
    ydl_opts.update(
        {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }
    )

    with YoutubeDL(ydl_opts) as ydl:
        # Postprocessor zum Säubern des Titels VOR der Dateinamenserzeugung.
        ydl.add_post_processor(CleanTitlePP(keep_features=False), when="pre_process")
        ydl.download([url])
