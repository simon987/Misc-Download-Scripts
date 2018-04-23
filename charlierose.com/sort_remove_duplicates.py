import csv
import os

rows = []

with open("links.csv", 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if row not in rows:
            rows.append(row)


def get_key(item):
    return int(os.path.split(item[0])[1])

sorted_list = sorted(rows, key=get_key)

with open('links_sorted.csv', 'a') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in sorted_list:
        csv_writer.writerow(row)
