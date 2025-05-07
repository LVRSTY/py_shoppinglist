import json

with open('itemList.json', 'r') as file:
    itemList = json.load(file)

# Ausgabe des geladenen Python-Objekts
#print(type(daten))
#print(daten)
daten_liste = itemList["items"]
print(daten_liste)


#json append
itemList["items"].append("Käse")

#json speichern
with open("itemList.json", "w") as file:
    json.dump(itemList, file, indent=2)


#Prüfung ist der Eintrag neu
neu = "Käse"
if neu not in daten["einkaufsliste"]:
    daten["einkaufsliste"].append(neu)