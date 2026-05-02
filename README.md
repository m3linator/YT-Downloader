**Sprache / Language:** 🇩🇪 Deutsch | [🇬🇧 English](README.en.md) | [🇫🇷 Français](README.fr.md) | [🇹🇷 Türkçe](README.tr.md) | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
Ein Programm, mit dem man Videos und Audios von YouTube herunterladen kann.

Das Programm ist bereits fertig gebaut und steht als **[Release](https://github.com/m3linator/YT-Downloader/releases/latest)** zum Download bereit.
*main* ist kompatibel mit macOS und Linux und *main_win.exe* mit Windows.


## Download

Die neueste Version gibt es direkt auf der **[Releases-Seite](https://github.com/m3linator/YT-Downloader/releases/latest)**:

| Datei | Plattform |
|-------|-----------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

Die Binaries sind eigenständig – kein Python nötig. Nur `ffmpeg` muss separat installiert werden (siehe [Anforderungen](#anforderungen)).


## Was das Programm kann

Wenn man das Programm startet, wird einem die Auswahl zwischen mp3 und mp4 angeboten. Durch simples Eingeben wird die Auswahl gespeichert. Begriffe wie *Sound, Audio, Stimme, Video und Film* werden ebenfalls akzeptiert.
Danach muss man nur noch den Link vom gewünschten YouTube-Video einfügen und der Download beginnt.

Zusätzliche Features:

* **Playlists werden in Reihenfolge nummeriert.** Hängt man einen Playlist-Link rein, werden die Dateien in der exakten YouTube-Reihenfolge mit zweistelligem Präfix benannt, z. B. `01 - <Titel>.mp3`, `02 - <Titel>.mp3` ...
* **Altersbeschränkte / „explizite" Videos** (z. B. einige Rap-Songs) werden ohne Login heruntergeladen.
* **Saubere Dateinamen.** Künstler-Präfixe und Tags wie *Official Audio*, *Official Video*, *HD*, *Lyrics Video* etc. werden automatisch aus dem Dateinamen entfernt. Bei mp3-Downloads bleibt ein eventuelles `(feat. ...)` erhalten.
* **Robust gegen tote Videos.** Nicht mehr verfügbare oder regional gesperrte Videos einer Playlist werden stillschweigend übersprungen, sodass der Download nicht abbricht.

Alle Dateien landen im Standard-Downloads-Ordner deines Benutzers.


## Anforderungen

Es wird nur ein Modul + `ffmpeg` benötigt:

* `yt-dlp`
* `ffmpeg`

Installation von `yt-dlp` (Win/Mac/Linux):
```
pip install -r requirements.txt
```
oder direkt:
```
pip install yt-dlp
```
Falls das nicht funktioniert:
```
python3 -m pip install yt-dlp
```

### ffmpeg Download

Auf macOS / Linux mit Paketmanager:
```
[paketmanager] install ffmpeg
```
z. B. `brew install ffmpeg` oder `sudo apt install ffmpeg`.

Auf Windows ist der Download von *ffmpeg* etwas umständlicher.
Lade dir dafür von der ffmpeg-Seite die [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) herunter und führe folgende Schritte durch:
  1. Datei entpacken, in den Ordner `bin/` navigieren und dessen Pfad-Link kopieren.
  2. Öffne die Einstellungen → System → erweiterte Systemeinstellungen
  3. Klicke auf Umgebungsvariable
  4. Bearbeite die Variable PATH → Neu → füge den kopierten Pfad ein

Test in PowerShell:
```
ffmpeg -version
```


## Programm ausführen

### Bare Metal (ohne venv-Aktivierung)

Sobald `yt-dlp` und `ffmpeg` system-weit installiert sind, kann das Skript direkt mit dem System-Python aufgerufen werden – ohne dass vorher eine virtuelle Umgebung aktiviert werden muss:

```
python3 main.py
```

oder direkt ausführbar (macOS/Linux):

```
./main.py
```

### Vorgebaute Binaries

Auf Windows reicht es, auf die *main_win.exe* Datei doppelt zu klicken. Es öffnet sich automatisch ein Terminal-Fenster.

Auf macOS/Linux öffnest du ein Terminal, navigierst in den Pfad mit der Datei *main* und führst aus:
```
./main
```

### Selber bauen

Wenn du das Programm nach einem Code-Update neu bauen möchtest:
```
pyinstaller -F --console main.py
```


## Projektstruktur

```
YT-Downloader/
├── main.py                       # Einstiegspunkt (mp3/mp4 + URL abfragen)
├── downloader/
│   ├── __init__.py
│   ├── utils.py                  # geteilte yt-dlp Optionen + Titel-Cleaner
│   ├── mp3_downloader.py
│   └── mp4_downloader.py
├── requirements.txt
├── Programme/                    # vorgebaute Binaries (macOS/Linux + Windows)
└── README.md
```


Ich hoffe das Programm hilft dir, die ganzen mp3/mp4 Downloader mit Werbungen und Pop-ups zu umgehen.

Autor:
Melih Erbas
