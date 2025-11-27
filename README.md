# YT-Downloader
Ein Programm mit dem man Videos von YouTube herunterladen kann 

Das Programm ist bereits fertig gebaut und kann im Ordner 'Programme/' heruntergeladen werden.  
*main* ist kompatibel mit macOS und Linux und *main_win.exe* mit Windows.


## Weitere Beschreibung:

Wenn man das Programm startet, wird einem die Auswahl zwischen mp3 und mp4 angeboten. Durch simples eingeben wird die Auswahl gespeichert. Begriffe wie *Sound, Audio, Stimme, Video und Film* werden ebenfalls akzeptiert. 
Danach muss man nur noch den Link vom gewünschten YouTube-Video einfügen und der Download beginnt.
Ganze YouTube-Playlists können ebenfalls heruntergeladen werden. Dafür muss man den Link beim ersten Video der Playlist kopieren. D.h. wenn man nicht beim ersten Video der Playlist ist, wird nur das jeweilige Video heruntergeladen, anstatt der gesamten Playlist.



### Anforderungen für das Programm

Um das Programm zu starten, muss man drei Module herunterladen.
* numpy
* yt-dlp
* ffmpeg

Wenn man diese bereits heruntergeladen hat, kann man das Programm ganz einfach wie unten beschrieben starten.

Wenn nicht, muss man diese erstmal herunterladen.



*NumPy* und *yt-dlp* können ganz einfach mit pip installiert werden (Win/Mac/Linux):
````
pip install numpy yt-dlp
````
Falls das nicht funktioniert, versuche:
````
python3 -m pip install numpy yt-dlp
````

### ffmpeg Download   

Wenn diese beiden Module installiert sind, fehlt nur noch ffmpeg. Auf macOS und Linux ist der Download ziemlich einfach. 
Gehe dazu ins Terminal und gebe folgenden Befehl ein:  
````
[paketmanager] install ffmpeg
````

Auf Windows ist der Download von *ffmpeg* etwas umständlicher

Dafür musst du erstmal von der ffmpeg Seite die [ffmpeg-release-essentials.zip](https://www.gyan.dev/ffmpeg/builds/) herunterladen. Wenn du das erledigt hast, führe folgende Schritte durch:
  1. Datei entpacken, in den Ordner 'bin/' navigieren und dessen Pfad-Link kopieren.
  2. Öffne die Einstellungen &rarr; System &rarr; erweiterte Systemeinstellungen
  3. Klicke auf Umgebungsvariable
  4. Bearbeite die Variable PATH &rarr; Neu &rarr; füge kopierten Pfad ein

Um zu testen ob alles geklappt hat, öffne Powershell und gib folgendes ein:
```
ffmpeg -version
```
Wenn alles geklappt hat, siehtst du die installierte Version.


# Programm ausführen

Auf Windows reicht es auf die *main_win.exe* Datei eine Doppel-Klick zu machen. Dadurch öffnet sich automatisch ein neues Terminal-Fenster und du kannst wie oben beschrieben fortfahren.

Auf macOS musst du ein neues Terminal-Fenster öffnen und in den Pfad navigieren, in dem die Datei *main* gespeichert ist. Danach führst du folgenden Befehl aus, um das Programm zu starten:
````
./main
````


Falls du das Programm selber bauen möchtest, zum Beispiel um nach einem Code-Update die neueste Version zu haben, kannst du es mit folgendem Befehl tun. 
````
pyinstaller -F --console main.py
````

> main.py oder main_win.py je nach Platform



Autor:
Melih Erbas
