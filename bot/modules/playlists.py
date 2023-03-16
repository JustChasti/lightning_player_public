from modules.decorators import default_decorator
from modules.requests import get_playlists
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@default_decorator('Sending playlists error')
async def send_playlists(message: Message):
    data = get_playlists(message.from_id)
    for i in data['message']:
        playlist_out_keyboard = InlineKeyboardMarkup()
        playlist_out_keyboard.add(InlineKeyboardButton(
            'Вывести плейлист',
            callback_data=f"get{i['id']}"
        ))
        playlist_out_keyboard.add(InlineKeyboardButton(
            'Добавить песни',
            callback_data=f"add{i['id']}"
        ))
        playlist_out_keyboard.add(InlineKeyboardButton(
            'Удалить плейлист',
            callback_data=f"del{i['id']}"
        ))
        await message.answer(
            text=i['name'],
            reply_markup=playlist_out_keyboard
        )
