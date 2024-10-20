import json
import logging
from tqdm import tqdm
from vk_api import VKAPI
from yandex_disk import YandexDiskAPI

# Настройка логирования
logging.basicConfig(level=logging.INFO)

def save_to_json(data, filename='photos.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    vk_token = input("Введите токен VK: ")
    yandex_token = input("Введите токен Яндекс.Диска: ")
    vk_user_input = input("Введите ID пользователя VK или короткое имя (screen_name): ")
    num_photos = int(input("Сколько фотографий сохранить? (по умолчанию 5): ") or 5)
    
    logging.info("Начало работы программы")

    # Создаем экземпляры API
    vk_api = VKAPI(vk_token)
    yd_api = YandexDiskAPI(yandex_token)

    # Получаем числовой ID пользователя (если введен screen_name)
    vk_user_id = vk_api.get_user_id(vk_user_input)
    if vk_user_id is None:
        logging.error("Не удалось получить ID пользователя.")
        return

    # Получаем фотографии
    logging.info(f"Получаем фотографии для пользователя {vk_user_input}")
    photos = vk_api.get_photos(vk_user_id, count=num_photos)

    if not photos:
        logging.error("Не удалось получить фотографии.")
        return

    # Создаем папку на Яндекс.Диске
    folder_name = f'vk_photos_{vk_user_input}'
    yd_api.create_folder(folder_name)

    photos_info = []

    # Загрузка фотографий
    for photo in tqdm(photos, desc="Загрузка фотографий"):
        # Используем метод для выбора самого большого размера
        max_size = vk_api.get_max_photo_size(photo['sizes'])
        likes = photo['likes']['count']
        file_name = f"{likes}.jpg"
        if any(p['file_name'] == file_name for p in photos_info):
            file_name = f"{likes}_{photo['date']}.jpg"

        photo_url = max_size['url']
        response = vk_api.download_photo(photo_url)
        with open(file_name, 'wb') as f:
            f.write(response.content)

        yd_api.upload_file(file_name, f"{folder_name}/{file_name}")

        photos_info.append({
            "file_name": file_name,
            "size": max_size['type']  # Сохраняем тип размера (например, "z")
        })

    save_to_json(photos_info)
    logging.info("Программа завершена")

if __name__ == "__main__":
    main()
