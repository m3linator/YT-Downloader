**Sprache / Language:** 🇩🇪 Deutsch | [🇬🇧 English](README.en.md) | [🇫🇷 Français](README.fr.md) | [🇹🇷 Türkçe](README.tr.md) | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
Ein Kommandozeilen-Programm, mit dem man Videos (mp4) und Audios (mp3) von YouTube herunterladen kann – ohne Werbung und Pop-ups.


## Download

Vorgebaute Versionen gibt es auf der **[Releases-Seite](https://github.com/m3linator/YT-Downloader/releases/latest)**:

| Datei | Plattform |
|-------|-----------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

> **Hinweis:** Die Binaries von v1.0.0 enthalten eine veraltete yt-dlp-Version und scheitern bei vielen Videos mit `HTTP Error 403`. Bis zu einem neuen Release das Programm bitte [aus dem Quellcode starten](#programm-ausführen).


## Was das Programm kann

Beim Start fragt das Programm nach dem Format: **mp3** oder **mp4**. Begriffe wie *Sound, Audio, Stimme, Video und Film* werden ebenfalls akzeptiert. Danach den Link einfügen – der Download beginnt.

Features:

* **Playlist-Abfrage.** Ist ein Video Teil einer Playlist (`watch?v=...&list=...`), fragt das Programm nach:
  ```
  Der Link gehört zu einer Playlist.
    [1] Nur dieses Video (Standard)
    [2] Ganze Playlist
  ```
  Ein reiner Playlist-Link (`playlist?list=...`) lädt direkt die ganze Playlist.
* **Parallele Playlist-Downloads.** Playlists werden mit bis zu 4 Videos gleichzeitig geladen (gemessen: 4 Videos in 9,8 s statt 25 s). Einzelvideos sind davon nicht betroffen.
* **Nummerierung in YouTube-Reihenfolge.** Playlist-Dateien heißen `01 - <Titel>.mp3`, `02 - <Titel>.mp3` … (ab 100 Videos dreistellig).
* **Metadaten und Cover in mp3s.** Titel, Künstler und Datum werden als Tags gespeichert, das Video-Thumbnail wird als Cover eingebettet – sichtbar in Apple Music, Spotify (lokale Dateien), VLC usw.
* **Saubere Dateinamen.** Künstler-Präfixe und Tags wie *Official Audio*, *Official Video*, *HD*, *Lyrics Video* werden entfernt. Bei mp3 bleibt ein `(feat. ...)` erhalten.
* **Altersbeschränkte Videos** werden – soweit YouTube es ohne Login erlaubt – heruntergeladen.
* **Ehrliche Statusmeldung.** Die Erfolgsmeldung erscheint nur, wenn der Download wirklich geklappt hat. Andernfalls listet das Programm die fehlgeschlagenen Videos auf und beendet sich mit Exit-Code `1`. Tote Videos in einer Playlist stoppen den Rest nicht.

Alle Dateien landen im Downloads-Ordner deines Benutzers (`~/Downloads`).


## Anforderungen

| Abhängigkeit | Wofür |
|--------------|-------|
| Python ≥ 3.10 | Ausführen des Programms |
| `yt-dlp[default]` | Download; das Extra `[default]` installiert u. a. `yt-dlp-ejs` |
| `deno` | JavaScript-Laufzeit, mit der `yt-dlp-ejs` die YouTube-Challenge löst |
| `ffmpeg` | mp3-Konvertierung, Zusammenführen von Video + Audio, Cover-Einbettung |

> **Warum `deno` und `yt-dlp-ejs`?** YouTube schützt seine Download-Links mit einer JavaScript-Challenge. Ohne Lösung antwortet YouTube mit `HTTP Error 403: Forbidden`. `deno` ist der Taschenrechner, `yt-dlp-ejs` das Formelblatt – es braucht beides.

### Python-Module installieren

```
python3 -m pip install -U -r requirements.txt
```

Auf macOS mit Homebrew-Python blockiert pip globale Installationen (PEP 668, Meldung `externally-managed-environment`). Dann ins Benutzerverzeichnis installieren:
```
python3 -m pip install --user --break-system-packages -U -r requirements.txt
```

### deno und ffmpeg installieren

macOS:
```
brew install deno ffmpeg
```

Linux (Debian/Ubuntu):
```
sudo apt install ffmpeg
curl -fsSL https://deno.land/install.sh | sh
```

Windows (PowerShell):
```
winget install DenoLand.Deno
winget install Gyan.FFmpeg
```

Alternativ ffmpeg unter Windows manuell: [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) herunterladen, entpacken, den Pfad des Ordners `bin/` zur Umgebungsvariable `PATH` hinzufügen (Einstellungen → System → Erweiterte Systemeinstellungen → Umgebungsvariablen).

Test:
```
deno --version
ffmpeg -version
```


## Programm ausführen

### Aus dem Quellcode (bare metal)

Das Programm läuft direkt mit dem System-Python – keine virtuelle Umgebung nötig:
```
python3 main.py
```
oder (macOS/Linux):
```
./main.py
```

Beispiel:
```
mp3 oder mp4: mp3
Gib die URL von dem YT-Video an:
https://www.youtube.com/watch?v=...
...
1 Datei(en) erfolgreich heruntergeladen!
Du findest sie im Download-Ordner.
```

### Vorgebaute Binaries

Windows: Doppelklick auf *main_win.exe*.
macOS/Linux: Im Terminal in den Ordner mit *main* wechseln und `./main` ausführen.
`deno` und `ffmpeg` müssen auch hier installiert sein.

### Selber bauen

```
python3 -m pip install --user pyinstaller
pyinstaller -F --console --collect-data yt_dlp_ejs main.py
```
`--collect-data yt_dlp_ejs` packt die Solver-Skripte mit in die Binary. Das Ergebnis liegt in `dist/`.


## Tests

Die Unit-Tests laufen ohne Netzwerk (yt-dlp wird durch Test-Doubles ersetzt):
```
python3 -m pytest -q
```


## Fehlerbehebung

| Meldung | Ursache | Lösung |
|---------|---------|--------|
| `HTTP Error 403: Forbidden` / `n challenge solving failed` | yt-dlp veraltet oder `yt-dlp-ejs` / `deno` fehlt | `python3 -m pip install -U "yt-dlp[default]"` und `deno` installieren |
| `Fehler: 'yt-dlp' ist nicht installiert.` | Modul fehlt im verwendeten Python | Siehe [Python-Module installieren](#python-module-installieren) |
| `ffmpeg not found` | ffmpeg nicht im `PATH` | Siehe [deno und ffmpeg installieren](#deno-und-ffmpeg-installieren) |
| `externally-managed-environment` | Homebrew-Python schützt sich (PEP 668) | `--user --break-system-packages` verwenden |

YouTube ändert sich ständig – bei neuen Fehlern hilft fast immer ein Update von yt-dlp.


## Projektstruktur

```
YT-Downloader/
├── main.py                  # Einstiegspunkt: Format, URL, Playlist-Abfrage, Statusmeldung
├── downloader/
│   ├── __init__.py
│   ├── core.py              # gemeinsame Download-Steuerung (Einzelvideo vs. Playlist)
│   ├── playlist.py          # Playlist-Erkennung, Auslesen, paralleler Download
│   ├── utils.py             # yt-dlp Basis-Optionen, Dateinamen-Vorlage, Titel-Säuberung
│   ├── mp3_downloader.py    # mp3-Optionen (Konvertierung, Metadaten, Cover)
│   └── mp4_downloader.py    # mp4-Optionen (bestes Video + Audio)
├── tests/                   # pytest Unit-Tests (ohne Netzwerk)
├── Programme/               # vorgebaute Binaries (macOS/Linux + Windows)
├── requirements.txt
└── README.md (+ en, fr, tr, zh)
```

Ablauf: `main.py` → `mp3_downloader` / `vid_download` → `core.download` → bei Einzelvideo `download_one`, bei Playlist `fetch_entries` + `download_parallel`.


Ich hoffe, das Programm hilft dir, die ganzen mp3/mp4-Downloader mit Werbung und Pop-ups zu umgehen.

Autor:
Melih Erbas


## Releases

### Unveröffentlicht
* **Behoben:** `HTTP Error 403` bei YouTube – `yt-dlp[default]` (inkl. JS-Challenge-Solver) und `deno` werden vorausgesetzt.
* **Behoben:** Erfolgsmeldung erschien auch bei fehlgeschlagenem Download.
* **Neu:** Abfrage „nur dieses Video / ganze Playlist“ bei Videos innerhalb einer Playlist.
* **Neu:** Parallele Playlist-Downloads (bis zu 4 gleichzeitig).
* **Neu:** Metadaten und Cover in mp3-Dateien.
* **Schneller:** Keine erzwungenen Player-Clients mehr (weniger Requests).
* **Entfernt:** venv-Fallback – das Programm läuft bare metal.
* **Neu:** Unit-Tests mit pytest.

### [v1.0.0](https://github.com/m3linator/YT-Downloader/releases/tag/v1.0.0)
* Erste Version: mp3/mp4-Download, Playlist-Nummerierung, saubere Dateinamen, vorgebaute Binaries für macOS/Linux und Windows.
