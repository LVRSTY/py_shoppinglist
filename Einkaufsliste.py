#import
import questionary
import json
from colorama import init, Fore, Style

#Öffne JSON File mit Items
with open('itemList.json', 'r') as file:
    itemList = json.load(file)
items = itemList["items"]

#Liste ausgeben
def showList():
    print(f"{Fore.CYAN}={Style.RESET_ALL}"* 40)
    print("Hier ist deine aktuelle Einkaufsliste:\n")
    for item in items:
        print(item)
    #print("\n")
    print(f"{Fore.CYAN}={Style.RESET_ALL}"* 40 + "\n")

#Modus wählen
def selectMode():
    print(f"{Fore.GREEN}={Style.RESET_ALL}"* 40)
    print(f"{Fore.GREEN}HAUPTMENUE:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}={Style.RESET_ALL}"* 40)
    mode_number = "0"
    if mode_number == "0":
        mode = questionary.select(
            "Wähle einen Modus aus:\n",
            choices=["1. Eingabemodus", "2. Ansichtsmodus", "3. Bearbeitungsmodus", "X. Beenden"]
        ).ask()
        mode_text = mode.split('. ', 1)[1]
        mode_number = mode.split('.', 1)[0]
        #print(f"Du hast den \"{mode_text}\" gewählt\n")
        #print(mode_number)
    return mode_number

#Eingabe Modus
def modeOne():
    addAnotherItem = True
    while addAnotherItem == True:
        addedItem = input(f"{Fore.YELLOW}Was willst du auf die Einkaufliste setzen?{Style.RESET_ALL}\n")
        if addedItem not in itemList["items"]:
            itemList["items"].append(addedItem)
            with open("itemList.json", "w") as file:
                json.dump(itemList, file, indent=2)
            showList()
            addAnotherQuestion = questionary.select(
                "Möchtest du ein weiteren Artikel auf deine Einkaufliste setzen?\n",
                choices=["Ja", "Nein"]
            ).ask()
            if addAnotherQuestion == "Ja":
                addAnotherItem = True
            elif addAnotherQuestion == "Nein":
                addAnotherItem = False
                showList()
        else:
            print(f"{Fore.RED}Dieser Artikel befindet sich schon auf deiner Einkaufsliste!{Style.RESET_ALL}\n")
            showList()
            addAnotherQuestion = questionary.select(
                "Möchtest du ein anderen Artikel auf deine Einkaufliste setzen?\n",
                choices=["Ja", "Nein"]
            ).ask()
            if addAnotherQuestion == "Ja":
                addAnotherItem = True
            elif addAnotherQuestion == "Nein":
                addAnotherItem = False
                showList()


#Main Programm
while True:
    showList()
    mode = selectMode()
    
    if mode == "1":
        modeOne()
    elif mode == "X":
        print("Programm wird beendet.")
        break
    #elif mode == "3":
        #modeThree()