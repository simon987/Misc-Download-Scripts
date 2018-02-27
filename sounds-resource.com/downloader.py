import pathlib
import requests
import os

file = open("links.txt", "r")


for line in file.read().splitlines():

    path, link = line.split("\0")
    pathlib.Path("sounds/" + path.strip()).mkdir(parents=True, exist_ok=True)

    # if os.path.exists("sounds/" + path + "/" + path.split("/")[-2:-1][0] + ".zip") or \
    #     os.path.exists("sounds/" + path + "/" + path.split("/")[-2:-1][0] + ".mp3"):
    #     continue

    print("sounds/" + path)


    while True:
        # try:
            response = requests.get(link, stream=True, timeout=5)

            file_extension = os.path.splitext(response.headers["Content-Disposition"])[1][:-2]

            with open("sounds/" + path + path.split("/")[-2:-1][0] + file_extension, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            break
        # except:
        #     print("!", end="", flush=True)
        #     continue