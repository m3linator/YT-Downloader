**Sprache / Language:** [🇩🇪 Deutsch](README.md) | [🇬🇧 English](README.en.md) | [🇫🇷 Français](README.fr.md) | [🇹🇷 Türkçe](README.tr.md) | 🇨🇳 中文

---

# YT-Downloader
一个命令行程序，用于从 YouTube 下载视频（mp4）和音频（mp3）——没有广告，也没有弹窗。

> 程序的提示信息为德语。


## 下载

预编译版本可在 **[Releases 页面](https://github.com/m3linator/YT-Downloader/releases/latest)** 获取：

| 文件 | 平台 |
|------|------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

> **注意：** v1.0.0 的二进制文件包含过时的 yt-dlp，许多视频会因 `HTTP Error 403` 而失败。在新版本发布之前，请[从源码运行程序](#运行程序)。


## 程序功能

启动时，程序会询问格式：**mp3** 或 **mp4**。也可以输入 *Sound、Audio、Stimme、Video 和 Film* 等词。然后粘贴链接，下载即开始。

功能：

* **播放列表询问。** 如果视频属于某个播放列表（`watch?v=...&list=...`），程序会询问：
  ```
  Der Link gehört zu einer Playlist.
    [1] Nur dieses Video (Standard)     -> 仅此视频（默认）
    [2] Ganze Playlist                  -> 整个播放列表
  ```
  纯播放列表链接（`playlist?list=...`）会直接下载整个播放列表。
* **并行下载播放列表。** 最多同时下载 4 个视频（实测：4 个视频用时 9.8 秒，而非 25 秒）。单个视频不受影响。
* **按 YouTube 顺序编号。** 播放列表文件命名为 `01 - <标题>.mp3`、`02 - <标题>.mp3` ……（100 个视频起使用三位数）。
* **mp3 中的元数据和封面。** 标题、艺术家和日期会保存为标签，视频缩略图会作为封面嵌入——可在 Apple Music、Spotify（本地文件）、VLC 等中显示。
* **干净的文件名。** 会删除艺术家前缀以及 *Official Audio*、*Official Video*、*HD*、*Lyrics Video* 等标签。mp3 会保留 `(feat. ...)`。
* **年龄限制视频**在 YouTube 允许免登录的范围内可以下载。
* **如实的状态信息。** 只有下载真正成功时才会显示成功信息。否则程序会列出失败的视频，并以退出码 `1` 结束。播放列表中失效的视频不会中断其余下载。

所有文件都保存在当前用户的下载文件夹（`~/Downloads`）中。


## 环境要求

| 依赖 | 用途 |
|------|------|
| Python ≥ 3.10 | 运行程序 |
| `yt-dlp[default]` | 下载；`[default]` 扩展会一并安装 `yt-dlp-ejs` 等组件 |
| `deno` | `yt-dlp-ejs` 用来解决 YouTube 验证的 JavaScript 运行时 |
| `ffmpeg` | mp3 转换、合并视频与音频、嵌入封面 |

> **为什么需要 `deno` 和 `yt-dlp-ejs`？** YouTube 用 JavaScript 验证（challenge）保护下载链接。如果无法解开，YouTube 会返回 `HTTP Error 403: Forbidden`。`deno` 是计算器，`yt-dlp-ejs` 是公式表——两者缺一不可。

### 安装 Python 模块

```
python3 -m pip install -U -r requirements.txt
```

在使用 Homebrew Python 的 macOS 上，pip 会阻止全局安装（PEP 668，提示 `externally-managed-environment`）。此时请安装到用户目录：
```
python3 -m pip install --user --break-system-packages -U -r requirements.txt
```

### 安装 deno 和 ffmpeg

macOS：
```
brew install deno ffmpeg
```

Linux（Debian/Ubuntu）：
```
sudo apt install ffmpeg
curl -fsSL https://deno.land/install.sh | sh
```

Windows（PowerShell）：
```
winget install DenoLand.Deno
winget install Gyan.FFmpeg
```

也可以在 Windows 上手动安装 ffmpeg：下载 [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/)，解压后将 `bin/` 文件夹的路径添加到 `PATH` 环境变量（设置 → 系统 → 高级系统设置 → 环境变量）。

测试：
```
deno --version
ffmpeg -version
```


## 运行程序

### 从源码运行（直接运行）

程序直接使用系统 Python 运行——无需虚拟环境：
```
python3 main.py
```
或（macOS/Linux）：
```
./main.py
```

示例：
```
mp3 oder mp4: mp3
Gib die URL von dem YT-Video an:
https://www.youtube.com/watch?v=...
...
1 Datei(en) erfolgreich heruntergeladen!
Du findest sie im Download-Ordner.
```

### 使用预编译二进制文件

Windows：双击 *main_win.exe*。
macOS/Linux：在终端中进入 *main* 所在文件夹并运行 `./main`。
同样需要安装 `deno` 和 `ffmpeg`。

### 自行编译

```
python3 -m pip install --user pyinstaller
pyinstaller -F --console --collect-data yt_dlp_ejs main.py
```
`--collect-data yt_dlp_ejs` 会把求解脚本打包进二进制文件。结果位于 `dist/`。


## 测试

单元测试无需网络（yt-dlp 由测试替身代替）：
```
python3 -m pytest -q
```


## 故障排除

| 信息 | 原因 | 解决方法 |
|------|------|----------|
| `HTTP Error 403: Forbidden` / `n challenge solving failed` | yt-dlp 过时，或缺少 `yt-dlp-ejs` / `deno` | `python3 -m pip install -U "yt-dlp[default]"` 并安装 `deno` |
| `Fehler: 'yt-dlp' ist nicht installiert.` | 当前使用的 Python 中缺少该模块 | 见[安装 Python 模块](#安装-python-模块) |
| `ffmpeg not found` | ffmpeg 不在 `PATH` 中 | 见[安装 deno 和 ffmpeg](#安装-deno-和-ffmpeg) |
| `externally-managed-environment` | Homebrew Python 的自我保护（PEP 668） | 使用 `--user --break-system-packages` |

YouTube 经常变化——遇到新错误时，更新 yt-dlp 几乎总能解决。


## 项目结构

```
YT-Downloader/
├── main.py                  # 入口：格式、URL、播放列表询问、状态信息
├── downloader/
│   ├── __init__.py
│   ├── core.py              # 公共下载控制（单个视频 vs. 播放列表）
│   ├── playlist.py          # 播放列表识别、读取、并行下载
│   ├── utils.py             # yt-dlp 基础选项、文件名模板、标题清理
│   ├── mp3_downloader.py    # mp3 选项（转换、元数据、封面）
│   └── mp4_downloader.py    # mp4 选项（最佳视频 + 音频）
├── tests/                   # pytest 单元测试（无需网络）
├── Programme/               # 预编译二进制文件（macOS/Linux + Windows）
├── requirements.txt
└── README.md (+ en, fr, tr, zh)
```

流程：`main.py` → `mp3_downloader` / `vid_download` → `core.download` → 单个视频调用 `download_one`，播放列表调用 `fetch_entries` + `download_parallel`。


希望这个程序能帮你摆脱那些满是广告和弹窗的 mp3/mp4 下载器。

作者：
Melih Erbas


## 版本发布

### 未发布
* **修复：** YouTube 上的 `HTTP Error 403`——现在需要 `yt-dlp[default]`（含 JS 验证求解器）和 `deno`。
* **修复：** 即使下载失败也会显示成功信息。
* **新增：** 对播放列表中的视频询问“仅此视频 / 整个播放列表”。
* **新增：** 并行下载播放列表（最多同时 4 个）。
* **新增：** mp3 文件中的元数据和封面。
* **更快：** 不再强制指定播放器客户端（请求更少）。
* **移除：** venv 回退——程序直接运行。
* **新增：** 使用 pytest 的单元测试。

### [v1.0.0](https://github.com/m3linator/YT-Downloader/releases/tag/v1.0.0)
* 第一个版本：mp3/mp4 下载、播放列表编号、干净的文件名、适用于 macOS/Linux 和 Windows 的预编译二进制文件。
