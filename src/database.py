import csv

# TODO: You will want to replace all of the code below. It is just to show you
# an example of reading the CSV files where you will get the data to complete
# the assignment.

print("reading movies")

with open("movies.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)
    movies = {}
    for row in reader:
        key = row[0]
        values = row[1:]
        movies[key] = values

with open("characters.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)
    characters = {}
    for row in reader:
        key = row[0]
        values = row[1:]
        characters[key] = values

with open("conversations.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)
    conversations = {}
    for row in reader:
        key = row[0]
        values = row[1:]
        conversations[key] = values

with open("lines.csv", mode="r", encoding="utf8") as csv_file:
    reader = csv.reader(csv_file)
    lines = {}
    for row in reader:
        key = row[0]
        values = row[1:]
        lines[key] = values