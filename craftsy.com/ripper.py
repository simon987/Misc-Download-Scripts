import requests
import pathlib
import os
import json


headers_login = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Referer": "https://unlimited.craftsy.com/login",
    "X-Requested-By": "Craftsy"
}

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "application/json, text/plain, */*"
}


def login(email, password):

    r1 = requests.get("https://unlimited.craftsy.com/login", headers=headers_login)

    payload = json.dumps({"email": email, "password": password})
    r2 = requests.post("https://api.craftsy.com/login/", data=payload, headers=headers_login, cookies=r1.cookies)

    print(r2.text)

    return r2


def get_course_info(r_login, course_id):
        while True:
            try:
                r = requests.get("https://api.craftsy.com/m/playlists/" + course_id, headers=headers_login,
                                 cookies=r_login.cookies, timeout=5)
                break
            except:
                print("!", end="", flush=True)
                continue

        course_info = json.loads(r.text)

        return course_info


def get_materials(r_login, course_id):

    materials = []

    while True:
        try:
            r = requests.get("https://api.craftsy.com/m/playlists/" + course_id + "/materials", headers=headers_login,
                             cookies=r_login.cookies, timeout=5)
            break
        except:
            print("!", end="", flush=True)
            continue

    try:
        material_info = json.loads(r.text)

        for material in material_info:
            materials.append((material["materialName"], material["materialPath"]))
    except:
        print("Err mat!", end="", flush=True)

    return materials


def get_episodes(course_info):

    episodes = []

    course_name = course_info["name"]
    print(course_name)

    for episode in course_info["episodes"]:
        episodes.append((course_name, episode["name"], episode["episodeId"]))

    return episodes


def download_episode(episode, r_login):
    while True:
        try:
            r = requests.get("https://api.craftsy.com/m/videos/secure/episodes/" + str(episode[2]), headers=headers,
                             cookies=r_login.cookies, timeout=5)
            break

        except Exception as e:
            print("!", end="", flush=True)
        continue

    episode_info = []
    try:
        episode_info = json.loads(r.text)
    except:
        print("Err episode!", end="", flush=True)

    for source in episode_info:
        if source["format"] == "mp4":
            path = episode[0]
            print(path + os.sep + str(episode[1]) + ".mp4")
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

            if os.path.exists(path + os.sep + str(episode[2]) + " - " + episode[1].replace("/", "") + ".mp4"):
                print("Skipping...")
                continue

            while True:
                try:
                    response = requests.get(source["url"], stream=True, timeout=5)

                    with open(path + os.sep + str(episode[2]) + " - " + episode[1].replace("/", "") + ".mp4", 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    break
                except Exception as e:
                    print("!", end="", flush=True)
                    continue


def download_material(r_login, material, course_info):

    path = course_info["name"]
    print(path + os.sep + material[0] + os.path.splitext(material[1])[1])
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    if os.path.exists(path + os.sep + material[0] + os.path.splitext(material[1])[1]):
        print("Skipping...")
        return

    while True:
        try:
            response = requests.get(material[1], stream=True, timeout=5, cookies=r_login.cookies)

            with open(path + os.sep + material[0] + os.path.splitext(material[1])[1], 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            break
        except:
            print("!", end="", flush=True)
            continue


rLogin = login("", "")


for course in open("courses.txt").read().splitlines():

    print(course)

    course_info = get_course_info(rLogin, course)

    for material in get_materials(rLogin, course):
        download_material(rLogin, material, course_info)
        print(material)

    for episode in get_episodes(course_info):
        download_episode(episode, rLogin)
        print(episode)





