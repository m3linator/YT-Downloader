**Langue :** [🇩🇪 Deutsch](README.md) | [🇬🇧 English](README.en.md) | 🇫🇷 Français | [🇹🇷 Türkçe](README.tr.md) | [🇨🇳 中文](README.zh.md)

---

# YT-Downloader
Un programme pour télécharger des vidéos et de l'audio depuis YouTube.

Le programme est déjà pré-compilé et disponible en tant que **[Release](https://github.com/m3linator/YT-Downloader/releases/latest)**.
*main* est compatible avec macOS et Linux, et *main_win.exe* avec Windows.


## Téléchargement

Obtenez la dernière version directement depuis la **[page Releases](https://github.com/m3linator/YT-Downloader/releases/latest)** :

| Fichier | Plateforme |
|---------|------------|
| `main` | macOS / Linux |
| `main_win.exe` | Windows |

Les binaires sont autonomes — aucune installation de Python requise. Seul `ffmpeg` doit être installé séparément (voir [Prérequis](#prérequis)).


## Ce que le programme peut faire

Au démarrage, le programme vous propose de choisir entre mp3 et mp4. Il suffit de taper votre choix pour le valider. Des termes comme *son, audio, voix, vidéo* et *film* sont également acceptés.
Ensuite, il ne reste plus qu'à coller le lien de la vidéo YouTube souhaitée et le téléchargement commence.

Fonctionnalités supplémentaires :

* **Les playlists sont numérotées dans l'ordre.** En collant un lien de playlist, les fichiers sont nommés dans l'ordre exact de YouTube avec un préfixe à deux chiffres, p. ex. `01 - <titre>.mp3`, `02 - <titre>.mp3` …
* **Les vidéos avec restriction d'âge / « explicites »** (p. ex. certains morceaux de rap) sont téléchargées sans connexion requise.
* **Noms de fichiers propres.** Les préfixes d'artiste et les balises telles que *Official Audio*, *Official Video*, *HD*, *Lyrics Video*, etc. sont automatiquement supprimés du nom de fichier. Pour les téléchargements mp3, un éventuel `(feat. ...)` est conservé.
* **Robuste face aux vidéos indisponibles.** Les vidéos d'une playlist qui ne sont plus disponibles ou sont bloquées géographiquement sont silencieusement ignorées afin que le téléchargement ne s'interrompe pas.

Tous les fichiers sont enregistrés dans le dossier Téléchargements standard de votre compte utilisateur.


## Prérequis

Un seul module + `ffmpeg` est nécessaire :

* `yt-dlp`
* `ffmpeg`

Installation de `yt-dlp` (Win/Mac/Linux) :
```
pip install -r requirements.txt
```
ou directement :
```
pip install yt-dlp
```
Si cela ne fonctionne pas :
```
python3 -m pip install yt-dlp
```

### Téléchargement de ffmpeg

Sur macOS / Linux avec un gestionnaire de paquets :
```
[gestionnaire-de-paquets] install ffmpeg
```
p. ex. `brew install ffmpeg` ou `sudo apt install ffmpeg`.

Sur Windows, l'installation de *ffmpeg* est un peu plus fastidieuse.
Téléchargez [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) depuis le site de ffmpeg et suivez ces étapes :
  1. Décompressez le fichier, naviguez dans le dossier `bin/` et copiez son chemin.
  2. Ouvrez Paramètres → Système → Paramètres système avancés.
  3. Cliquez sur Variables d'environnement.
  4. Modifiez la variable PATH → Nouveau → collez le chemin copié.

Test dans PowerShell :
```
ffmpeg -version
```


## Exécuter le programme

### Bare Metal (sans activation de venv)

Une fois `yt-dlp` et `ffmpeg` installés à l'échelle du système, le script peut être lancé directement avec le Python système — sans avoir à activer un environnement virtuel au préalable :

```
python3 main.py
```

ou directement exécutable (macOS/Linux) :

```
./main.py
```

### Binaires pré-compilés

Sur Windows, il suffit de double-cliquer sur le fichier *main_win.exe*. Une fenêtre de terminal s'ouvre automatiquement.

Sur macOS/Linux, ouvrez un terminal, naviguez jusqu'au dossier contenant *main* et exécutez :
```
./main
```

### Compiler soi-même

Si vous souhaitez recompiler le programme après une mise à jour du code :
```
pyinstaller -F --console main.py
```


## Structure du projet

```
YT-Downloader/
├── main.py                       # Point d'entrée (choix mp3/mp4 + URL)
├── downloader/
│   ├── __init__.py
│   ├── utils.py                  # options yt-dlp partagées + nettoyeur de titres
│   ├── mp3_downloader.py
│   └── mp4_downloader.py
├── requirements.txt
├── Programme/                    # binaires pré-compilés (macOS/Linux + Windows)
└── README.md
```


J'espère que ce programme vous aidera à éviter tous ces téléchargeurs mp3/mp4 remplis de publicités et de pop-ups.

Auteur :
Melih Erbas
