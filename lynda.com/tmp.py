
terms = ["data science", "big data", "hadoop", "python", "data mining", "text mining", "deep learning", "blender",
         "unity", "zbrush", "substance"]

for line in open("courses.txt"):

    category, name, course_id, url = line.split("\0")

    for term in terms:
        if term in name.lower():
            print(url[:-1])