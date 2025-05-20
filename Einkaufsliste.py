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

#Liste anzeigen
def showList():
    print(f"{Fore.CYAN}="* 40)
    print(f"{Fore.LIGHTBLUE_EX}Hier ist deine aktuelle Einkaufsliste:")
    for item in items:
        print(item)
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

#Eingabemodus
def modeAdd():
    print(f"{Fore.GREEN}\nWillkommen im Eingabemodus\n")
    try:
        while True:
            addedItem = input(f"{Fore.YELLOW}Was willst du auf deine Einkaufsliste schreiben? (Ctrl + C zum Beenden)\n")
            if addedItem == "":
                print(f"{Fore.RED}Du kannst keine 'leeren Artikel' auf die Einkaufsliste setzen")
            elif addedItem not in itemList["items"]:
                itemList["items"].append(addedItem)
                saveList()
                showList()
            else:
                print(f"{Fore.RED}Dieser Artikel befindet sich schon auf deiner Einkaufsliste!\n")
                showList()
    except KeyboardInterrupt:
        print("\n\nEingabe beendet!")

#Einkaufsmodus
def modeShop():
    print(f"{Fore.GREEN}\nWillkommen im Einkaufsmodus\n\n")
    try:
        if checkListEmpty() == True:
            print(f"{Fore.RED}Deine Liste ist leer!\n")
        else:
            while True:
                if checkListEmpty():
                    print(f"{Fore.YELLOW}Du hast alle deine Artikel von der Liste abgehakt. Super Shopping Tour!\n")
                    break
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
            

#Bearbeitungsmodus
def modeEdit():
    print(f"{Fore.GREEN}\nWillkommen im Bearbeitungsmodus\n\n")
    try:
        if checkListEmpty() == True:
            print(f"{Fore.RED}Deine Liste ist leer!\n")
        else:
            submenuSelect = inquirer.select(
                message="Welche Bearbeitungsfunktion möchtest du auswählen?",
                choices=["a) einen Artikel bearbeiten", "b) die gesamte Liste verwalten"]
            ).execute()
            if "bearbeiten" in submenuSelect.lower():
                if checkListEmpty():
                    print(f"{Fore.RED}Es gibt keine Artikel zum Bearbeiten!")
                editArticleSelect = inquirer.select(
                    message="Welchen Artikel möchtest du bearbeiten?",
                    choices=itemList["items"]
                ).execute()
                articleToEdit = editArticleSelect
                print(f"Du hast folgenden Artikel zum Bearbeiten gewählt: {articleToEdit}")
                articleEditAction = inquirer.select(
                    message="Was möchtest du mit dem Artikel tun?",
                    choices=["a) Umbenennen", "b) Löschen", "c) Markieren"]
                ).execute()
                if "umbenennen" in articleEditAction.lower():
                    articleIndex = items.index(articleToEdit)
                    itemList["items"][articleIndex] = input(f"Gib einen neuen Namen für den Artikel ein:\n")
                    print(f"Artikel {articleToEdit} wurde umbenannt!\n")
                    saveList()
                elif "löschen" in articleEditAction.lower():
                    itemList["items"].remove(articleToEdit)
                    print(f"Artikel {articleToEdit} wurde gelöscht")
                    saveList()
                elif "markieren" in articleEditAction.lower():
                    print(f"Diese Funktion gibt es noch nicht")
            elif "verwalten" in submenuSelect.lower():
                listEditAction = inquirer.select(
                    message="Was möchtest du mit der Liste tun?",
                    choices=["a) Liste leeren", "b) mehrere Artikel löschen", "c) Duplikate prüfen", "d) Liste alphabetisch sortieren"]
                ).execute()
                if "leeren" in listEditAction.lower():
                    confirmListClear = inquirer.confirm(
                       message="Bist du dir sicher, dass du die gesamte Liste leeren willst?",
                       default=False
                    ).execute()
                    if confirmListClear:
                       print(f"{Fore.RED}\nLösche alle Einträge...")
                       itemList["items"] = []
                       saveList()
                    else:
                        print(f"Aktion abbrechen...")
                if "löschen" in listEditAction.lower():
                    deleteMultipleArticles = inquirer.checkbox(
                        message="Welche Artikel möchtest du löschen?",
                        choices=itemList["items"]
                    ).execute()
                    confirmDeleteMultiple = inquirer.confirm(
                       message="Bist du dir sicher, dass du die Artikel löschen willst?",
                       default=False
                    ).execute()
                    if confirmDeleteMultiple:
                        print(f"Lösche Einträge...")
                        for toDelete in deleteMultipleArticles:
                            if toDelete in itemList["items"]:
                                itemList["items"].remove(toDelete)
                            saveList()
                    else:
                        print(f"Aktion abbrechen...")         
    except KeyboardInterrupt:
        print("\nBearbeitungsmodus beendet")




if checkListEmpty() == True:
        print(f"{Fore.RED}\n***Deine Einkaufsliste ist noch leer!***\n")
else:
    showList()
while True:
        mode = selectMode()
        if mode == "1":
            modeAdd()
        elif mode == "2":
            modeShop()
        elif mode == "3":
#            print(f"{Fore.RED}\nDieser Modus ist noch nicht verfügbar!\n")
            modeEdit()
        elif mode == "X":
            print("Programm wird beendet.")
            break