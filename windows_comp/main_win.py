from win_downloader.mp3_downloader_win import mp3_downloader
from win_downloader.mp4_downloader_win import vid_download 
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

    print("\nDein Video wurde erfolgreich heruntergeladen!")
    print("Du findest sie im Download-Ordner")



if __name__ == "__main__":
    main()

