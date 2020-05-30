from hexlib.web import cookiejar_filter, load_cookiejar, save_cookiejar
import browser_cookie3
import requests
import json
import glob
import time
import os
import pathlib
import multiprocessing

# cj = browser_cookie3.firefox()
# save_cookiejar(cookiejar_filter(cj, r".*mybluprint.*"), "cookies")

cj = load_cookiejar("cookies")

API = "https://api.mybluprint.com"
PLAYLIST_URL = "https://api.mybluprint.com/m/playlists/"
EPISODE_URL = "https://api.mybluprint.com/m/videos/secure/episodes/"

s = requests.session()
s.cookies = cj

FILTERS = [
    2058,
    2059,
    2046,
    2053,
    2047,
    2055,
    2057,
    2049,
    2045,  # bake
    2056,
    2050,
    2048,  # crochet
    2052,
    2054,
    3185,
    2062,
    2051,
    2061,
    2060,
]


# for category in FILTERS:
#    has_more_pages = True
#    page = 0
#    while has_more_pages:
#        r = s.get(API + "/filteredGalleries/all-online-classes?offset=%d&pageSize=24"
#                        "&sortBy=mostRecent&filterEnrolledCourses=false&"
#                        "selectedFilterOptions=[%%7B%%22facetName%%22:%%22categoryFilter%%22,%%22filterOptionId%%22:%%22%d%%22%%7D]"
#                  % (page, category))
#        with open("%d_page%d.json" % (category, page), "wb") as out:
#            out.write(r.content)
#
#        j = json.loads(r.content)
#        if j["searchResults"]["page"] == j["searchResults"]["totalPages"]:
#            has_more_pages = False
#        page += 1


def courses():
    for fname in glob.glob("pages/*.json"):
        with open(fname) as f:
            j = json.loads(f.read())

        for hit in j["searchResults"]["hits"]:
            hit = hit["baseballCard"]

            for cid in hit["enrollableCourseIds"]:
                yield (cid, hit)


# for cid, hit in courses():
#    url = PLAYLIST_URL + str(cid)
#
#    r = s.get(url)
#    with open("playlists/%d.json" % cid, "wb") as out:
#        out.write(r.content)
#    print(cid)

# for cid, hit in courses():
#    url = PLAYLIST_URL + str(cid) + "/materials"
#
#    r = s.get(url)
#    with open("materials/%d.json" % cid, "wb") as out:
#        out.write(r.content)
#    print(cid)

def download(url, path):
    try:
        response = s.get(url, stream=True, timeout=10)

        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(e)


# Download materials

# for fname in glob.glob("materials/*.json"):
#    with open(fname) as f:
#        j = json.loads(f.read())
#
#    for material in j:
#        if not material["downloadable"]:
#            continue
#
#        ext = os.path.splitext(material["materialPath"])[1]
#        path = "data/%d/materials/%s" % (material["playlistId"], material["materialName"] + ext)
#
#        pathlib.Path("data/%d/materials" % material["playlistId"]).mkdir(parents=True, exist_ok=True)
#
#        if os.path.exists(path):
#            continue
#
#        download(material["materialPath"], path)
#        print(path)


for fname in glob.glob("playlists/*.json"):
    with open(fname) as f:
        j = json.loads(f.read())

    for episode in j["episodes"]:
        r = s.get(EPISODE_URL + str(episode["episodeId"]))
        with open("episodes/%d.json" % episode["episodeId"], "wb") as out:
            out.write(r.content)
        print(episode["episodeId"])


def episode_info(eid):
    with open("episodes/%d.json" % eid) as f:
        j = json.loads(f.read())
    return j

# Download episodes
for fname in glob.glob("playlists/*.json"):
    with open(fname) as f:
        j = json.loads(f.read())

    for episode in j["episodes"]:
        for source in episode_info(episode["episodeId"]):
            if source["format"] == "mp4":

                path = "data/%d/episodes/%d_%s" % (j["playlistId"], episode["playlistPosition"], episode["name"] + ".mp4")
                pathlib.Path("data/%d/episodes" % j["playlistId"]).mkdir(parents=True, exist_ok=True)
                print(path)

                if os.path.exists(path):
                    continue

                download(source["url"], path)
