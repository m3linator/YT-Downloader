**语言：** [🇩🇪 Deutsch](README.md) | [🇬🇧 English](README.en.md) | [🇫🇷 Français](README.fr.md) | [🇹🇷 Türkçe](README.tr.md) | 🇨🇳 中文

---

# YT-Downloader
一个从 YouTube 下载视频和音频的程序。

程序已预先编译，可在 `Programme/` 文件夹中下载。
*main* 兼容 macOS 和 Linux，*main_win.exe* 兼容 Windows。


## 程序功能

启动程序后，系统会提示您选择 mp3 或 mp4。直接输入您的选择即可确认。*声音、音频、语音、视频、电影* 等词汇同样被接受。
之后只需粘贴所需 YouTube 视频的链接，下载即自动开始。

附加功能：

* **播放列表按顺序编号。** 粘贴播放列表链接时，文件将按 YouTube 中的确切顺序以两位数前缀命名，例如 `01 - <标题>.mp3`、`02 - <标题>.mp3` ……
* **年龄限制 / "限制级" 视频**（如某些说唱歌曲）无需登录即可下载。
* **干净的文件名。** 艺术家前缀及 *Official Audio*、*Official Video*、*HD*、*Lyrics Video* 等标签会自动从文件名中移除。对于 mp3 下载，`(feat. ...)` 部分将予以保留。
* **对失效视频具有鲁棒性。** 播放列表中不再可用或受地区限制的视频将被静默跳过，不会中断下载。

所有文件均保存至您用户账户的默认下载文件夹。


## 环境要求

仅需一个模块和 `ffmpeg`：

* `yt-dlp`
* `ffmpeg`

安装 `yt-dlp`（Win/Mac/Linux）：
```
pip install -r requirements.txt
```
或直接安装：
```
pip install yt-dlp
```
如果上述方法不奏效：
```
python3 -m pip install yt-dlp
```

### 下载 ffmpeg

在 macOS / Linux 上使用包管理器：
```
[包管理器] install ffmpeg
```
例如 `brew install ffmpeg` 或 `sudo apt install ffmpeg`。

在 Windows 上安装 *ffmpeg* 稍显繁琐。
请从 ffmpeg 网站下载 [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/)，然后按以下步骤操作：
  1. 解压文件，进入 `bin/` 文件夹，复制其路径。
  2. 打开 设置 → 系统 → 高级系统设置。
  3. 点击 环境变量。
  4. 编辑 PATH 变量 → 新建 → 粘贴复制的路径。

在 PowerShell 中测试：
```
ffmpeg -version
```


## 运行程序

### 直接运行（无需激活 venv）

`yt-dlp` 和 `ffmpeg` 在系统范围内安装完成后，可直接使用系统 Python 运行脚本，无需提前激活虚拟环境：

```
python3 main.py
```

或直接执行（macOS/Linux）：

```
./main.py
```

### 使用预编译二进制文件

在 Windows 上，双击 *main_win.exe* 文件即可，终端窗口将自动打开。

在 macOS/Linux 上，打开终端，切换到包含 *main* 文件的目录，然后运行：
```
./main
```

### 自行编译

如果您想在代码更新后重新编译程序：
```
pyinstaller -F --console main.py
```


## 项目结构

```
YT-Downloader/
├── main.py                       # 入口点（mp3/mp4 + URL 输入）
├── downloader/
│   ├── __init__.py
│   ├── utils.py                  # 共享的 yt-dlp 选项 + 标题清理器
│   ├── mp3_downloader.py
│   └── mp4_downloader.py
├── requirements.txt
├── Programme/                    # 预编译二进制文件（macOS/Linux + Windows）
└── README.md
```


希望这个程序能帮助您摆脱那些充斥着广告和弹窗的 mp3/mp4 下载网站。

作者：
Melih Erbas
