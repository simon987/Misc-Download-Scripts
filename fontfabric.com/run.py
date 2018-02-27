import requests
from bs4 import BeautifulSoup
import multiprocessing

fonts = []


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_fonts():

    for page in range(1, 4):
        r = request_timeout("http://www.fontfabric.com/category/free/page/" + str(page))
        soup = BeautifulSoup(r.text, "html.parser")

        for link in soup.find("div", attrs={"class": "recent-leads fix"}).findAll("a"):

            href = link.get("href")

            if href is not None and href not in fonts and href.find("#") == -1 and href.find("category/") == -1:
                fonts.append(link.get("href"))

    print(len(fonts))


def download_font(url):

    r = request_timeout(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.findAll("a"):

        onclick = a.get("onclick")

        if onclick is not None and onclick.startswith("window.location"):
            dl_link = "http://www.fontfabric.com" + onclick[onclick.find("'")+1:onclick.rfind("'")]
            file_path = "fonts" + dl_link[dl_link.rfind("/"):]
            r_dl = requests.get(dl_link, stream=True, cookies=r.cookies)

            if r_dl.status_code != 200:
                print(r_dl.status_code)
                return

            print(file_path)

            with open(file_path, 'wb') as f:
                for chunk in r_dl.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)


def download_all():
    pool = multiprocessing.Pool(processes=25)
    pool.map(download_font, fonts)


get_fonts()
download_all()