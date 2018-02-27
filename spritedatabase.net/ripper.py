import requests
from bs4 import BeautifulSoup
import re
import os
import mimetypes


headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

}


def get_systems():

    systems = []

    response = requests.get("http://spritedatabase.net/", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all("a")

    for link in links:
        if "system" in link.get('href'):

            systems.append((link.text.strip(), "http://spritedatabase.net/" + link.get('href')))

    return systems


def get_games(system):

    games = []

    response = requests.get(system[1], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all("a")

    for link in links:
        if link.get('href') is not None and "game/" in link.get('href'):
            games.append((link.text.strip().replace("/", ""), "http://spritedatabase.net/" + link.get('href')))

    return games


def get_sprites(game):
    print(game[0])
    sprites = []

    while True:
        try:
            response = requests.get(game[1], headers=headers, timeout=5)
            break
        except:
            print("!", end="", flush=True)
            continue

    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all("a")

    for link in links:
        if link.get('href') is not None and "file/" in link.get('href'):

            print(".", end="", flush=True)
            # Skip 'Latest files' thing
            if link.parent.get("class") is None:
                continue

            file_name = link.find(text=True)
            file_name = file_name.replace("zip", "")
            file_name = file_name.replace("mp3", "")
            file_name = file_name.replace("png", "")
            file_name = file_name.replace("gif", "")
            file_name = file_name.replace("ogg", "")
            file_name = re.sub('[^A-Za-z0-9 ]+', '', file_name)
            file_name = file_name.strip()

            sprites.append((file_name, "http://spritedatabase.net/" + link.get('href')))

    print("")
    return sprites


def get_download_link(link):

    while True:
        try:
            response = requests.get(link, headers=headers, timeout=5)
            break
        except:
            print("!", end="", flush=True)
            continue
    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all("img")

    for image in images:

        if image.get("style") is not None and "border: 1px solid" in image.get("style"):
            download_link = image.get("src")

            if "layout/format" in download_link:

                for div in soup.find_all("div"):

                    if div.get("class") is not None and str(div.get("class")) == "['dlcapsule']":

                        link = div.find("a").get("href")

                        if "files/" in link:
                            return "http://spritedatabase.net/" + link
                        else:
                            return link

            else:
                return "http://spritedatabase.net/" + download_link


def download_all(folder, sprite):

    if not os.path.isdir(folder):
        os.mkdir(folder)

    link = get_download_link(sprite[1])

    if link is None:
        print("ERROR: " + sprite[1])
        return

    if "drive.google" in link or "mediafire" in link:
        print("I can't download external link. Link: " + link)
        open("links", "a").write(link + "\n")
    else:

        print(folder + os.sep + sprite[0])

        while True:
            try:
                response = requests.get(link, stream=True, headers=headers, timeout=5)

                extension = ""
                if response.headers["Content-Type"] is not None:
                    extension = mimetypes.guess_extension(response.headers["Content-Type"])

                    if extension is None:
                        extension = ""

                if not os.path.exists(folder + os.sep + sprite[0] + extension) and response.status_code == 200:
                            with open(folder + os.sep + sprite[0] + extension, 'wb') as f:
                                for chunk in response.iter_content(chunk_size=1024):
                                    if chunk:
                                        f.write(chunk)
                break
            except:
                print("!")


mimetypes.init()


for system in get_systems():

    if not os.path.exists(system[0]):
        os.mkdir(system[0])

    for game in get_games(system):
        sprites = get_sprites(game)

        if os.path.exists(system[0] + os.sep + game[0]):
            print(str(len(os.listdir(system[0] + os.sep + game[0]))) + "/" + str(len(sprites)))

        if os.path.exists(system[0] + os.sep + game[0]) and len(os.listdir(system[0] + os.sep + game[0])) >= len(sprites):
            print("Skipping existing folder with " + str(len(os.listdir(system[0] + os.sep + game[0]))) + "/" + str(len(sprites)) + " existing sprites")
            continue

        for sprite in sprites:
            download_all(str(system[0] + os.sep + game[0]), sprite)



