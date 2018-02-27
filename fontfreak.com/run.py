import requests
from bs4 import BeautifulSoup
import multiprocessing
import os


fonts = []


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_fonts():

    letters = list("abcdefghijklmnopqrstuvwxyz")
    letters.append("no")

    pool = multiprocessing.Pool(processes=25)
    pool.map(get_dl_links, letters)


def get_dl_links(letter):

    for page in range(1, 11):

        r = request_timeout("http://www.fontfreak.com/fonts-" + letter + str(page) + ".htm")
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.findAll("a"):
            if a.text is not None and a.text == "click here to download":
                with open("fonts.txt", "a") as f:
                    f.write("http://www.fontfreak.com/" + a.get("href") + "\n")


def download_font(url):
    r = request_timeout(url)
    soup = BeautifulSoup(r.text, "html.parser")

    dl_link = soup.find("a", attrs={"title": "DOWNLOAD FONT"})

    if dl_link is not None:

        dl_url = "http://www.fontfreak.com/" + dl_link.get("href")
        file_path = "fonts/" + dl_url[dl_url.rfind("/")+1:]

        if os.path.exists(file_path):
            return

        r = requests.get(dl_url, stream=True)

        print(file_path)

        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    else:
        print("no dl" + url)


get_fonts()

pool = multiprocessing.Pool(processes=25)
with open("fonts.txt", "r") as f:
    pool.map(download_font, f.read().splitlines())

