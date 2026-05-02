**Dil:** [🇩🇪 Deutsch](README.md) | [🇬🇧 English](README.en.md) | [🇫🇷 Français](README.fr.md) | 🇹🇷 Türkçe | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
YouTube'dan video ve ses indirmeye yarayan bir program.

Program zaten önceden derlenmiş olup `Programme/` klasöründen indirilebilir.
*main* macOS ve Linux ile, *main_win.exe* ise Windows ile uyumludur.


## Programın Özellikleri

Programı başlattığınızda mp3 ile mp4 arasında seçim yapmanız istenir. Seçiminizi yazarak onaylayabilirsiniz. *ses, audio, video, film* gibi kelimeler de kabul edilir.
Ardından istediğiniz YouTube videosunun bağlantısını yapıştırmanız yeterlidir; indirme otomatik olarak başlar.

Ek özellikler:

* **Çalma listeleri sırayla numaralandırılır.** Bir çalma listesi bağlantısı yapıştırırsanız dosyalar, YouTube'daki sıraya göre iki basamaklı ön ekle adlandırılır; ör. `01 - <başlık>.mp3`, `02 - <başlık>.mp3` …
* **Yaş kısıtlı / "müstehcen" videolar** (ör. bazı rap parçaları) giriş yapmaya gerek kalmadan indirilir.
* **Temiz dosya adları.** Sanatçı ön ekleri ve *Official Audio*, *Official Video*, *HD*, *Lyrics Video* gibi etiketler dosya adından otomatik olarak kaldırılır. Mp3 indirmelerinde varsa `(feat. ...)` kısmı korunur.
* **Erişilemeyen videolara karşı dayanıklı.** Bir çalma listesindeki artık mevcut olmayan veya bölgesel olarak engellenen videolar sessizce atlanır; böylece indirme işlemi yarıda kalmaz.

Tüm dosyalar, kullanıcı hesabınızın varsayılan İndirilenler klasörüne kaydedilir.


## Gereksinimler

Yalnızca bir modül ve `ffmpeg` gereklidir:

* `yt-dlp`
* `ffmpeg`

`yt-dlp` kurulumu (Win/Mac/Linux):
```
pip install -r requirements.txt
```
ya da doğrudan:
```
pip install yt-dlp
```
Bu işe yaramazsa:
```
python3 -m pip install yt-dlp
```

### ffmpeg İndirme

macOS / Linux'ta paket yöneticisiyle:
```
[paket-yöneticisi] install ffmpeg
```
ör. `brew install ffmpeg` veya `sudo apt install ffmpeg`.

Windows'ta *ffmpeg* kurulumu biraz daha zahmetlidir.
ffmpeg sitesinden [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) dosyasını indirin ve şu adımları uygulayın:
  1. Dosyayı çıkartın, `bin/` klasörüne gidin ve klasörün yolunu kopyalayın.
  2. Ayarlar → Sistem → Gelişmiş sistem ayarları'nı açın.
  3. Ortam Değişkenleri'ne tıklayın.
  4. PATH değişkenini düzenleyin → Yeni → kopyaladığınız yolu yapıştırın.

PowerShell'de test edin:
```
ffmpeg -version
```


## Programı Çalıştırma

### Bare Metal (venv aktivasyonu olmadan)

`yt-dlp` ve `ffmpeg` sistem genelinde kurulduktan sonra betik, sanal ortam etkinleştirmeye gerek kalmadan doğrudan sistem Python'ıyla çalıştırılabilir:

```
python3 main.py
```

ya da doğrudan çalıştırılabilir (macOS/Linux):

```
./main.py
```

### Önceden Derlenmiş İkili Dosyalar

Windows'ta *main_win.exe* dosyasına çift tıklamanız yeterlidir. Terminal penceresi otomatik olarak açılır.

macOS/Linux'ta bir terminal açın, *main* dosyasının bulunduğu klasöre gidin ve şunu çalıştırın:
```
./main
```

### Kendiniz Derleyin

Bir kod güncellemesinden sonra programı yeniden derlemek isterseniz:
```
pyinstaller -F --console main.py
```


## Proje Yapısı

```
YT-Downloader/
├── main.py                       # Giriş noktası (mp3/mp4 + URL sorgusu)
├── downloader/
│   ├── __init__.py
│   ├── utils.py                  # paylaşılan yt-dlp seçenekleri + başlık temizleyici
│   ├── mp3_downloader.py
│   └── mp4_downloader.py
├── requirements.txt
├── Programme/                    # önceden derlenmiş ikili dosyalar (macOS/Linux + Windows)
└── README.md
```


Umarım bu program, reklam ve pop-up dolu mp3/mp4 indirici sitelerden kurtulmanıza yardımcı olur.

Yazar:
Melih Erbas
