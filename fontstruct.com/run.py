import requests
from bs4 import BeautifulSoup
import multiprocessing
import os

username = ""
password = ""

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://fontstruct.com/",
    "Connection": "keep-alive"
}


font_ids = []


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30, headers=headers)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def login():

    r1 = request_timeout("https://fontstruct.com/login")
    print(r1.cookies)

    login_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://fontstruct.com/login",
        "Connection": "keep-alive"
    }

    payload = {"_username": username, "_password": password, "_csrf_token": "", "_submit": "Sign+In"}
    r = requests.post("https://fontstruct.com/login_check", headers=login_headers, data=payload, cookies=r1.cookies)
    print(r.cookies)
    print(len(r.text))
    print(r.headers)

    return r.history[0]


def get_font_ids(page_url):

    print(page_url)

    r = request_timeout(page_url)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.findAll("a"):

        href = a.get("href")

        if href is not None and href.startswith("/fontstructions") and href.find("/license/") == -1 and\
                        href.find("/vote_breakdown/") == -1:

            font_id = href[href.find("show/")+5:href.rfind("/")]

            if font_id not in font_ids:
                font_ids.append(font_id)
                with open("fonts.txt", "a") as f:
                    f.write(font_id + "\n")


def get_fonts():

    page_urls = []

    for page_num in range(1, 1428):
        page_urls.append("https://fontstruct.com/gallery?filters=all&page=" + str(page_num))

    pool = multiprocessing.Pool(processes=25)
    pool.map(get_font_ids, page_urls)


def download_font(font_id):

    dl_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://fontstruct.com/fontstructions/download/" + font_id,
        "Connection": "keep-alive"
    }

    dl_url = "https://fontstruct.com/font_archives/download/" + font_id

    while True:
        r = requests.get(dl_url, stream=True, headers=dl_headers, cookies=cookies)

        if r.status_code == 403:
            return

        if r.status_code == 500:
            continue

        if "Content-Disposition" not in r.headers:
            print(r.text)
            return

        file_path = "fonts/" + r.headers["Content-Disposition"][r.headers["Content-Disposition"].rfind("'") + 1:]

        if os.path.exists(file_path):
            return

        print(file_path)

        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return


def download_all():
    pool = multiprocessing.Pool(processes=25)

    with open("fonts.txt", "r") as f:
        pool.map(download_font, f.read().splitlines())


cookies = login().cookies

# get_fonts()
download_all()


