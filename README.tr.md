**Sprache / Language:** [🇩🇪 Deutsch](README.md) | [🇬🇧 English](README.en.md) | [🇫🇷 Français](README.fr.md) | 🇹🇷 Türkçe | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
YouTube'dan video (mp4) ve ses (mp3) indirmek için bir komut satırı programı – reklamsız ve açılır pencere olmadan.

> Programın komut istemleri Almancadır.


## İndirme

Önceden derlenmiş sürümler **[Releases sayfasında](https://github.com/m3linator/YT-Downloader/releases/latest)** bulunur:

| Dosya | Platform |
|-------|----------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

> **Not:** v1.0.0 ikili dosyaları eski bir yt-dlp sürümü içerir ve birçok videoda `HTTP Error 403` hatası verir. Yeni bir sürüm çıkana kadar lütfen [programı kaynak koddan çalıştırın](#programı-çalıştırma).


## Programın Özellikleri

Program başlarken formatı sorar: **mp3** veya **mp4**. *Sound, Audio, Stimme, Video ve Film* gibi kelimeler de kabul edilir. Ardından bağlantıyı yapıştırın – indirme başlar.

Özellikler:

* **Oynatma listesi sorusu.** Bir video bir oynatma listesinin parçasıysa (`watch?v=...&list=...`), program sorar:
  ```
  Der Link gehört zu einer Playlist.
    [1] Nur dieses Video (Standard)     -> sadece bu video (varsayılan)
    [2] Ganze Playlist                  -> tüm oynatma listesi
  ```
  Saf bir oynatma listesi bağlantısı (`playlist?list=...`) doğrudan tüm listeyi indirir.
* **Paralel oynatma listesi indirme.** Aynı anda en fazla 4 video indirilir (ölçüm: 4 video 25 s yerine 9,8 s). Tek videolar bundan etkilenmez.
* **YouTube sırasına göre numaralandırma.** Oynatma listesi dosyaları `01 - <başlık>.mp3`, `02 - <başlık>.mp3` … şeklinde adlandırılır (100 videodan itibaren üç haneli).
* **mp3'lerde meta veriler ve kapak.** Başlık, sanatçı ve tarih etiket olarak kaydedilir, video küçük resmi kapak olarak gömülür – Apple Music, Spotify (yerel dosyalar), VLC vb. uygulamalarda görünür.
* **Temiz dosya adları.** Sanatçı önekleri ve *Official Audio*, *Official Video*, *HD*, *Lyrics Video* gibi etiketler kaldırılır. mp3'lerde `(feat. ...)` korunur.
* **Yaş sınırlı videolar**, YouTube'un giriş yapmadan izin verdiği ölçüde indirilir.
* **Dürüst durum mesajı.** Başarı mesajı yalnızca indirme gerçekten başarılı olduğunda görünür. Aksi halde program başarısız videoları listeler ve `1` çıkış koduyla sonlanır. Listedeki ölü videolar diğerlerini durdurmaz.

Tüm dosyalar kullanıcınızın İndirilenler klasörüne (`~/Downloads`) kaydedilir.


## Gereksinimler

| Bağımlılık | Amaç |
|------------|------|
| Python ≥ 3.10 | Programı çalıştırmak |
| `yt-dlp[default]` | İndirme; `[default]` eki diğerlerinin yanında `yt-dlp-ejs`'i de kurar |
| `deno` | `yt-dlp-ejs`'in YouTube challenge'ını çözmek için kullandığı JavaScript çalışma ortamı |
| `ffmpeg` | mp3 dönüştürme, video + ses birleştirme, kapak gömme |

> **Neden `deno` ve `yt-dlp-ejs`?** YouTube indirme bağlantılarını bir JavaScript challenge'ı ile korur. Çözülmezse YouTube `HTTP Error 403: Forbidden` ile yanıt verir. `deno` hesap makinesi, `yt-dlp-ejs` formül kâğıdıdır – ikisine de ihtiyaç vardır.

### Python modüllerini kurma

```
python3 -m pip install -U -r requirements.txt
```

macOS'ta Homebrew Python kullanılıyorsa pip global kurulumları engeller (PEP 668, `externally-managed-environment` mesajı). Bu durumda kullanıcı dizinine kurun:
```
python3 -m pip install --user --break-system-packages -U -r requirements.txt
```

### deno ve ffmpeg kurma

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

Alternatif olarak Windows'ta ffmpeg'i elle kurmak için: [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) dosyasını indirin, çıkarın ve `bin/` klasörünün yolunu `PATH` ortam değişkenine ekleyin (Ayarlar → Sistem → Gelişmiş sistem ayarları → Ortam Değişkenleri).

Test:
```
deno --version
ffmpeg -version
```


## Programı Çalıştırma

### Kaynak koddan (bare metal)

Program doğrudan sistem Python'u ile çalışır – sanal ortam gerekmez:
```
python3 main.py
```
veya (macOS/Linux):
```
./main.py
```

Örnek:
```
mp3 oder mp4: mp3
Gib die URL von dem YT-Video an:
https://www.youtube.com/watch?v=...
...
1 Datei(en) erfolgreich heruntergeladen!
Du findest sie im Download-Ordner.
```

### Önceden Derlenmiş İkili Dosyalar

Windows: *main_win.exe* dosyasına çift tıklayın.
macOS/Linux: Terminalde *main* dosyasının bulunduğu klasöre gidin ve `./main` komutunu çalıştırın.
Burada da `deno` ve `ffmpeg` kurulu olmalıdır.

### Kendiniz Derleyin

```
python3 -m pip install --user pyinstaller
pyinstaller -F --console --collect-data yt_dlp_ejs main.py
```
`--collect-data yt_dlp_ejs`, çözücü betiklerini ikili dosyaya ekler. Sonuç `dist/` klasöründedir.


## Testler

Birim testleri ağ erişimi olmadan çalışır (yt-dlp test dublörleriyle değiştirilir):
```
python3 -m pytest -q
```


## Sorun Giderme

| Mesaj | Neden | Çözüm |
|-------|-------|-------|
| `HTTP Error 403: Forbidden` / `n challenge solving failed` | yt-dlp eski veya `yt-dlp-ejs` / `deno` eksik | `python3 -m pip install -U "yt-dlp[default]"` ve `deno` kurun |
| `Fehler: 'yt-dlp' ist nicht installiert.` | Kullanılan Python'da modül yok | Bkz. [Python modüllerini kurma](#python-modüllerini-kurma) |
| `ffmpeg not found` | ffmpeg `PATH` içinde değil | Bkz. [deno ve ffmpeg kurma](#deno-ve-ffmpeg-kurma) |
| `externally-managed-environment` | Homebrew Python kendini korur (PEP 668) | `--user --break-system-packages` kullanın |

YouTube sürekli değişir – yeni hatalarda yt-dlp'yi güncellemek neredeyse her zaman işe yarar.


## Proje Yapısı

```
YT-Downloader/
├── main.py                  # Giriş noktası: format, URL, oynatma listesi sorusu, durum mesajı
├── downloader/
│   ├── __init__.py
│   ├── core.py              # ortak indirme kontrolü (tek video ve oynatma listesi)
│   ├── playlist.py          # oynatma listesi algılama, okuma, paralel indirme
│   ├── utils.py             # yt-dlp temel seçenekleri, dosya adı şablonu, başlık temizleme
│   ├── mp3_downloader.py    # mp3 seçenekleri (dönüştürme, meta veri, kapak)
│   └── mp4_downloader.py    # mp4 seçenekleri (en iyi video + ses)
├── tests/                   # pytest birim testleri (ağ olmadan)
├── Programme/               # önceden derlenmiş ikili dosyalar (macOS/Linux + Windows)
├── requirements.txt
└── README.md (+ en, fr, tr, zh)
```

Akış: `main.py` → `mp3_downloader` / `vid_download` → `core.download` → tek videoda `download_one`, oynatma listesinde `fetch_entries` + `download_parallel`.


Umarım bu program, reklam ve açılır pencerelerle dolu tüm o mp3/mp4 indiricilerden kurtulmana yardımcı olur.

Yazar:
Melih Erbas


## Sürümler

### Yayınlanmamış
* **Düzeltildi:** YouTube'da `HTTP Error 403` – artık `yt-dlp[default]` (JS challenge çözücü dahil) ve `deno` gereklidir.
* **Düzeltildi:** Başarı mesajı, indirme başarısız olsa bile görünüyordu.
* **Yeni:** Oynatma listesindeki videolar için „sadece bu video / tüm liste“ sorusu.
* **Yeni:** Paralel oynatma listesi indirme (aynı anda en fazla 4).
* **Yeni:** mp3 dosyalarında meta veriler ve kapak.
* **Daha hızlı:** Artık zorunlu oynatıcı istemcileri yok (daha az istek).
* **Kaldırıldı:** venv yedeği – program bare metal çalışır.
* **Yeni:** pytest ile birim testleri.

### [v1.0.0](https://github.com/m3linator/YT-Downloader/releases/tag/v1.0.0)
* İlk sürüm: mp3/mp4 indirme, oynatma listesi numaralandırma, temiz dosya adları, macOS/Linux ve Windows için önceden derlenmiş ikili dosyalar.
