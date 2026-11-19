**Sprache / Language:** [🇩🇪 Deutsch](README.md) | [🇬🇧 English](README.en.md) | 🇫🇷 Français | [🇹🇷 Türkçe](README.tr.md) | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
Un programme en ligne de commande pour télécharger des vidéos (mp4) et de l'audio (mp3) depuis YouTube – sans publicités ni pop-ups.

> Les invites du programme sont en allemand.


## Téléchargement

Des versions pré-compilées sont disponibles sur la **[page des Releases](https://github.com/m3linator/YT-Downloader/releases/latest)** :

| Fichier | Plateforme |
|---------|------------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

> **Remarque :** Les binaires de la v1.0.0 contiennent une version obsolète de yt-dlp et échouent sur de nombreuses vidéos avec `HTTP Error 403`. En attendant une nouvelle release, veuillez [lancer le programme depuis le code source](#exécuter-le-programme).


## Ce que le programme peut faire

Au démarrage, le programme demande le format : **mp3** ou **mp4**. Les mots *Sound, Audio, Stimme, Video et Film* sont également acceptés. Collez ensuite le lien – le téléchargement commence.

Fonctionnalités :

* **Question sur la playlist.** Si une vidéo fait partie d'une playlist (`watch?v=...&list=...`), le programme demande :
  ```
  Der Link gehört zu einer Playlist.
    [1] Nur dieses Video (Standard)     -> uniquement cette vidéo (par défaut)
    [2] Ganze Playlist                  -> toute la playlist
  ```
  Un lien de playlist pur (`playlist?list=...`) télécharge directement toute la playlist.
* **Téléchargements de playlists en parallèle.** Jusqu'à 4 vidéos sont téléchargées simultanément (mesuré : 4 vidéos en 9,8 s au lieu de 25 s). Les vidéos individuelles ne sont pas concernées.
* **Numérotation dans l'ordre de YouTube.** Les fichiers d'une playlist sont nommés `01 - <titre>.mp3`, `02 - <titre>.mp3` … (trois chiffres à partir de 100 vidéos).
* **Métadonnées et pochette dans les mp3.** Le titre, l'artiste et la date sont enregistrés comme tags, et la miniature de la vidéo est intégrée comme pochette – visible dans Apple Music, Spotify (fichiers locaux), VLC, etc.
* **Noms de fichiers propres.** Les préfixes d'artiste et les tags comme *Official Audio*, *Official Video*, *HD*, *Lyrics Video* sont supprimés. Pour les mp3, un `(feat. ...)` est conservé.
* **Les vidéos soumises à une limite d'âge** sont téléchargées dans la mesure où YouTube le permet sans connexion.
* **Message de statut honnête.** Le message de succès n'apparaît que si le téléchargement a réellement réussi. Sinon, le programme liste les vidéos en échec et se termine avec le code `1`. Les vidéos mortes d'une playlist n'arrêtent pas le reste.

Tous les fichiers sont enregistrés dans le dossier Téléchargements de votre utilisateur (`~/Downloads`).


## Prérequis

| Dépendance | Rôle |
|------------|------|
| Python ≥ 3.10 | Exécution du programme |
| `yt-dlp[default]` | Téléchargement ; l'extra `[default]` installe notamment `yt-dlp-ejs` |
| `deno` | Environnement JavaScript utilisé par `yt-dlp-ejs` pour résoudre le challenge de YouTube |
| `ffmpeg` | Conversion mp3, fusion vidéo + audio, intégration de la pochette |

> **Pourquoi `deno` et `yt-dlp-ejs` ?** YouTube protège ses liens de téléchargement par un challenge JavaScript. S'il n'est pas résolu, YouTube répond par `HTTP Error 403: Forbidden`. `deno` est la calculatrice, `yt-dlp-ejs` la fiche de formules – il faut les deux.

### Installer les modules Python

```
python3 -m pip install -U -r requirements.txt
```

Sur macOS avec le Python de Homebrew, pip bloque les installations globales (PEP 668, message `externally-managed-environment`). Installez alors dans votre répertoire utilisateur :
```
python3 -m pip install --user --break-system-packages -U -r requirements.txt
```

### Installer deno et ffmpeg

macOS :
```
brew install deno ffmpeg
```

Linux (Debian/Ubuntu) :
```
sudo apt install ffmpeg
curl -fsSL https://deno.land/install.sh | sh
```

Windows (PowerShell) :
```
winget install DenoLand.Deno
winget install Gyan.FFmpeg
```

Alternative pour ffmpeg sous Windows : téléchargez [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/), décompressez-le et ajoutez le chemin du dossier `bin/` à la variable d'environnement `PATH` (Paramètres → Système → Paramètres système avancés → Variables d'environnement).

Test :
```
deno --version
ffmpeg -version
```


## Exécuter le programme

### Depuis le code source (bare metal)

Le programme s'exécute directement avec le Python du système – aucun environnement virtuel nécessaire :
```
python3 main.py
```
ou (macOS/Linux) :
```
./main.py
```

Exemple :
```
mp3 oder mp4: mp3
Gib die URL von dem YT-Video an:
https://www.youtube.com/watch?v=...
...
1 Datei(en) erfolgreich heruntergeladen!
Du findest sie im Download-Ordner.
```

### Binaires pré-compilés

Windows : double-cliquez sur *main_win.exe*.
macOS/Linux : dans un terminal, allez dans le dossier contenant *main* et exécutez `./main`.
`deno` et `ffmpeg` doivent également être installés.

### Compiler soi-même

```
python3 -m pip install --user pyinstaller
pyinstaller -F --console --collect-data yt_dlp_ejs main.py
```
`--collect-data yt_dlp_ejs` intègre les scripts du solveur dans le binaire. Le résultat se trouve dans `dist/`.


## Tests

Les tests unitaires s'exécutent sans accès réseau (yt-dlp est remplacé par des doublures de test) :
```
python3 -m pytest -q
```


## Dépannage

| Message | Cause | Solution |
|---------|-------|----------|
| `HTTP Error 403: Forbidden` / `n challenge solving failed` | yt-dlp obsolète, ou `yt-dlp-ejs` / `deno` manquant | `python3 -m pip install -U "yt-dlp[default]"` et installer `deno` |
| `Fehler: 'yt-dlp' ist nicht installiert.` | Module absent du Python utilisé | Voir [Installer les modules Python](#installer-les-modules-python) |
| `ffmpeg not found` | ffmpeg absent du `PATH` | Voir [Installer deno et ffmpeg](#installer-deno-et-ffmpeg) |
| `externally-managed-environment` | Le Python de Homebrew se protège (PEP 668) | Utiliser `--user --break-system-packages` |

YouTube change constamment – en cas de nouvelle erreur, mettre à jour yt-dlp aide presque toujours.


## Structure du projet

```
YT-Downloader/
├── main.py                  # Point d'entrée : format, URL, question playlist, message de statut
├── downloader/
│   ├── __init__.py
│   ├── core.py              # pilotage commun du téléchargement (vidéo seule vs. playlist)
│   ├── playlist.py          # détection de playlist, lecture, téléchargement parallèle
│   ├── utils.py             # options de base yt-dlp, modèle de nom de fichier, nettoyage des titres
│   ├── mp3_downloader.py    # options mp3 (conversion, métadonnées, pochette)
│   └── mp4_downloader.py    # options mp4 (meilleure vidéo + audio)
├── tests/                   # tests unitaires pytest (sans réseau)
├── Programme/               # binaires pré-compilés (macOS/Linux + Windows)
├── requirements.txt
└── README.md (+ en, fr, tr, zh)
```

Déroulement : `main.py` → `mp3_downloader` / `vid_download` → `core.download` → pour une vidéo seule `download_one`, pour une playlist `fetch_entries` + `download_parallel`.


J'espère que ce programme t'aidera à éviter tous ces téléchargeurs mp3/mp4 remplis de publicités et de pop-ups.

Auteur :
Melih Erbas


## Releases

### Non publié
* **Corrigé :** `HTTP Error 403` sur YouTube – `yt-dlp[default]` (avec le solveur de challenge JS) et `deno` sont désormais requis.
* **Corrigé :** Le message de succès s'affichait même en cas d'échec.
* **Nouveau :** Question « uniquement cette vidéo / toute la playlist » pour les vidéos d'une playlist.
* **Nouveau :** Téléchargements de playlists en parallèle (jusqu'à 4 simultanément).
* **Nouveau :** Métadonnées et pochette dans les fichiers mp3.
* **Plus rapide :** Plus de clients de lecture imposés (moins de requêtes).
* **Supprimé :** Repli sur venv – le programme s'exécute en bare metal.
* **Nouveau :** Tests unitaires avec pytest.

### [v1.0.0](https://github.com/m3linator/YT-Downloader/releases/tag/v1.0.0)
* Première version : téléchargement mp3/mp4, numérotation des playlists, noms de fichiers propres, binaires pré-compilés pour macOS/Linux et Windows.
