"""
    Description: Combines the list of different stopwords files
    Author: Harshit Varma
"""

with open("smart_stop_list.txt", "r", encoding = "ascii") as f:
    ssl = f.readlines()
ssl = [w.strip() for w in ssl[1:]] # Skip the first line

with open("names.txt", "r", encoding = "ascii") as f:
    names = f.readlines()
names = [w.strip() for w in names[1:]] # Skip the first line

with open("custom.txt", "r", encoding = "ascii") as f:
    custom = f.readlines()
custom = [w.strip() for w in custom[1:]] # Skip the first line


sw = ssl + names + custom

sw = sorted(list(set(sw)))

print("Total unique stopwords: {}".format(len(sw)))

with open("stopwords.txt", "w") as f:
    f.write("# Combined stopwords list\n")
    for w in sw:
        f.write(w + "\n")


