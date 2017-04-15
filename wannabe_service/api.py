import json
import io
from urllib import request
from urllib.parse import urlencode
from PIL import Image


class WannabeApi:

    def __init__(self, config):
        self._api_base_path = config.get('WannabeService', 'api_base_path')
        self._api_users_path = config.get('WannabeService', 'api_users_path')
        self._api_pictures_path = config.get('WannabeService', 'api_pictures_path')
        self._app_id = config.get('WannabeService', 'app_id')
        self._api_key = config.get('WannabeService', 'api_key')

    def get_approved_users(self):
        parameters = urlencode({'approved': '1', 'app': self._app_id, 'apikey': self._api_key})
        req = request.Request(self._api_base_path + self._api_users_path + parameters)
        response = request.urlopen(req)
        json_result = json.loads(response.read().decode(response.info().get_content_charset('utf-8')))
        return json_result['users']['user']

    def get_picture_urls(self):
        users = self.get_approved_users()
        result = []
        for user in users:
            for image in user['images']['image']:
                if image['width'] == 320:
                    result.append(image['url'])
        return result

    def download_and_parse_image(self, url):
        req = request.Request(url)
        response = request.urlopen(req)
        image_file = io.BytesIO(response.read())
        return Image.open(image_file)
