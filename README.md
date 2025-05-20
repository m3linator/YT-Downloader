# YT-Downloader
Ein Programm mit dem man Videos von YouTube herunterladen kann 

Das Programm ist bereits fertig gebaut und kann im Ordner 'Programme/' heruntergeladen werden.  
*main* ist kompatibel mit macOS und *main_win.exe* mit Windows

## Weitere Beschreibung:

Wenn man das Programm starte, wird einem die Auswahl zwischen mp3 und mp4 angeboten. Durch simples Eingeben wird die Auswahl gespeichert. Begriffe wie *Sound, Audio, Stimme, Video und Film* werden ebenfalls akzeptiert. 
Danach muss man nur noch den Link vom gewünschten YouTube-Video einfügen und der Download beginnt.

### Wie starte ich das Programm?
Auf Windows reicht es auf die *main_win.exe* Datei eine Doppel-Klick zu machen. Dadurch öffnet sich automatisch ein neues Terminal-Fenster und du kannst wie oben beschrieben fortfahren

Auf macOS musst du ein neues Terminal-Fenster öffnen und in den Pfad navigieren, in dem die Datei *main* gespeichert ist. Danach führst du folgenden Befehl aus, um das Programm zu starten:
````
./main
````


## Anforderungen um Programm selber zu bauen

Damit man das Programm ausführen kann, wenn man es selber bauen möchte (also nicht die fertige exe verwenden möchte),  
muss man einige Module herunterladen.  
Diese sind: 
* numpy
* yt-dlp
* ffmpeg

*NumPy* und *yt-dlp* können ganz einfach mit pip installiert werden:
````
pip install numpy yt-dlp
````
Falls das nicht funktioniert, versuche:
````
python3 -m pip install numpy yt-dlp
````

### ffmpeg Download   

Wenn diese beiden Module installiert sind, fehlt nur noch ffmpeg. Auf macOS ist der Download ziemlich einfach. 
Gehe dazu ins Terminal und gebe folgenden Befehl ein  
````
brew install ffmpeg
````

Aus Windows ist der Download etwas umständlicher




Um die Datei zu bauen:
````
pyinstaller -F --console main.py
````


> main.py oder main_win.py je nach Platform



Autor:
...
...
