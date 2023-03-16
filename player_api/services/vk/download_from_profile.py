import hashlib
from loguru import logger
from services.pikasender import send
from db.db import client
from services.vk.get_connetction import connect


playlists = client['playlists']


def download_profile_music(user_id, telegram_id, playlist_name):
    try:
        vk_audio = connect()
        for i in vk_audio.get(owner_id=user_id):
            try:
                hash_name = hashlib.sha256(str.encode(i["title"])).hexdigest()
                filename = f'{telegram_id}_{hash_name}'
                logger.info(f"filename {filename} sended to pika")
                message = {
                    'filename': filename,
                    'url': i["url"],
                    'songname': i["title"],
                    'telegram_id': telegram_id,
                    'playlist_id': playlist_name,
                    'song_id': hash_name
                }
                send(message)
            except Exception as e:
                logger.exception(e)
    except Exception as e:
        logger.exception(e)
        logger.error('Vk connection error')
