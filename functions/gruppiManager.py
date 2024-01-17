import json

def loadUserData():
    data = []
    with open("./jsons/user_data.json", "r") as f:
        data = json.load(f)
        f.close()
    return data['gruppi']

def updateUserData(key, value, daAggiungere = True):
    data = []
    with open("./jsons/user_data.json", "r") as f:
        data = json.load(f)
        f.close()
    if daAggiungere:
        data['gruppi'].append({key:value})
    else:
        for i, g in enumerate(value):
            if list(g.keys())[0] == key:
                data['gruppi'].remove(value[i])
    with open("./jsons/user_data.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()

def join(gruppi:list):
    if len(gruppi) < 2:
        print("Numero di gruppi insufficienti, inserirne almeno due.\n")
        return
    joined_list = {'test'}
    for g in gruppi:
        print(g)
        # print(type(g))
        # joined_list.update(g.values())
    # print(joined_list)

def manager():
    scelta = ""
    while scelta != '...':
        nome = ""
        scelta = input("Vuole aggiungere, rimuovere, modificare gruppo o fare join? [a/r/m/j] [... per uscire]")
        if scelta == 'a':
            nome = input("Nome gruppo: ")
            gruppi_selezionati = []
            gruppo = input("Inserire dato: [... per uscire]\n")
            while gruppo != '...':
                gruppi_selezionati.append(gruppo)
                gruppo = input("Inserire dato: [... per uscire]\n")
            updateUserData(nome, gruppi_selezionati)

        elif scelta == 'r':
            gruppi = loadUserData()
            print("Gruppi disponibili: ")
            for g in gruppi:
                print("\t"+list(g.keys())[0], end="\n")
            gruppo = input("\nInserire nome del gruppo da rimuovere [... per uscire]\n")
            if gruppo == '...':
                break
            updateUserData(gruppo, gruppi, False)

        elif scelta == 'm':
            gruppi = loadUserData()
            print("Gruppi disponibili:")
            for g in gruppi:
                print("\t"+list(g.keys())[0], end="\n")
        
        elif scelta == 'j':
            gruppi = loadUserData()
            print("Gruppi disponibili: ")
            for g in gruppi:
                print("\t"+list(g.keys())[0], end="\n")

            gruppi_selezionati = []
            gruppo = input("Inserire gruppo: [... per uscire]\n")
            while gruppo != '...':
                for g in gruppi:
                    if list(g.keys())[0] == gruppo:
                        gruppi_selezionati.append(g)
                        break
                gruppo = input("Inserire gruppo: [... per uscire]\n")
            join(gruppi_selezionati)
        
        elif scelta != '...':
            print("Input non valido. Riprova.")
    
