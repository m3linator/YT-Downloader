**Sprache / Language:** [🇩🇪 Deutsch](README.md) | 🇬🇧 English | [🇫🇷 Français](README.fr.md) | [🇹🇷 Türkçe](README.tr.md) | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
A command-line program to download videos (mp4) and audio (mp3) from YouTube – without ads or pop-ups.

> The program's prompts are in German.


## Download

Pre-built versions are available on the **[Releases page](https://github.com/m3linator/YT-Downloader/releases/latest)**:

| File | Platform |
|------|----------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

> **Note:** The v1.0.0 binaries ship an outdated yt-dlp and fail on many videos with `HTTP Error 403`. Until a new release is out, please [run the program from source](#running-the-program).


## What the program can do

On start, the program asks for the format: **mp3** or **mp4**. Words like *Sound, Audio, Stimme, Video and Film* are accepted as well. Then paste the link – the download starts.

Features:

* **Playlist prompt.** If a video is part of a playlist (`watch?v=...&list=...`), the program asks:
  ```
  Der Link gehört zu einer Playlist.
    [1] Nur dieses Video (Standard)     -> only this video (default)
    [2] Ganze Playlist                  -> whole playlist
  ```
  A pure playlist link (`playlist?list=...`) downloads the whole playlist right away.
* **Parallel playlist downloads.** Playlists are downloaded with up to 4 videos at once (measured: 4 videos in 9.8 s instead of 25 s). Single videos are not affected.
* **Numbering in YouTube order.** Playlist files are named `01 - <title>.mp3`, `02 - <title>.mp3` … (three digits from 100 videos on).
* **Metadata and cover art in mp3s.** Title, artist and date are stored as tags, and the video thumbnail is embedded as cover art – visible in Apple Music, Spotify (local files), VLC, etc.
* **Clean file names.** Artist prefixes and tags like *Official Audio*, *Official Video*, *HD*, *Lyrics Video* are removed. For mp3, a `(feat. ...)` is kept.
* **Age-restricted videos** are downloaded as far as YouTube allows without login.
* **Honest status message.** The success message only appears if the download really worked. Otherwise the program lists the failed videos and exits with code `1`. Dead videos in a playlist don't stop the rest.

All files are saved to your user's Downloads folder (`~/Downloads`).


## Requirements

| Dependency | Purpose |
|------------|---------|
| Python ≥ 3.10 | Running the program |
| `yt-dlp[default]` | Downloading; the `[default]` extra installs `yt-dlp-ejs`, among others |
| `deno` | JavaScript runtime that `yt-dlp-ejs` uses to solve YouTube's challenge |
| `ffmpeg` | mp3 conversion, merging video + audio, embedding cover art |

> **Why `deno` and `yt-dlp-ejs`?** YouTube protects its download links with a JavaScript challenge. If it isn't solved, YouTube answers with `HTTP Error 403: Forbidden`. `deno` is the calculator, `yt-dlp-ejs` the formula sheet – you need both.

### Install the Python modules

```
python3 -m pip install -U -r requirements.txt
```

On macOS with Homebrew Python, pip blocks global installs (PEP 668, message `externally-managed-environment`). Install into your user directory instead:
```
python3 -m pip install --user --break-system-packages -U -r requirements.txt
```

### Install deno and ffmpeg

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

Alternatively, install ffmpeg on Windows manually: download [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the path of the `bin/` folder to the `PATH` environment variable (Settings → System → Advanced system settings → Environment Variables).

Test:
```
deno --version
ffmpeg -version
```


## Running the program

### From source (bare metal)

The program runs directly with the system Python – no virtual environment needed:
```
python3 main.py
```
or (macOS/Linux):
```
./main.py
```

Example:
```
mp3 oder mp4: mp3
Gib die URL von dem YT-Video an:
https://www.youtube.com/watch?v=...
...
1 Datei(en) erfolgreich heruntergeladen!
Du findest sie im Download-Ordner.
```

### Pre-built binaries

Windows: double-click *main_win.exe*.
macOS/Linux: in a terminal, go to the folder containing *main* and run `./main`.
`deno` and `ffmpeg` must be installed here as well.

### Build it yourself

```
python3 -m pip install --user pyinstaller
pyinstaller -F --console --collect-data yt_dlp_ejs main.py
```
`--collect-data yt_dlp_ejs` bundles the solver scripts into the binary. The result is in `dist/`.


## Tests

The unit tests run without network access (yt-dlp is replaced by test doubles):
```
python3 -m pytest -q
```


## Troubleshooting

| Message | Cause | Solution |
|---------|-------|----------|
| `HTTP Error 403: Forbidden` / `n challenge solving failed` | yt-dlp outdated, or `yt-dlp-ejs` / `deno` missing | `python3 -m pip install -U "yt-dlp[default]"` and install `deno` |
| `Fehler: 'yt-dlp' ist nicht installiert.` | Module missing in the Python being used | See [Install the Python modules](#install-the-python-modules) |
| `ffmpeg not found` | ffmpeg not in `PATH` | See [Install deno and ffmpeg](#install-deno-and-ffmpeg) |
| `externally-managed-environment` | Homebrew Python protects itself (PEP 668) | Use `--user --break-system-packages` |

YouTube changes constantly – for new errors, updating yt-dlp almost always helps.


## Project Structure

```
YT-Downloader/
├── main.py                  # Entry point: format, URL, playlist prompt, status message
├── downloader/
│   ├── __init__.py
│   ├── core.py              # shared download control (single video vs. playlist)
│   ├── playlist.py          # playlist detection, listing, parallel download
│   ├── utils.py             # yt-dlp base options, file name template, title cleaning
│   ├── mp3_downloader.py    # mp3 options (conversion, metadata, cover art)
│   └── mp4_downloader.py    # mp4 options (best video + audio)
├── tests/                   # pytest unit tests (no network)
├── Programme/               # pre-built binaries (macOS/Linux + Windows)
├── requirements.txt
└── README.md (+ en, fr, tr, zh)
```

Flow: `main.py` → `mp3_downloader` / `vid_download` → `core.download` → for a single video `download_one`, for a playlist `fetch_entries` + `download_parallel`.


I hope this program helps you avoid all those mp3/mp4 downloaders full of ads and pop-ups.

Author:
Melih Erbas


## Releases

### Unreleased
* **Fixed:** `HTTP Error 403` on YouTube – `yt-dlp[default]` (incl. JS challenge solver) and `deno` are now required.
* **Fixed:** The success message appeared even when the download failed.
* **New:** "only this video / whole playlist" prompt for videos inside a playlist.
* **New:** Parallel playlist downloads (up to 4 at once).
* **New:** Metadata and cover art in mp3 files.
* **Faster:** No more forced player clients (fewer requests).
* **Removed:** venv fallback – the program runs bare metal.
* **New:** Unit tests with pytest.

### [v1.0.0](https://github.com/m3linator/YT-Downloader/releases/tag/v1.0.0)
* First version: mp3/mp4 download, playlist numbering, clean file names, pre-built binaries for macOS/Linux and Windows.
