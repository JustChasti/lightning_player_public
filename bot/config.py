from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv


load_dotenv()

token = os.getenv('TOKEN')
api_host = os.getenv('CORE_HOST')
web_app_host = str(os.getenv('WEB_APP')) + '/page/add-songs/'


class UserStates(StatesGroup):
    introduction = State()
    add_music = State()
    get_playlists = State()
    get_popular = State()
    add_playlist = State()


memory_storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=memory_storage)
