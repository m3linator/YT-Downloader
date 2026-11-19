"""
Gemeinsame Hilfsfunktionen für den YT-Downloader.

Hier liegt alles, was sowohl der mp3- als auch der mp4-Downloader teilen:
  * Standard-Optionen für yt-dlp (Speicherort, Dateinamen-Vorlage,
    Überspringen nicht verfügbarer Videos)
  * Eine Funktion zum Säubern der Videotitel (Künstler-Präfix sowie Tags
    wie "Official Audio", "HD" etc. werden entfernt)
  * Ein eigener yt-dlp Postprocessor, der den Titel vor dem Erstellen
    des Dateinamens anpasst, sodass die Datei direkt richtig benannt wird,
    und den Künstler für die Metadaten übernimmt.
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


def split_artist(title: str) -> tuple[str | None, str]:
    """
    @brief Trennt "Künstler - Titel" am ersten Trennzeichen auf.
    @param title Originaltitel des Videos.
    @return (Künstler, Rest) oder (None, title), falls kein Trenner existiert.
    """
    parts = _ARTIST_SEP_RE.split(title, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1]
    return None, title


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
    _, title = split_artist(title)

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
    aufbaut, ist die heruntergeladene Datei direkt korrekt benannt – wir
    sparen uns ein nachträgliches Umbenennen.

    Liefert YouTube keinen Künstler, wird er aus "Künstler - Titel"
    übernommen, damit die eingebetteten Metadaten stimmen.
    """

    def __init__(self, downloader=None, *, keep_features: bool = False):
        super().__init__(downloader)
        self.keep_features = keep_features

    def run(self, info):
        original = info.get("title") or ""
        artist, _ = split_artist(original)
        if artist and not info.get("artist"):
            info["artist"] = artist
        cleaned = clean_title(original, keep_features=self.keep_features)
        if cleaned and cleaned != original:
            info["title"] = cleaned
        return [], info


def get_download_dir() -> Path:
    """
    @brief Standard-Speicherort: der Downloads-Ordner des Benutzers.
    @return Pfad zu ~/Downloads.
    """
    return Path.home() / "Downloads"


def build_outtmpl(index: int | None = None, width: int = 2) -> str:
    """
    @brief Baut die yt-dlp Dateinamen-Vorlage.
    @param index Position in der Playlist (1-basiert) oder None für Einzelvideos.
    @param width Mindestanzahl Ziffern der Nummerierung ("01", "001", ...).
    @return Vorlage wie "~/Downloads/03 - %(title)s.%(ext)s".
    """
    prefix = f"{index:0{width}d} - " if index is not None else ""
    return str(get_download_dir() / f"{prefix}%(title)s.%(ext)s")


def base_ydl_opts(outtmpl: str | None = None) -> dict:
    """
    @brief Gemeinsame yt-dlp Optionen für mp3- und mp4-Downloads.

    Bewusst wird KEIN ``player_client`` erzwungen: yt-dlp wählt die je
    Version funktionierenden Clients selbst. Feste Clients wie
    ``tv_simply`` kosten zusätzliche Requests und werden ohne PO-Token
    ohnehin übersprungen.

    @param outtmpl Eigene Dateinamen-Vorlage; Standard: build_outtmpl().
    @return Options-Dictionary für ``YoutubeDL``.
    """
    return {
        "outtmpl": outtmpl or build_outtmpl(),
        # Fehler melden, aber nicht abbrechen. Ob alles geklappt hat,
        # verrät der Rückgabewert von ``YoutubeDL.download``.
        "ignoreerrors": True,
        "age_limit": 99,
        # Fragmentierte Formate (DASH/HLS) parallel laden.
        "concurrent_fragment_downloads": 4,
    }
