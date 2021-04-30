import requests
import json

uploadLink = "https://api.imgur.com/3/upload"
deleteLink = "https://api.imgur.com/3/image/{}"

headers = {}

def upload(image, client_id, naslov=None, opis=None, album=None):
    headers["Authorization"] = f"Client-ID {client_id}"
    files = {
        "image": image,
        "title": (None, naslov),  # https://stackoverflow.com/a/35974071
        "description": (None, opis),
        "album": (None, album)
    }

    response = requests.post(uploadLink, headers=headers, files=files)
    jsonResponse = json.loads(response.text)
    if not jsonResponse["success"]:
        return

    return jsonResponse["data"]["id"], jsonResponse["data"]["deletehash"]

def delete(client_id, deleteHash):
    headers["Authorization"] = f"Client-ID {client_id}"
    response = requests.delete(deleteLink.format(deleteHash), headers=headers)
    jsonResponse = json.loads(response.text)
    if not jsonResponse["success"]:
        print("au nece ")
    else:
        print("aa dobroe")
