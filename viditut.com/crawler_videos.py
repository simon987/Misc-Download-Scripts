import requests
import bs4
import json


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except:
            print("!", end="", flush=True)
            continue


def get_videos(course):

    videos = []
    r = request_timeout(course[2])
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    for link in soup.find_all("a"):

        if link.get("class") is not None and str(link.get("class")) == "['item-name', 'video-name', 'ga']":
            video_id = link.get("data-ga-value")
            video_name = link.text.replace("\n", "").strip()

            videos.append((video_name, video_id))

    return videos


def get_links(course, video):

    links = []
    r = request_timeout("https://viditut.com/ajax/course/" + course[1] + "/" + video[1] + "/play")
    json_obj = json.loads(r.text)

    if len(json.loads(r.text)) > 0:
        json_obj = json_obj[0]
    else:
        return links

    for quality in json_obj["qualities"]:
        links.append((quality, json_obj["urls"][quality]))

    return links


file = open("courses.txt", "r")

fileout = open("links1.txt", "w")

for line in file.read().splitlines():

    category, course_name, course_id, course_url = line.split("\0")

    course = (course_name, course_id, course_url)

    print(course_name)

    for video in get_videos(course):
        for link in get_links(course, video):
            fileout.write(category + "/" + course_name + "/" + video[0] + "\0" + link[0] + "\0" + link[1] + "\n")
        fileout.flush()


fileout.close()
file.close()