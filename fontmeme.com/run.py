import requests
from bs4 import BeautifulSoup
import multiprocessing
import os


proxy_index = 0

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1"
}

proxies = {
    'https': '',
}


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_fonts():
    for i in range(3758):

        print(i)

        r = request_timeout("https://fontmeme.com/fonts/page/" + str(i))

        soup = BeautifulSoup(r.text, "html.parser")

        for div in soup.findAll("div"):

            if div.get("id") is not None and div.get("id") == "ptitle":
                for child in div.children:
                    if child.get("href") is not None:

                        with open("fonts.txt", "a") as f:
                            f.write(child.get("href") + '\n')


def get_new_proxy():

    global proxy_index

    with open("proxies.txt", "r") as f:
        line = f.read().splitlines()[proxy_index]
        proxies["https"] = line
        print("Switched to proxy " + line)
        proxy_index += 1


def download_font(font_url):

    file_path = "fonts/" + font_url[font_url[:-1].rfind("/")+1:-6] + ".zip"

    if os.path.exists(file_path):
        return

    r1 = request_timeout(font_url)

    dl_link_index = r1.text.find("https://fontmeme.com/fonts/download/")

    if dl_link_index != -1:
        dl_link = r1.text[dl_link_index: r1.text.find("'", dl_link_index)]

        headers["Referer"] = font_url

        try:
            r = requests.get(dl_link, stream=True, headers=headers, proxies=proxies, cookies=r1.cookies, timeout=10)
        except:
            get_new_proxy()
            return

        if r.status_code != 200:
            print(r.status_code)
            return

        reached_limit = False

        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        with open(file_path, "rb") as f:
            if f.read().find(b"PK") != 0:
                reached_limit = True

        if reached_limit:
            os.remove(file_path)
            print("You have reached the maximum permitted downloads")
            get_new_proxy()


def download_all():
    pool = multiprocessing.Pool(processes=100)

    with open("fonts.txt", "r") as f:
        pool.map(download_font, f.read().splitlines())


# get_fonts()
# get_new_proxy()
download_all()


