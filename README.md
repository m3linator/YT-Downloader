# YT-Downloader
Ein Programm mit dem man Videos von YouTube herunterladen kann 

Das Programm ist bereits fertig gebaut und kann im Ordner 'Programme/' heruntergeladen werden.  
*main* ist kompatibel mit macOS und *main_win.exe* mit Windows

## Weitere Beschreibung:

Wenn man das Programm starte, wird einem die Auswahl zwischen mp3 und mp4 angeboten. Durch simples Eingeben wird die Auswahl gespeichert. Begriffe wie *sound, audio, stimme, video und film* werden ebenfalls akzeptiert. 
Danach muss man nur noch den Link vom gewünschten YouTube-Video einfügen und der Download beginnt.

### Wie starte ich das Programm?
Auf Windows reicht es auf die *main_win.exe* Datei eine Doppel-Klick zu machen. Dadurch öffnet sich automatisch ein neues Terminal-Fenster und du kannst wie oben beschrieben fortfahren

Auf macOS musst du ein neues Terminal-Fenster öffnen und in den Pfad navigieren, in dem die Datei *main* gespeichert ist. Danach führst du folgenden Befehl aus, um das Programm zu starten:
````
./main
````


## Anforderungen um Programm selber zu bauen

weitere Anforderungen:
...
...
...


Download auf MacOS:
````
brew install ffmpeg
````


Um die Datei zu bauen:
````
pyinstaller -F --console main.py
````


> main.py oder main_win.py je nach Platform



Autor:
...
...
