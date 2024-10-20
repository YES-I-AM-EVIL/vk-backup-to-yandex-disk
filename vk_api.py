import requests
import logging

class VKAPI:
    def __init__(self, token):
        self.token = token
        self.api_version = '5.131'
        self.base_url = 'https://api.vk.com/method/'

    # Получение числового ID пользователя по screen_name
    def get_user_id(self, user_input):
        url = self.base_url + 'users.get'
        params = {
            'user_ids': user_input,
            'access_token': self.token,
            'v': self.api_version
        }
        response = requests.get(url, params=params).json()
        if 'error' in response:
            logging.error(f"Ошибка VK API: {response['error']['error_msg']}")
            return None
        return response['response'][0]['id']

    # Получение фотографий
    def get_photos(self, user_id, count=5):
        url = self.base_url + 'photos.get'
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,  # Чтобы получить количество лайков
            'photo_sizes': 1,
            'count': count,
            'access_token': self.token,
            'v': self.api_version
        }
        response = requests.get(url, params=params).json()
        if 'error' in response:
            logging.error(f"Ошибка VK API: {response['error']['error_msg']}")
            return []
        return response['response']['items']

    # Скачивание фотографии
    def download_photo(self, url):
        logging.info(f"Скачиваем фотографию с URL: {url}")
        return requests.get(url)

    # Метод для выбора максимального размера
    def get_max_photo_size(self, sizes):
        # Ищем размер с типом "z", если он есть
        for size in sizes:
            if size['type'] == 'z':
                return size
        # Если нет "z", выбираем самый большой по ширине и высоте
        return max(sizes, key=lambda s: s['width'] * s['height'])
