import requests
from bs4 import BeautifulSoup
import multiprocessing
import os
from urllib.parse import urljoin


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "http://www.fontspace.com"
}


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_dl_links(page_url):

    print(page_url)

    r_page = request_timeout(page_url)
    soup_page = BeautifulSoup(r_page.text, "html.parser")

    for dl_link in soup_page.findAll("a", attrs={"class": "box-button transparent"}):
        with open("fonts.txt", "a") as f:
            f.write(dl_link.get("href") + "\n")


def get_fonts():

    lists = list("abcdefghijklmnopqrstuvwxyz")
    lists.append("letter")

    page_links = []

    for page in lists:

        print(page)

        r = request_timeout("http://www.fontspace.com/list/" + page)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.findAll("a"):
            if a.get("href") is not None and a.get("href").find("?p=") != -1:
                page_links.append(a.get("href"))

        page_max = page_links[-2]
        page_max = int(page_max[page_max.rfind("=") + 1:])

        print(page_max)

        for i in range(1, page_max):
            page_links.append("http://www.fontspace.com/list/" + page + "?p=" + str(i))

    pool = multiprocessing.Pool(processes=25)
    pool.map(get_dl_links, page_links)


def download_font(dl_url):

    full_url = urljoin("http://www.fontspace.com", dl_url)
    file_path = "fonts" + full_url[full_url.rfind("/"):]

    if os.path.exists(file_path):
        return

    print(file_path)

    r = requests.get(full_url, stream=True, headers=headers, cookies=cookies)

    if r.status_code != 200:
        print(r.status_code)
        return

    with open(file_path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def get_cookie():

    r = request_timeout("http://www.fontspace.com/list/a?text=&p=2")
    return r.cookies


def download_all(cookies):

    pool = multiprocessing.Pool(processes=25)

    with open("fonts.txt", "r") as f:

        pool.map(download_font, f.read().splitlines())



# get_fonts()
cookies = get_cookie()

download_all(cookies)

