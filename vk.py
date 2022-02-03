import requests

VK_API_URL = "https://api.vk.com/method"
VK_API_VERSION = "5.124"


def get_upload_url(token: str, group_id: int) -> str:
    url = f"{VK_API_URL}/photos.getWallUploadServer"
    params = {
        "access_token": token,
        "v": VK_API_VERSION,
        "group_id": group_id,
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()

    upload_url = response.json()["response"]["upload_url"]

    return upload_url


def upload_photo(token: str, upload_url: str, filename: str) -> dict:
    with open(filename, "rb") as file:
        params = {"access_token": token, "v": VK_API_VERSION}
        files = {"photo": file}

        response = requests.post(url=upload_url, params=params, files=files)
        response.raise_for_status()

    return response.json()


def save_photo(token: str, upload_params: dict, group_id: int) -> tuple[int, int]:
    url = f"{VK_API_URL}/photos.saveWallPhoto"
    params = {
        "access_token": token,
        "v": VK_API_VERSION,
        "group_id": group_id,
        "photo": upload_params["photo"],
        "server": upload_params["server"],
        "hash": upload_params["hash"],
    }

    response = requests.post(url=url, params=params)
    response.raise_for_status()

    [saved_file_metadata] = response.json()["response"]
    photo_id = saved_file_metadata["id"]
    owner_id = saved_file_metadata["owner_id"]

    return photo_id, owner_id


def publish_wall_post(
    token: str, group_id: int, message: str, owner_id: str, photo_id: str
):
    url = f"{VK_API_URL}/wall.post"
    params = {
        "access_token": token,
        "v": VK_API_VERSION,
        "owner_id": -group_id,
        "from_group": 1,
        "message": message,
        "attachments": f"photo{owner_id}_{photo_id}",
    }

    response = requests.post(url=url, params=params)
    response.raise_for_status()

    post_id = response.json()["response"]["post_id"]
    return post_id
