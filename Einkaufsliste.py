#import
import json
import os
from InquirerPy import inquirer
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
    print("Hier ist deine aktuelle Einkaufsliste:\n")
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
    mode = inquirer.select(
        message="Wähle einen Modus aus:\n",
        choices=["1. Eingabemodus", "2. Einkaufsmodus", "3. Bearbeitungsmodus", "X. Beenden"]
    ).execute()
    mode_number = mode.split('.', 1)[0]
    return mode_number

#Eingabe Modus
def modeOne():
    print(f"{Fore.GREEN}\nWillkommen im Eingabemodus\n")
    try:
        while True:
            addedItem = input(f"{Fore.YELLOW}Was willst du auf die Einkaufsliste setzen? (Ctrl + C zum Beenden)\n")
            if addedItem not in itemList["items"]:
                itemList["items"].append(addedItem)
                saveList()
                showList()
            else:
                print(f"{Fore.RED}Dieser Artikel befindet sich schon auf deiner Einkaufsliste!\n")
                showList()
    except KeyboardInterrupt:
        print("\n\nEingabe beendet!")

#Einkaufsmodus
def modeTwo():
    print(f"{Fore.GREEN}\nWillkommen im Einkaufsmodus\n\n")
    if checkListEmpty() == True:
        print(f"{Fore.GREEN}Deine Liste ist leer!\n")
    try:
        while True:
            selectList = inquirer.select(
                message="Hier ist deine aktuelle Liste:\nWähle einen Artikel aus, um ihn von deiner Liste zu streichen (Ctrl + C zum Beenden)",
                choices=itemList["items"]
            ).execute()
            itemToRemove = selectList
            itemList["items"].remove(itemToRemove)
            print(f"\n{Fore.RED}{itemToRemove} wurde entfernt!\n")
            saveList()
    except KeyboardInterrupt:
        print("\nEinkaufsmodus beendet")
            

if checkListEmpty() == True:
        print(f"{Fore.RED}\n***Deine Einkaufsliste ist noch leer!***\n")
while True:
        mode = selectMode()
        if mode == "1":
            modeOne()
        elif mode == "2":
            modeTwo()
        elif mode == "3":
            print(f"{Fore.RED}\nDieser Modus ist noch nicht verfügbar!\n")
        elif mode == "X":
            print("Programm wird beendet.")
            break