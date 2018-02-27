import requests
import bs4
import json

URL = "https://viditut.com"


def request_timeout(url):
    while True:
        try:
            return requests.get(url, timeout=30)
        except:
            print("!", end="", flush=True)
            continue


def get_categories():

    categories = []

    r = requests.get(URL)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    for i in soup.find_all("i"):
        if i.get("class") is not None and len(i.get("class")) > 1 and "cat-" in i.get("class")[1]:
            category_id = i.get("class")[1][4:]
            category_name = i.get("title")[:i.get("title").find("-") - 1]

            categories.append((category_name, category_id))

    return categories


def get_courses(category):
    last_len = 0
    courses = []
    page = 0
    while True:

        page += 1
        r = request_timeout("https://viditut.com/ajax/category/" + category[1] + "/courses?page=" + str(page))
        soup = bs4.BeautifulSoup(json.loads(r.text)["html"], "html.parser")

        for link in soup.find_all("a"):
            if link.get("href") is not None:
                if link.find("h3") is not None:
                    course_link = link.get("href")
                    course_name = link.find("h3").string
                    course_id = course_link.split("/")[-1:][0][:-7]

                    courses.append((course_name, course_id, course_link))

        print("Page " + str(page) + " (" + str(len(courses)) + ")")

        if last_len == len(courses):
            break

        last_len = len(courses)

    return courses


file = open("courses.txt", "w")

for category in get_categories():
    print(category)
    for course in get_courses(category):
        print(course[0])
        file.write(category[1] + "\0" + course[0] + "\0" + course[1] + "\0" + course[2] + "\n")
    file.flush()


file.close()