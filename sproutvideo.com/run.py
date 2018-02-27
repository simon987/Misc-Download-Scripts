import requests
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("password")
parser.add_argument("url")
parser.add_argument("--user")

args = parser.parse_args()


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Upgrade-Insecure-Requests": "1",
    "Referer": args.url
}


payload = {"email": args.user if args.user is not None else "", "password": args.password,
           "host": "unknown", "url": "unknown", "queryParams": ""}
print(payload)
r = requests.post(args.url.replace("embed", "video_password"), headers=headers, data=payload)
print(r.cookies)


soup = BeautifulSoup(r.text, "html.parser")

try:
    print(soup.find("a", attrs={"class": "hd-download"}).get("href"))
    print(soup.find("a", attrs={"class": "sd-download"}).get("href"))
except AttributeError:
    print("Wrong password/username")

