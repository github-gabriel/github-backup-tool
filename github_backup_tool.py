import json
import sys

import tkinter as tk
from tkinter import filedialog

import git
import requests

root = tk.Tk()
root.withdraw()

print("Wähle einen Ordner aus, in dem die geklonten Repositories"
      "unter /GitHub_Backup/Repositories gespeichert werden sollen.")

localdir = filedialog.askdirectory()
while True:
    if localdir:
        localdir += "/GitHub_Backup/Repositories"
        break
    else:
        localdir = filedialog.askdirectory()

username = input("Von welchem Profil(Name) soll ein Backup erstellt werden?: ")

response = requests.get(f"https://api.github.com/users/{username}/repos")

input_dict = json.loads(response.text)

print("Folgende Repositories werden heruntergeladen bzw. geklont:\n")

for x in input_dict:
    if x['html_url']:
        print(x['name'])

print(f"\nDie Repositories werden unter {localdir} gespeichert.\nSoll der Vorgang gestartet werden? y/n")

choice = input()
choice = choice.lower()

if choice == "y":
    print("\nDer Vorgang wird gestartet...")
    for x in input_dict:
        if x['html_url']:
            try:
                repo = git.Repo.clone_from(x['html_url'], localdir + "/" + x['name'])
            except:
                print(f"\nDer Ordner {localdir} ist nicht leer!")
                sys.exit(0)
            else:
                print(
                    "\nName: " + x['name'] + "\nURL: " + x['html_url'] + "\nSpeicherort: " + localdir + "/" + x['name'])
    print(f"\nDas Backup wurde unter {localdir} erstellt!")
else:
    sys.exit(0)

input()
