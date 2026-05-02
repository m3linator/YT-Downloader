**Language:** [🇩🇪 Deutsch](README.md) | 🇬🇧 English | [🇫🇷 Français](README.fr.md) | [🇹🇷 Türkçe](README.tr.md) | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
A program to download videos and audio from YouTube.

The program is already pre-built and available as a **[Release](https://github.com/m3linator/YT-Downloader/releases/latest)**.
*main* is compatible with macOS and Linux, and *main_win.exe* with Windows.


## Download

Get the latest version directly from the **[Releases page](https://github.com/m3linator/YT-Downloader/releases/latest)**:

| File | Platform |
|------|----------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

The binaries are self-contained — no Python required. Only `ffmpeg` needs to be installed separately (see [Requirements](#requirements)).


## What the program can do

When you start the program, you are prompted to choose between mp3 and mp4. Simply type your choice to confirm. Terms like *sound, audio, voice, video* and *film* are also accepted.
After that, just paste the link to the desired YouTube video and the download begins.

Additional features:

* **Playlists are numbered in order.** If you paste a playlist link, files are named in the exact YouTube order with a two-digit prefix, e.g. `01 - <title>.mp3`, `02 - <title>.mp3` …
* **Age-restricted / "explicit" videos** (e.g. some rap songs) are downloaded without requiring a login.
* **Clean filenames.** Artist prefixes and tags such as *Official Audio*, *Official Video*, *HD*, *Lyrics Video*, etc. are automatically removed from the filename. For mp3 downloads, any `(feat. ...)` part is kept.
* **Robust against dead videos.** Unavailable or regionally blocked videos in a playlist are silently skipped so the download does not abort.

All files are saved to the standard Downloads folder of your user account.


## Requirements

Only one module + `ffmpeg` is needed:

* `yt-dlp`
* `ffmpeg`

Install `yt-dlp` (Win/Mac/Linux):
```
pip install -r requirements.txt
```
or directly:
```
pip install yt-dlp
```
If that doesn't work:
```
python3 -m pip install yt-dlp
```

### ffmpeg Download

On macOS / Linux with a package manager:
```
[package-manager] install ffmpeg
```
e.g. `brew install ffmpeg` or `sudo apt install ffmpeg`.

On Windows, installing *ffmpeg* is a bit more involved.
Download [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) from the ffmpeg website and follow these steps:
  1. Extract the file, navigate to the `bin/` folder, and copy its path.
  2. Open Settings → System → Advanced system settings.
  3. Click on Environment Variables.
  4. Edit the PATH variable → New → paste the copied path.

Test in PowerShell:
```
ffmpeg -version
```


## Running the program

### Bare Metal (without venv activation)

Once `yt-dlp` and `ffmpeg` are installed system-wide, the script can be run directly with the system Python — no need to activate a virtual environment first:

```
python3 main.py
```

or directly executable (macOS/Linux):

```
./main.py
```

### Pre-built Binaries

On Windows, simply double-click the *main_win.exe* file. A terminal window will open automatically.

On macOS/Linux, open a terminal, navigate to the folder containing *main*, and run:
```
./main
```

### Build it yourself

If you want to rebuild the program after a code update:
```
pyinstaller -F --console main.py
```


## Project Structure

```
YT-Downloader/
├── main.py                       # Entry point (mp3/mp4 + URL prompt)
├── downloader/
│   ├── __init__.py
│   ├── utils.py                  # shared yt-dlp options + title cleaner
│   ├── mp3_downloader.py
│   └── mp4_downloader.py
├── requirements.txt
├── Programme/                    # pre-built binaries (macOS/Linux + Windows)
└── README.md
```


I hope this program helps you avoid all those mp3/mp4 downloaders full of ads and pop-ups.

Author:
Melih Erbas
