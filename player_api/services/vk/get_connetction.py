import vk_api
from vk_api import audio
from config import vk_pool
from services.decorators import default_decorator
from loguru import logger


class LoginError(Exception):
    pass


@default_decorator('Vk connection ERROR!!!')
def connect():
    for i in vk_pool:
        try:
            vk_session = vk_api.VkApi(login=i['login'], password=i['password'])
            vk_session.auth()
            vk = vk_session.get_api()
            vk_audio = audio.VkAudio(vk_session)
            return vk_audio
        except Exception as e:
            logger.warning(f'cant connect to {i["login"]}')
    raise LoginError
