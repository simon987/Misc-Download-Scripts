import requests
from bs4 import BeautifulSoup
import csv
import multiprocessing


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Referrer": "https://charlierose.com/videos"
}


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=15)
        except Exception as e:
            print("!", end="", flush=True)
            continue


def get_video_info(url):

    r = request_timeout(url)
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        desc = soup.find("div", attrs={"class", "description"}).find("p").text

        with open('links.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([url, desc])

    except Exception as e:
        print(e)
        print("Invalid " + url)


pool = multiprocessing.Pool(processes=50)

urls = []
for i in range(0, 35000):
    urls.append("https://charlierose.com/videos/" + str(i))

pool.map(get_video_info, urls)
