from features import *
from spotify import *
import os

def loadUserData():
    data = []
    with open("./jsons/user_data.json", "r") as f:
        data = json.load(f)
        f.close()
    return data['artisti_preferiti'], data['artisti_da_ignorare'], data['album_da_ignorare']
        
def modifica_user_data(lista:list):
    print("Dati presenti or ora:")
    print(lista)
    dato = input("Inserire dato da modificare [. per rimuovere dato, ... per annullare]\n")
    if dato == "...":
        return
    if dato == '.':
        dato = input("Inserire dato da rimuovere: ")
        lista.remove(dato)
    else:
        lista.append(dato)

def menu():
    artisti_preferiti, artisti_da_ignorare, album_da_ignorare = loadUserData()
    scelta = -1
    while scelta != '0':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("0. Fine esecuzione programma")
        print("1. Mischiare una playlist")
        print("2. Rimuovere tutte le playlist che condividono nome")
        print("3. Gestisci gruppi")
        scelta = input("Quale opzione si vuole scegliere?\n")
        if scelta == '1':
            playlist = input("Inserire nome playlist da mischiare: ")
            modificare = input("Si vuole modificare qualche arista/album da ignorare o qualche artista preferito? [y/n]\n")
            if modificare == 'y':
                opzione = -1
                while opzione != '0':
                    print("0. Ho cambiato idea!")
                    print("1. Artista preferito")
                    print("2. Artista da ignorare")
                    print("3. Album da ignorare")
                    opzione = input("Quale azione vuole compiere?\n")
                    if opzione == '1':
                        modifica_user_data(artisti_preferiti)
                    elif opzione == '2':
                        modifica_user_data(artisti_da_ignorare)
                    elif opzione == '3':
                        modifica_user_data(album_da_ignorare)
                with open("./jsons/user_data.json", "w") as f:
                    json.dump(
                            {   
                                "artisti_preferiti": artisti_preferiti,
                                "artisti_da_ignorare": artisti_da_ignorare,
                                "album_da_ignorare": album_da_ignorare
                            }, f, ensure_ascii=False, indent=4
                        )
            mischia_playlist(playlist, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify)
        elif scelta == '2':
            playlist = input("Inserire nome playlist da cancellare: ")
            remove_same_name(spotify, playlist)
        elif scelta == '3':
            gruppi_manager()
        else:
            if scelta != '0':
                print("Input non riconosciuto. Riprova.")
            else:
                input("Press Enter to continue...")


if __name__ == "__main__":
    spotify = Spotify()
    playlists = spotify.fetch_data()
    menu()