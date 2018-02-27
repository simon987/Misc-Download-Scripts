import requests
from bs4 import BeautifulSoup
import multiprocessing
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.1001freefonts.com/"
}


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30, headers=headers)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_dl_links(url):

    print(url)

    r = request_timeout(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.findAll("a"):

        href = a.get("href")

        if href is not None and href.find("/d/") != -1:
            with open("links.txt", "a") as f:
                f.write(href + "\n")


def get_fonts():
    letters = list("abcdefghijklmnopqrstuvwxyz")
    letters.append("num")

    all_page_links = []

    for letter in letters:

        print(letter)

        r = request_timeout("https://www.1001freefonts.com/" + letter + "fonts.php")

        soup = BeautifulSoup(r.text, "html.parser")

        page_max = soup.find("div", attrs={"class": "pagingLabelWrapper"})
        page_max = page_max.text.split(" ")[-1]
        page_max = int(page_max)
        print(page_max)

        for i in range(1, page_max+1):
            all_page_links.append("https://www.1001freefonts.com/" + letter + "fonts" + str(i) + ".php")

    pool = multiprocessing.Pool(processes=25)
    pool.map(get_dl_links, all_page_links)


def download_font(url):
    file_path = "fonts" + url[url.rfind("/"):]

    if os.path.exists(file_path):
        return

    print(file_path)
    r = requests.get(url, stream=True, headers=headers)

    if r.status_code != 200:
        print(r.status_code)
        return

    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def download_all():
    pool = multiprocessing.Pool(processes=25)

    with open("links.txt", "r") as f:
        pool.map(download_font, f.read().splitlines())



# get_fonts()
download_all()