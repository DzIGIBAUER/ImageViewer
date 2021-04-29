import configparser
import requests
import json

uploadLink = "https://api.imgur.com/3/upload"
deleteLink = "https://api.imgur.com/3/image/{}"

headers = {}

def clientID():
    config = configparser.ConfigParser()
    config.read("config.cfg")
    try:
        APIConfig = config["API"]
    except KeyError:
        return False
    return APIConfig.get("ClientID")

def namestiClientID():
    id_ = clientID()
    if not id_:
        print("Nema client id")
        return False
    headers["Authorization"] = f"Client-ID {id_}"

def upload(image, naslov=None, opis=None, album=None):
    files = {
        "image": image,
        "title": (None, naslov),  # https://stackoverflow.com/a/35974071
        "description": (None, opis),
        "album": (None, album)
    }

    if not namestiClientID():
        return

    response = requests.post(uploadLink, headers=headers, files=files)
    jsonResponse = json.loads(response.text)
    if not jsonResponse["success"]:
        return

    return jsonResponse["data"]["id"], jsonResponse["data"]["deletehash"]

def delete(deleteHash):
    if not namestiClientID():
        return

    response = requests.delete(deleteLink.format(deleteHash), headers=headers)
    jsonResponse = json.loads(response.text)
    if not jsonResponse["success"]:
        print("au nece ")
    else:
        print("aa dobroe")
