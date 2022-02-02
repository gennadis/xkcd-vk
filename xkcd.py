import os
from urllib.parse import unquote, urlsplit

import requests

COMICS_DIR = "/comics"


def get_comics_metadata(comics_id: int) -> dict:
    response = requests.get(f"https://xkcd.com/{comics_id}/info.0.json")
    response.raise_for_status()

    return response.json()


def get_filename(url: str) -> str:
    url_unqoted = unquote(url)
    _, _, path, _, _ = urlsplit(url_unqoted)
    _, filename = os.path.split(path)

    return filename


def fetch_comics(metadata: dict, folder: str) -> tuple[str, str]:
    image_url = metadata["img"]
    title = metadata["alt"]
    filename = get_filename(metadata["img"])
    filepath = os.path.join(folder, filename)

    response = requests.get(image_url)
    response.raise_for_status()

    with open(filepath, "wb") as file:
        file.write(response.content)

    return filepath, title


def get_comics_count() -> int:
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()

    return response.json()["num"]
