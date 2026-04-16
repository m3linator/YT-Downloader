"""
Gemeinsame Hilfsfunktionen für den YT-Downloader.

Hier liegt alles, was sowohl der mp3- als auch der mp4-Downloader teilen:
  * Standard-Optionen für yt-dlp (Speicherort, Playlist-Nummerierung,
    Überspringen nicht verfügbarer Videos, Umgehung der Altersbeschränkung)
  * Eine Funktion zum Säubern der Videotitel (Künstler-Präfix sowie Tags
    wie "Official Audio", "HD" etc. werden entfernt)
  * Ein eigener yt-dlp Postprocessor, der den Titel vor dem Erstellen
    des Dateinamens anpasst, sodass die Datei direkt richtig benannt wird.
"""

from __future__ import annotations

import re
from pathlib import Path

from yt_dlp.postprocessor.common import PostProcessor


# Begriffe, die wir aus () oder [] heraus entfernen wollen.
# Es wird nur entfernt, wenn der Inhalt der Klammer (nach Trimmung) zu
# einem dieser Muster passt – so überleben sinnvolle Zusätze wie
# "(Live in Berlin)" oder "(Remix)".
_JUNK_PATTERNS = [
    r"official\s*music\s*video",
    r"official\s*video",
    r"official\s*audio",
    r"official\s*lyrics?\s*video",
    r"official\s*visualizer",
    r"official",
    r"music\s*video",
    r"lyrics?\s*video",
    r"lyric\s*video",
    r"lyrics?",
    r"audio",
    r"visualizer",
    r"karaoke",
    r"\d{3,4}p",
    r"4k",
    r"8k",
    r"hd",
    r"hq",
    r"hi[-\s]?res",
]
_JUNK_RE = re.compile(r"^\s*(?:" + "|".join(_JUNK_PATTERNS) + r")\s*$", re.IGNORECASE)
_FEATURE_RE = re.compile(r"\b(?:feat\.?|featuring|ft\.?)\b", re.IGNORECASE)

# Trennzeichen "Künstler - Titel". YouTube nutzt -, – oder —.
_ARTIST_SEP_RE = re.compile(r"\s+[-\u2013\u2014]\s+")

# Zeichen, die Windows/macOS in Dateinamen nicht mögen.
_INVALID_FS_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def _strip_decorative_blocks(title: str, *, keep_features: bool) -> str:
    """Entfernt Klammer-/Eckklammer-Blöcke mit Werbe-Tags wie 'Official Video'."""

    def replace(match: re.Match) -> str:
        content = match.group(1).strip()
        if keep_features and _FEATURE_RE.search(content):
            return match.group(0)
        if _JUNK_RE.match(content):
            return ""
        return match.group(0)

    # Mehrfach durchlaufen, falls verschachtelte Klammern vorhanden sind.
    previous = None
    while previous != title:
        previous = title
        title = re.sub(r"\(([^()]*)\)", replace, title)
        title = re.sub(r"\[([^\[\]]*)\]", replace, title)
    return title


def clean_title(title: str, *, keep_features: bool = False) -> str:
    """
    Säubert einen YouTube-Titel.

    * "Künstler - Song" -> "Song"
    * Entfernt Tags wie "(Official Video)", "[HD]", "(Audio)" usw.
    * Wenn ``keep_features`` True ist, bleiben "(feat. ...)"-Klammern erhalten
      (für mp3-Downloads gewünscht). Sonst werden auch diese entfernt.
    """

    if not title:
        return title

    # 1. Künstler-Präfix entfernen (nur am ersten Trenner aufteilen)
    parts = _ARTIST_SEP_RE.split(title, maxsplit=1)
    if len(parts) == 2:
        title = parts[1]

    # 2. Werbe-Tags entfernen
    title = _strip_decorative_blocks(title, keep_features=keep_features)

    # 3. Falls keine Features behalten werden sollen, jegliche feat.-Hinweise
    #    auch außerhalb von Klammern wegwerfen.
    if not keep_features:
        title = re.sub(
            r"\s*[\(\[]?\s*(?:feat\.?|featuring|ft\.?)[^\)\]]*[\)\]]?",
            "",
            title,
            flags=re.IGNORECASE,
        )

    # 4. Trailing-Tags hinter Pipe / Dash entfernen, z.B. "Song | Official Video".
    trailing_re = re.compile(
        r"\s*[\|\-\u2013\u2014\u2022]+\s*(?:" + "|".join(_JUNK_PATTERNS) + r")\s*$",
        re.IGNORECASE,
    )
    previous = None
    while previous != title:
        previous = title
        title = trailing_re.sub("", title)

    # 5. Aufräumen: doppelte Leerzeichen, hängende Bindestriche/Pipes.
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"[\|\-\u2013\u2014\u2022]+\s*$", "", title).strip()

    # 6. Filesystem-feindliche Zeichen entfernen.
    title = _INVALID_FS_CHARS.sub("", title)

    return title


