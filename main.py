from features import *
from spotify import *

def loadUserData():
    data = []
    with open("./jsons/settings.json", "r") as f:
        data = json.load(f)
    return data['artisti_preferiti'], data['artisti_da_ignorare'], data['album_da_ignorare']
        
def modifica_user_data(lista:list):
    if len(lista) != 0:
        print("Dati presenti:")
        print(lista)
    else:
        print("Nessun dato presente.")

    dato = input("Inserire dato da modificare [. per rimuovere dato, ... per annullare]\n")
    if dato == "...":
        return
    if dato == '.':
        dato = input("Inserire dato da rimuovere: ")
        #todo controllare se dato è presente sia in ignora che in preferisci
        #todo controllare se dato è stato trovato, altrimetni dare errore
        lista.remove(dato)
    else:
        lista.append(dato)

def menu_settings(artisti_preferiti, artisti_da_ignorare, album_da_ignorare):
    opzione = -1
    while opzione != '0':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("0. Torna al menù precedente")
        print("1. Aggiungi o rimuovi un artista preferito")
        print("2. Aggiungi o rimuovi un artista da ignorare")
        #todo print("3. Aggiungi o rimuovi un album preferito")
        print("3. Aggiungi o rimuovi un album da ignorare")
        opzione = input("Quale azione si vuole compiere?\n")
        if opzione == '1':
            modifica_user_data(artisti_preferiti)
        elif opzione == '2':
            modifica_user_data(artisti_da_ignorare)
        elif opzione == '3':
            modifica_user_data(album_da_ignorare)
    with open("./jsons/settings.json", "w") as f:
        json.dump({   
                    "artisti_preferiti": artisti_preferiti,
                    "artisti_da_ignorare": artisti_da_ignorare,
                    "album_da_ignorare": album_da_ignorare
                }, f, ensure_ascii=False, indent=4
            )

def menu():
    artisti_preferiti, artisti_da_ignorare, album_da_ignorare = loadUserData()
    playlist = input("Inserire nome playlist da mischiare: ")
    modificare = input("Si vuole modificare qualche arista/album da ignorare o qualche artista preferito? [y/n]\n")
    if modificare == 'y':
        menu_settings(artisti_preferiti, artisti_da_ignorare, album_da_ignorare)
    mischia_playlist(playlist, album_da_ignorare, artisti_da_ignorare, artisti_preferiti, playlists, spotify)



if __name__ == "__main__":
    spotify = Spotify()
    playlists = spotify.fetch_data()
    menu()