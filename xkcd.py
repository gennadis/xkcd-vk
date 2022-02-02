import os
from typing import Optional, Union
from urllib.parse import urljoin, unquote, urlsplit
from dotenv import load_dotenv


import requests


COMICS_JSON_URL = "https://xkcd.com/{}/info.0.json"
VK_API_URL = "https://api.vk.com/method"
COMMUNITY_ID = 210496327


def get_comics_json(comics_id: int) -> Optional[dict]:
    response = requests.get(COMICS_JSON_URL.format(comics_id))
    response.raise_for_status()

    return response.json()


def get_filename(url: str) -> str:
    url_unqoted = unquote(url)
    _, _, path, _, _ = urlsplit(url_unqoted)
    _, filename = os.path.split(path)

    return filename


def fetch_comics(comics_id: int) -> Optional[str]:
    comics_json = get_comics_json(comics_id)
    image_url = comics_json["img"]
    filename = get_filename(image_url)
    comment = comics_json["alt"]

    response = requests.get(image_url)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)

    return comment


def get_upload_server(token: str) -> dict:
    params = {"access_token": token, "v": "5.124", "group_id": COMMUNITY_ID}
    response = requests.get(f"{VK_API_URL}/photos.getWallUploadServer", params=params)
    response.raise_for_status()

    return response.json()["response"]


def push_photo(token: str, filename: str) -> dict:
    with open(filename, "rb") as file:
        url = get_upload_server(token)["upload_url"]
        params = {"access_token": token, "v": "5.124"}
        files = {
            "photo": file,
        }
        response = requests.post(url, params=params, files=files)
        response.raise_for_status()
    return response.json()


def main():
    load_dotenv()
    token = os.getenv("VK_TOKEN")

    # print(get_upload_server(token))
    print(push_photo(token, "python.png"))


if __name__ == "__main__":
    main()
