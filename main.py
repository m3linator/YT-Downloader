from downloader.mp4_downloader import vid_download
from downloader.mp3_downloader import mp3_downloader
from numpy import array


audio = ["mp3", "sound", "audio", "stimme"]
video = ["mp4", "video", "film"]


def main():

    format = input('mp3 oder mp4: ')
    link = input("Gib die URL von dem YT-Video an: \n")

    if format.lower() in video:
        vid_download(link)
    elif format.lower() in audio:
        mp3_downloader(link)
    else:
        print("Dieses Format wird nicht unterstütz!!!")
        return

    print("\n Dein Video wurde erfolgreich heruntergeladen!")
    print(" Du findest es bei /Documents/Privat/Video-Downloads-PY")




if __name__ == "__main__":
    main()

