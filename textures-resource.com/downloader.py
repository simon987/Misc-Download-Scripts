import pathlib
import requests
import os

file = open("links.txt", "r")


for line in file.read().splitlines():

    path, preview, link = line.split("\0")

    if os.path.isfile("textures/" + path + "preview.png"):
        continue

    print("textures/" + path)

    pathlib.Path("textures/" + path).mkdir(parents=True, exist_ok=True)

    while True:
        try:
            response = requests.get(preview, stream=True, timeout=5)
            with open("textures/" + path + "preview.png", 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            response2 = requests.get(link, stream=True, timeout=5)

            file_extension = os.path.splitext(response2.headers["Content-Disposition"])[1][:-2]

            with open("textures/" + path + path.split("/")[-2:-1][0] + file_extension, 'wb') as f:
                for chunk in response2.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            break
        except:
            print("!", end="", flush=True)
            continue