import main_project
from main_project.downloader import vid_download


def main():

    link = input("Gib die URL von dem YT-Video an: \n")
    vid_download(link)
    print("\n Dein Video wurde erfolgreich heruntergeladen!")
    print(" Du findest es bei /Documents/Privat/Video-Downloads-PY")

if __name__ == "__main__":
    main()

