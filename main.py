import os
import random

from dotenv import load_dotenv

import vk
import xkcd

COMICS_DIR = "./comics"


def main():
    os.makedirs(COMICS_DIR, exist_ok=True)

    load_dotenv()
    token = os.getenv("VK_TOKEN")
    group_id = int(os.getenv("VK_GROUP_ID"))

    random_id = random.randint(1, xkcd.get_comics_count())
    comics_metadata = xkcd.get_comics_metadata(random_id)
    filepath, title = xkcd.fetch_comics(comics_metadata, COMICS_DIR)

    upload_server_url = vk.get_upload_server(token, group_id)
    upload_params = vk.upload_photo(token, upload_server_url, filepath)
    photo_id, owner_id = vk.save_photo(token, upload_params, group_id)
    post_id = vk.publish_wall_post(token, group_id, title, owner_id, photo_id)

    print(f"https://vk.com/club210496327?w=wall-210496327_{post_id}")


if __name__ == "__main__":
    main()
