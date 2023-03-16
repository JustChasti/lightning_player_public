from loguru import logger
from db.db import client
from services.vk.download_from_profile import download_profile_music
from services.vk.download_from_playlist import download_album_music
from services.youtube.download_from_youtube import download_youtube_video
from models import SongModel


songs = client['songs']


def create_or_update_song(song: SongModel, artist=None):
    result = songs.find_one({'url': song.url})
    result_h = songs.find_one({'hash': song.hash})
    if result:
        element = {
            "$set": {
                'download_count': result["download_count"] + 1
            }
        }
        songs.update_one({'_id': result["_id"]}, element)
        logger.warning('Duplicate track')
        return result["_id"]
    elif result_h:
        element = {
            "$set": {
                'url': song.url,
                'download_count': result_h["download_count"] + 1
            }
        }
        songs.update_one({'_id': result_h["_id"]}, element)
        logger.warning('Duplicate track')
        return result_h["_id"]
    else:
        element = {
            # 'artist': artist,
            'title': song.title,
            'url': song.url,
            'hash': song.hash,
            'download_count': 1
        }
        id = songs.insert_one(element)
        return id.inserted_id


def get_songs_from_structure(url: str, telegram_id, playlist_name):
    if 'youtu' in url:
        download_youtube_video(url, telegram_id, playlist_name)
    elif 'playlist' in url:
        url = url.split('playlist/')[1]
        download_album_music(url, telegram_id, playlist_name)
    else:
        url = url.split('audios')[1]
        download_profile_music(url, telegram_id, playlist_name)
