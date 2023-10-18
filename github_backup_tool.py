import os, stat, shutil, requests, git, json, validators

import urllib.request
import tkinter as tk

from tkinter import filedialog
from datetime import datetime


def error(exception):
    seperator = ""
    max_len = 0
    for line in str(exception).splitlines():
        if len(line) > max_len:
            max_len = len(line)
    for i in range(max_len):
        seperator += '-'
    return f"\n{seperator}\n" + datetime.today().strftime('%d.%m.%Y %H:%M:%S') + '\n\n' + str(
        exception) + f"\n{seperator}\n"


def download_file_from_readme(local_repository_path, log):
    try:
        i = 0
        file = open(local_repository_path + "/README.md", encoding="utf8")
        lines = file.readlines()
        for line in lines:
            if validators.url(line):
                req = urllib.request.Request(line, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
                r = urllib.request.urlopen(req)
                if r.getheader('Content-Type') == "video/mp4":
                    try:
                        i += 1
                        urllib.request.urlretrieve(line, local_repository_path + '/' + f"video {i}" + ".mp4")
                    except Exception as e1:
                        log.write(error(e1))
    except Exception as e2:
        log.write(error(e2))


def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


def get_all_user_repositories(username):
    page = 1
    per_page = 100
    all_repositories = []

    while True:
        # API-Anfrage für die aktuelle Seite der Repositories
        response = requests.get(f"https://api.github.com/users/{username}/repos",
                                params={'per_page': per_page, 'page': page},
                                headers={'accept': 'application/vnd.github+json'})

        if response.status_code == 200:
            repositories = response.json()
            if len(repositories) == 0:
                # Wenn die Antwort leer ist, sind alle Repositories aufgelistet
                break
            else:
                # Füge die Repositories der aktuellen Seite zur Gesamtliste hinzu
                all_repositories.extend(repositories)
                # Gehe zur nächsten Seite
                page += 1
        else:
            # Fehler bei der API-Anfrage
            print(f"Fehler bei der API-Anfrage (Statuscode: {response.status_code}).")
            break

    return all_repositories


def main():
    log = open('log.txt', 'a')

    root = tk.Tk()
    root.withdraw()

    username = input("Von welchem Profil(Name) soll ein Backup erstellt werden?: ")

    print("Wähle einen Ordner aus, in dem die geklonten Repositories"
          f" unter  \"/GitHub_Backup/Repositories_{username}\" gespeichert werden sollen.")

    localdir = filedialog.askdirectory()
    while True:
        if localdir:
            localdir += "/GitHub_Backup/Repositories_" + username
            break
        else:
            localdir = filedialog.askdirectory()

    all_repositories = get_all_user_repositories(username)

    input_dict = json.loads(json.dumps(all_repositories))

    print(f"Folgende Repositories [{len(all_repositories)} Stück] werden heruntergeladen bzw. geklont:\n")

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
                path = ""
                try:
                    path = localdir + "/" + x['name']
                    repo = git.Repo.clone_from(x['html_url'], path)
                    download_file_from_readme(path, log)
                except Exception as e1:
                    log.write(error(e1))
                    print(
                        f"\nDer Ordner {path} ist nicht leer! Soll der Ordner ersetzt werden? y für ja, Y für Ja für alle, n für nein, N für Nein für alle")
                    answer = input()
                    if answer == 'y':
                        shutil.rmtree(path, onerror=del_rw)
                        repo = git.Repo.clone_from(x['html_url'], path)
                        download_file_from_readme(path, log)
                    elif answer == 'n':
                        continue
                    elif answer == 'Y':
                        shutil.rmtree(localdir, onerror=del_rw)
                        try:
                            for y in input_dict:
                                if y['html_url']:
                                    path = localdir + "/" + y['name']
                                    repo = git.Repo.clone_from(y['html_url'], path)
                                    download_file_from_readme(path, log)
                                    print(
                                        "\nName: " + y['name'] + "\nURL: " + y['html_url'] + "\nSpeicherort: " + path)
                            break
                        except Exception as e2:
                            log.write(error(e2))
                    elif answer == 'N':
                        for z in input_dict:
                            if z['html_url']:
                                path = localdir + "/" + z['name']
                                if not os.path.isdir(path):
                                    try:
                                        repo = git.Repo.clone_from(z['html_url'], path)
                                        download_file_from_readme(path, log)
                                        print(
                                            "\nName: " + z['name'] + "\nURL: " + z[
                                                'html_url'] + "\nSpeicherort: " + path)
                                    except Exception as e3:
                                        log.write(error(e3))
                        break
                else:
                    print(
                        "\nName: " + x['name'] + "\nURL: " + x['html_url'] + "\nSpeicherort: " + path)
        print(f"\nDas Backup wurde unter {localdir} erstellt!")
    else:
        print("Der Vorgang wurde abgebrochen")

    input()


if __name__ == '__main__':
    main()
