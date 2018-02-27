import requests
from bs4 import BeautifulSoup
import os
import pdfkit
from urllib.parse import urljoin
import youtube_dl


articles = []
videos = []
kits = []


def get_articles():

    for page in range(0, 10):
        r = requests.get("https://software.intel.com/en-us/ai-academy/library?page=" + str(page))
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.find_all("a"):
            if link.get("href") is not None and link.get("href").startswith("/en-us/articles/"):
                if link.string is not None:
                    articles.append((link.get("href"), link.string))

            if link.get("href") is not None and link.get("href").startswith("/en-us/videos/"):
                if link.string is not None:
                    videos.append((link.get("href"), link.string))

        print(str(len(articles)) + " articles")
        print(str(len(videos)) + " videos")


def get_kits():

    r = requests.get("https://software.intel.com/en-us/ai-academy/students/kits")
    soup = BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):
        if link.string is not None and link.string == "Get Started":

            kits.append(link.get("href"))


def download_article(article):

    if not os.path.exists("articles"):
        os.mkdir("articles")

    if not os.path.isfile("articles/" + article[1] + ".pdf"):
        pdfkit.from_url(urljoin("https://software.intel.com/", article[0]), "articles/" + article[1] + ".pdf")


def download_video(video):

    if not os.path.exists("videos"):
        os.mkdir("videos")

    options = {"outtmpl": "videos/%(title)s.%(ext)s"}

    ytd = youtube_dl.YoutubeDL(options)
    ytd.download([urljoin("https://software.intel.com/", video[0])])


def download_file(url, destination):
    while True:
        try:
            response = requests.get(url, stream=True, timeout=10)

            if not os.path.exists(destination) and response.status_code == 200:
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
            break
        except:
            print("!")


def download_kit(kit_url):
    if not os.path.exists("kits"):
        os.mkdir("kits")

    kit_url = urljoin("https://software.intel.com/", kit_url)

    r = requests.get(kit_url)
    soup = BeautifulSoup(r.text, "html.parser")

    kit_title = soup.find("title").string

    if not os.path.exists("kits/" + kit_title):
        os.mkdir("kits/" + kit_title)

    pdfkit.from_url(kit_url, "kits/" + kit_title + "/kit.pdf")

    for link in soup.find_all("a"):

        target = link.get("href")

        if target is not None and target.endswith(".zip"):
            download_file(urljoin("https://software.intel.com/", target), "kits/" + kit_title + "/" + os.path.split(target)[1])


# get_articles()
get_kits()

for k in kits:
    download_kit(k)
#
# for a in articles:
#     download_article(a)
#
# for v in videos:
#     download_video(v)