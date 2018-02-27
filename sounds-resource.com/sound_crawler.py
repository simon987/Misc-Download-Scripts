import requests
import bs4
import os

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
}

URL = "https://www.sounds-resource.com"


def get_consoles():

    consoles = []

    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for console in soup.find(id="leftnav-consoles"):
        if type(console) == bs4.element.Tag and console.get("href") is not None:
            consoles.append((console.text, URL + console.get("href")))

    return consoles


def get_games(console, letter):

    games = []

    print(console[0] + " - " + letter)

    print(console[1] + letter + ".html")
    response = requests.get(console[1] + letter + ".html")
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all("a"):
        for child in link.findChildren():
            if child.get("class") is not None and child.get("class") == ['gameiconcontainer']:
                game_name = child.find("div").find("span").string

                games.append((game_name, URL + link.get("href")))

    return games


def get_sounds(game):
    sounds = []

    response = requests.get(game[1])
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for row in soup.find_all("tr"):

        if row.get("class") is not None and "altrow" in row.get("class")[0]:

            for child in row.children:
                if child is not None and isinstance(child, bs4.Tag) and child.get("style") == "padding-left: 10px;":

                    sound_name = child.string
                    sound_url = child.find("a").get("href")

                    sound_dl = "https://www.sounds-resource.com/download/" + sound_url.split("/")[-2:-1][0] + "/"

                    sounds.append((sound_name, sound_dl))

    return sounds

file = open("links.txt", "w")

for console in get_consoles():
    for letter in "0ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for game in get_games(console, letter):
            for sound in get_sounds(game):
                file.write(console[0] + os.sep + game[0] + os.sep + sound[0] + os.sep + "\0" + sound[1] + "\n")

file.close()
