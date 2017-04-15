from .api import WannabeApi
from os import path as op
from os import listdir
from PIL import Image


class WannabeService:
    def __init__(self, config):
        self._config = config
        self._picture_directory = config.get('WannabeService', 'picture_download_folder')
        self._api = WannabeApi(config)

    def get_approved_users(self):
        return self._api.get_approved_users()

    def get_crew_pictures(self):
        picture_urls = self._api.get_picture_urls()
        downloaded_pictures = {}

        for url in picture_urls:
            filename = url.rsplit('/', 2)[1] + '.png'
            downloaded_pictures[filename] = self._api.download_and_parse_image(url)
        return downloaded_pictures

    def get_crew_picture(self, crew_id, force_update=False):
        if not force_update:
            downloaded_pictures = [op.join(self._picture_directory, f) for f in listdir(self._picture_directory)
                           if op.isfile(op.join(self._picture_directory, f))]
            for picture in downloaded_pictures:
                if crew_id in picture:
                    return Image.open(picture).convert("RGBA")

        picture_urls = self._api.get_picture_urls()
        for url in picture_urls:
            if url.rsplit('/', 2)[1] == crew_id:
                return self._api.download_and_parse_image(url)

    def download_and_save_crew_pictures(self):
        pictures = self.get_crew_pictures()

        for name, picture in pictures.items():
            picture.save(op.join(self._picture_directory, name))
