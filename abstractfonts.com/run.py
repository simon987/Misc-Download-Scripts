import requests
from bs4 import BeautifulSoup
import multiprocessing
import os


proxy_index = 0

proxies = {
    "http": ""
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1"
}


def already_downloaded(font_id):
    with open("downloaded.txt", "r") as f:
        return font_id in f.read().splitlines()


def flag_downloaded(font_id):
    with open("downloaded.txt", "a") as f:
        f.write(font_id + "\n")


def get_new_proxy():

    global proxy_index

    with open("proxies.txt", "r") as f:
        line = f.read().splitlines()[proxy_index]
        proxies["http"] = line
        print("Switched to proxy " + line)
        proxy_index += 1


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_dl_links(url):
    print(url)
    r = request_timeout(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.findAll("a"):
        if a.get("data-font-id") is not None:
            with open("fonts.txt", "a") as f:
                f.write(a.get("data-font-id") + "\n")


def get_fonts():
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letters.append("Numbers")

    all_page_links = []

    for letter in letters:
        all_page_links.append("http://www.abstractfonts.com/alpha/" + letter)

    pool = multiprocessing.Pool(processes=25)
    pool.map(get_dl_links, all_page_links)


def download_font(font_id):

    if already_downloaded(font_id):
        return

    while True:
        try:
            r = requests.get("http://www.abstractfonts.com/download/" + font_id, stream=True, proxies=proxies, headers=headers, timeout=5)

            if r.status_code == 404:
                print(str(r.status_code) + " - http://www.abstractfonts.com/download/" + font_id)
                get_new_proxy()
                return

            if "Content-Disposition" not in r.headers:
                print(r.text)
                get_new_proxy()
                return

            file_path = "fonts/" + r.headers["Content-Disposition"][r.headers["Content-Disposition"].rfind("\"", 0, -2) + 1:-1]

            if os.path.exists(file_path):
                return

            print(file_path)

            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            flag_downloaded(font_id)
            break
        except:
            get_new_proxy()
            continue

    return


# get_fonts()
get_new_proxy()

pool = multiprocessing.Pool(processes=100)

with open("fonts.txt", "r") as f1:
    pool.map(download_font, f1.read().splitlines())