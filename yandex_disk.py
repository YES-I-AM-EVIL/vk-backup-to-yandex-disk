import requests
import logging

class YandexDiskAPI:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, folder_name):
        url = self.base_url + 'resources'
        params = {'path': folder_name}
        response = requests.put(url, headers=self.get_headers(), params=params)
        if response.status_code == 201:
            logging.info(f"Папка '{folder_name}' успешно создана на Яндекс.Диске")
        elif response.status_code == 409:
            logging.info(f"Папка '{folder_name}' уже существует")
        else:
            logging.error(f"Ошибка создания папки: {response.status_code}")

    def upload_file(self, file_path, disk_path):
        url = self.base_url + 'resources/upload'
        params = {'path': disk_path, 'overwrite': 'true'}
        response = requests.get(url, headers=self.get_headers(), params=params)
        upload_url = response.json().get('href', '')
        if upload_url:
            with open(file_path, 'rb') as f:
                upload_response = requests.put(upload_url, files={'file': f})
            if upload_response.status_code == 201:
                logging.info(f"Файл '{file_path}' успешно загружен на Яндекс.Диск")
            else:
                logging.error(f"Ошибка загрузки файла: {upload_response.status_code}")
        else:
            logging.error(f"Ошибка получения ссылки для загрузки файла: {response.status_code}")
