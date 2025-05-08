#import
import questionary
import json
import os
from colorama import init, Fore, Style
init(autoreset=True)

#Öffne JSON File mit Items
#Pfad des Scriptes herausfinden
script_dir = os.path.dirname(os.path.abspath(__file__))
#Absoluten Dateipfad erstellen
file_path = os.path.join(script_dir, 'itemList.json')
#Falls die Datei vorhanden ist - öffne sie
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        itemList = json.load(file)
#Falls die Datei nicht vorhanden ist - erstelle sie
else:
    itemList = {"items": []}
    with open(file_path, "w") as file:
        json.dump(itemList, file, indent=2)

items = itemList["items"]

#Liste ausgeben
def showList():
    print(f"{Fore.CYAN}="* 40)
    print("Hier ist deine aktuelle Einkaufsliste:")
    for item in items:
        print(item)
    #print("\n")
    print(f"{Fore.CYAN}="* 40 + "\n")

#Liste speichern
def saveList():
    with open(file_path, "w") as file:
        json.dump(itemList, file, indent=2)

#Liste auf Einträge überprüfen
def checkListEmpty():
    return len(itemList["items"]) == 0


#Modus wählen
def selectMode():
    print(f"{Fore.GREEN}="* 40)
    print(f"{Fore.GREEN}HAUPTMENUE:")
    print(f"{Fore.GREEN}="* 40)
    #mode_number = "0"
    #if mode_number == "0":
    mode = questionary.select(
        "Wähle einen Modus aus:\n",
        choices=["1. Eingabemodus", "2. Ansichtsmodus", "3. Bearbeitungsmodus", "X. Beenden"]
    ).ask()
    mode_number = mode.split('.', 1)[0]
    return mode_number

#Eingabe Modus
def modeOne():
    addAnotherItem = True
    while addAnotherItem == True:
        addedItem = input(f"{Fore.YELLOW}Was willst du auf die Einkaufsliste setzen?\n")
        if addedItem not in itemList["items"]:
            itemList["items"].append(addedItem)
            saveList()
            showList()
            addAnotherQuestion = questionary.select(
                "Möchtest du ein weiteren Artikel auf deine Einkaufsliste setzen?\n",
                choices=["Ja", "Nein"]
            ).ask()
            if addAnotherQuestion == "Ja":
                addAnotherItem = True
            elif addAnotherQuestion == "Nein":
                addAnotherItem = False
                showList()
        else:
            print(f"{Fore.RED}Dieser Artikel befindet sich schon auf deiner Einkaufsliste!\n")
            showList()
            addAnotherQuestion = questionary.select(
                "Möchtest du ein anderen Artikel auf deine Einkaufsliste setzen?\n",
                choices=["Ja", "Nein"]
            ).ask()
            if addAnotherQuestion == "Ja":
                addAnotherItem = True
            elif addAnotherQuestion == "Nein":
                addAnotherItem = False
                showList()

def modeTwo():
    print("Willkommen im Anzeigemodus\n")
    if checkListEmpty() == True:
        print(f"{Fore.GREEN}Deine Liste ist leer!\n")
    else:
        showList()
    stopShow = False
    while stopShow == False:
        wannaScratch = questionary.select(
            "Bist du etwa einkaufen und möchtest Elemente von deiner Liste abhaken?",
            choices=["Nein, ich will nur gucken.", "Ja, ich bin auf einem ShoppingSpree!"]
        ).ask()
        wannaScratchShort = wannaScratch.split(",", 1)[0]
        if wannaScratchShort == "Nein":
            showList()
            endShow = questionary.select(
                "Bist du fertig?",
                choices=["Fertig!"]
            ).ask()
            if endShow == "Fertig!":
                stopShow = True
        elif wannaScratchShort == "Ja":
            selectList = questionary.select(
                "Hier ist deine aktuelle Liste:\nWähle einen Artikel aus, um ihn von deiner Liste zu streichen",
                choices=itemList["items"]
            ).ask()
            itemToRemove = selectList
            itemList["items"].remove(itemToRemove)
            print(f"\n{Fore.RED}{itemToRemove} wurde entfernt!\n")
            saveList()


#Main Programm
if checkListEmpty() == True:
    modeOne()
else:
    while True:    
        mode = selectMode()
        if mode == "1":
            modeOne()
        elif mode == "2":
            modeTwo()
        elif mode == "X":
            print("Programm wird beendet.")
            break