class CleanTitlePP(PostProcessor):
    """
    yt-dlp Postprocessor, der vor dem Download (im ``pre_process``-Schritt)
    den Titel säubert. Da yt-dlp den Dateinamen aus ``info['title']``
    aufbaut, ist der heruntergeladene Datei direkt korrekt benannt – wir
    sparen uns ein nachträgliches Umbenennen.
    """

    def __init__(self, downloader=None, *, keep_features: bool = False):
        super().__init__(downloader)
        self.keep_features = keep_features

    def run(self, info):
        original = info.get("title") or ""
        cleaned = clean_title(original, keep_features=self.keep_features)
        if cleaned and cleaned != original:
            info["title"] = cleaned
        return [], info


def get_download_dir() -> Path:
    """Standard-Speicherort: der Downloads-Ordner des Benutzers."""
    return Path.home() / "Downloads"


def base_ydl_opts() -> dict:
    """
    Gemeinsame yt-dlp Optionen für mp3- und mp4-Downloads.

    Enthält:
      * Speicherort + Vorlage mit optionaler "01 - "-Nummerierung,
        falls eine Playlist heruntergeladen wird.
      * ``ignoreerrors`` damit nicht verfügbare Videos in einer Playlist
        einfach übersprungen werden.
      * Umgehung der YouTube-Altersbeschränkung über alternative
        Player-Clients (kein Login nötig).
    """
    download_dir = get_download_dir()

    # %(playlist_index&CONSEQUENT|ALTERNATE)s ist die yt-dlp-Konditional-
    # syntax: existiert ein playlist_index, wird "01 - " vorangestellt,
    # ansonsten bleibt die Datei einfach "<Titel>.<ext>".
    outtmpl = str(download_dir / "%(playlist_index&{0:02d} - |)s%(title)s.%(ext)s")

    return {
        "outtmpl": outtmpl,
        # Playlist-Indizes garantiert konsistent zur YouTube-Reihenfolge.
        "playlist_items": None,
        # Nicht verfügbare / gelöschte / regional gesperrte Videos überspringen.
        "ignoreerrors": True,
        # Alters-Beschränkung umgehen: hohe Grenze + mehrere Player-Clients
        # als Fallback. ``default`` lässt yt-dlp die jeweils aktuell besten
        # Clients wählen (das ändert sich mit jeder yt-dlp Version, da
        # YouTube seine Endpoints regelmäßig dichtmacht). ``tv_simply`` und
        # ``web_embedded`` sind die zuverlässigen Fallbacks für altersbe-
        # schränkte Inhalte ohne Login.
        # WICHTIG: Sollte der Fehler "YouTube is no longer supported in
        # this application or device" auftreten, ist meistens yt-dlp zu
        # alt – mit ``./venv/bin/pip install -U yt-dlp`` aktualisieren.
        "age_limit": 99,
        "extractor_args": {
            "youtube": {
                "player_client": ["default", "tv_simply", "web_embedded"],
            }
        },
        # Bei Playlists einen kompakten Statusausdruck behalten.
        "noprogress": False,
        "quiet": False,
        "no_warnings": False,
    }
