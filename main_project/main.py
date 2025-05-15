import pytube
from pytube import YouTube

def downloader():
    """User gibt YT URL ein und kann dann das Video downloaden"""

    url = input("Gebe die URL deines YouTube-Videos ein: \n" )

    youtube = pytube.YouTube(url)
    video = youtube.streams.get_highest_resolution()            #setzt Streaming-Auflösung
    #video.download('/Dokumente/Privat/Video-Downloads-PY')      #Download Verzeichnis

    video.download()

    print("Dein Video wurde erfolgreich heruntergeladen!")

def main():
    downloader()



if __name__ == "__main__":
    main()



