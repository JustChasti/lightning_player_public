import requests
from config import api_host
from loguru import logger
from modules.decorators import default_decorator


@default_decorator('user creation error')
def create_user(telegram_id):
    data = {
        'telegram_id': telegram_id
    }
    response = requests.post(f'{api_host}user/create', json=data)
    logger.info(response.status_code)


@default_decorator('playlist creation error')
def create_playlist(telegram_id, name, description=''):
    data = {
        'telegram_id': telegram_id,
        'name': name,
        'description': description
    }
    response = requests.post(f'{api_host}playlist/create', json=data)
    logger.info(response.status_code)
    if response.status_code == 200:
        return True
    else:
        return False


@default_decorator('playlist get error')
def get_playlists(telegram_id):
    response = requests.get(f'{api_host}user/get_playlists/{telegram_id}')
    return response.json()


@default_decorator('playlist get songs error')
def get_playlist_songs(telegram_id, item_id):
    response = requests.get(f'{api_host}get/{telegram_id}/{item_id}')
    return response.json()


@default_decorator('playlist get info error')
def get_playlist_info(telegram_id, item_id):
    response = requests.get(f'{api_host}info/{telegram_id}/{item_id}')
    return response.json()


@default_decorator('playlist insert error')
def insert_to_playlist(telegram_id, playlist_id, url):
    data = {
        'telegram_id': telegram_id,
        'playlist_id': playlist_id,
        'url': url
    }
    response = requests.patch(f'{api_host}playlist/insert', json=data)
    return response


@default_decorator('song delete error')
def delete_song(playlist, song):
    response = requests.delete(f'{api_host}delete/{playlist}/{song}')
    if response.status_code == 200:
        return True
    else:
        return False


@default_decorator('playlist delete error')
def delete_playlist(playlist):
    response = requests.delete(f'{api_host}delete_playlist/{playlist}')
    if response.status_code == 200:
        return True
    else:
        return False
