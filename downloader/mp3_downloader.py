from yt_dlp import YoutubeDL

from .utils import CleanTitlePP, base_ydl_opts


def mp3_downloader(url):
    """
    Lädt nur Audio von einer YouTube-URL als .mp3 herunter.

    Funktioniert sowohl für einzelne Videos als auch für komplette
    Playlists. Bei Playlists werden die Dateien in der YouTube-Reihenfolge
    nummeriert ("01 - <Titel>.mp3", "02 - ..." etc.). Nicht mehr verfügbare
    Videos einer Playlist werden übersprungen, ohne dass der Vorgang
    abbricht. Altersbeschränkte Videos werden ohne Login heruntergeladen.

    Der Künstlername sowie Tags wie "Official Audio", "HD" usw. werden
    aus dem Dateinamen entfernt; ein "(feat. ...)"-Hinweis bleibt erhalten.
    """

    ydl_opts = base_ydl_opts()
    ydl_opts.update(
        {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
    )

    with YoutubeDL(ydl_opts) as ydl:
        # Postprocessor zum Säubern des Titels VOR der Dateinamenserzeugung.
        ydl.add_post_processor(CleanTitlePP(keep_features=True), when="pre_process")
        ydl.download([url])
