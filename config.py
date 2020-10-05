import json


data = None


def Load():
    global data
    with open('config.json', 'r', encoding='utf8') as file:
        data = json.load(file)


def Save():
    global data
    with open('config.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=2)
