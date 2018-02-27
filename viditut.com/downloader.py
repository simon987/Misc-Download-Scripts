import pathlib
import os
import requests

file = open("links1.txt", "r")

i = 0

for line in file.read().splitlines():

    path, quality, link = line.split("\0")

    if quality != "720":
        continue

    i += 1

    pathlib.Path(os.path.split(path)[0]).mkdir(parents=True, exist_ok=True)

    if os.path.isfile(os.path.split(path)[0] + os.sep + str(i) + " -" + os.path.split(path)[1] +
            "[" + quality + "].mp4"):
        continue

    print(path)

    while True:
        try:
            response = requests.get(link, stream=True, timeout=5)

            with open(os.path.split(path)[0] + os.sep + str(i) + " -" + os.path.split(path)[1] +
                              "[" + quality + "].mp4", 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            break
        except:
            print("!", end="", flush=True)
            continue
