from aiogram import types
from loguru import logger
from config import dp, UserStates, web_app_host
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from modules.requests import get_playlist_songs, delete_playlist, delete_song
from modules.requests import create_playlist
from modules import keyboards


@dp.callback_query_handler(lambda callback_query: 'get' in callback_query.data, state=UserStates.get_playlists)
async def get_playlist_handler(callback_query: types.CallbackQuery):
    item_id = str(callback_query.data)[3:]
    data = get_playlist_songs(callback_query.message.chat.id, item_id)
    await callback_query.message.answer(data['message'])


@dp.callback_query_handler(lambda callback_query: 'add' in callback_query.data, state=UserStates.get_playlists)
async def add_playlist_handler(callback_query: types.CallbackQuery):
    item_id = str(callback_query.data)[3:]
    add_song_keyboard = ReplyKeyboardMarkup()
    logger.info(f'{web_app_host}{callback_query.from_user["id"]}/{item_id}')
    add_song_keyboard.row(KeyboardButton(
        text='Добавить',
        web_app=WebAppInfo(
            url=f'{web_app_host}{callback_query.from_user["id"]}/{item_id}'
        )
    ))
    add_song_keyboard.row(KeyboardButton('Назад'))
    await callback_query.message.answer(
        'Чтобы добавить песню заполните форму, нажав кнопку добавить',
        reply_markup=add_song_keyboard
    )
    await UserStates.add_music.set()


@dp.callback_query_handler(lambda callback_query: 'del' in callback_query.data, state=UserStates.get_playlists)
async def del_playlist_handler(callback_query: types.CallbackQuery):
    item_id = str(callback_query.data)[3:]
    if '/' in item_id:
        data = item_id.split('/')
        answer = delete_song(data[1], data[0])
        if answer:
            await callback_query.message.answer(f'песня была удалена')
        else:
            await callback_query.message.answer(f'ошибка удаления песни')

    else:
        answer = delete_playlist(item_id)
        if answer:
            await callback_query.message.answer(f'плейлист был удален')
        else:
            await callback_query.message.answer(f'ошибка удаления плейлиста')


@dp.message_handler(state=UserStates.add_playlist)
async def create_new_playlist(message: types.Message):
    if message.text == 'Назад':
        await UserStates().get_playlists.set()
        await message.answer(
            text='Выберите вариант',
            reply_markup=keyboards.my_playlists_keyboard
        )
    else:
        answer = create_playlist(message.from_id, message.text)
        if answer:
            await message.answer(
                text=f'плейлист {message.text} был создан',
                reply_markup=keyboards.my_playlists_keyboard
            )
        else:
            await message.answer(
                text=f'ошибка создания плейлиста {message.text}',
                reply_markup=keyboards.my_playlists_keyboard
            )
