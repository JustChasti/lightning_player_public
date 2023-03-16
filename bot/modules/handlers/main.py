from aiogram import types
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import api_host, web_app_host
from modules import keyboards
from config import dp, UserStates
from modules.playlists import send_playlists
from modules.requests import get_playlists
from modules.handlers import playlist


@dp.message_handler(state=UserStates.introduction)
async def main_menu(message: types.Message):
    if message.text == 'Добавить песню':
        add_song_keyboard = ReplyKeyboardMarkup()
        data = get_playlists(message.from_id)
        default_playlist = '0'
        for i in data['message']:
            if i['name'] == 'Добавленные':
                default_playlist = i['id']
        add_song_keyboard.row(KeyboardButton(
            text='Добавить',
            web_app=WebAppInfo(
                url=f'{web_app_host}{message.from_id}/{default_playlist}'
            )
        ))
        add_song_keyboard.row(KeyboardButton('Назад'))
        await message.answer(
            'Чтобы добавить песню заполните форму, нажав кнопку добавить',
            reply_markup=add_song_keyboard
        )
        await UserStates.add_music.set()
    elif message.text == 'Мои плейлисты':
        await send_playlists(message)
        await UserStates.get_playlists.set()
        await message.answer(
            text='Выберите вариант',
            reply_markup=keyboards.my_playlists_keyboard
        )
    elif message.text == 'Популярное':
        await message.answer('Эта функция пока недоступна')
        # await UserStates.get_popular.set()
    else:
        await message.answer(
            """Не понял вас, выберите один из предложенных вариантов.
             Я, увы пока не Google LaMDA""",
            reply_markup=keyboards.hello_keyboard
        )


@dp.message_handler(state=UserStates.add_music)
async def add_song(message: types.Message):
    if message.text == 'Назад':
        await UserStates().introduction.set()
        await message.answer(
            text='Главное меню',
            reply_markup=keyboards.hello_keyboard
        )
    elif 'bot-answer000' in message.text:
        await UserStates().introduction.set()
        await message.answer(
            text="""Скачиваю музыку, это займет какое-то время.
             Я отправлю вам все скачанные треки и добавлю
             их в плейлист добавленные"""
        )
        await message.answer(
            text='Главное меню',
            reply_markup=keyboards.hello_keyboard
        )
    else:
        add_song_keyboard = ReplyKeyboardMarkup()
        add_song_keyboard.row(KeyboardButton(
            text='Добавить',
            web_app=WebAppInfo(
                url=f'{api_host}/page/add-songs/{message.from_id}'
            )
        ))
        add_song_keyboard.row(KeyboardButton('Назад'))
        await message.answer(
            text="""Не понял вас, выберите один из предложенных
             вариантов или Напишите 'Назад'""",
            reply_markup=add_song_keyboard
        )


@dp.message_handler(state=UserStates.get_playlists)
async def my_playlists(message: types.Message):
    if message.text == 'Назад':
        await UserStates().introduction.set()
        await message.answer(
            text='Главное меню',
            reply_markup=keyboards.hello_keyboard
        )
    elif message.text == 'Создать новый плейлист':
        await UserStates().add_playlist.set()
        await message.answer(
            text='Введите название плейлиста',
            reply_markup=keyboards.popular_keyboard
        )
    else:
        await message.answer(
            text="""Не понял вас, выберите один из предложенных
             вариантов или Напишите 'Назад'""",
            reply_markup=keyboards.my_playlists_keyboard
        )
