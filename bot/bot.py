from config import dp, UserStates
from aiogram import executor, types
from modules import requests
from modules import keyboards
from modules.handlers import main


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    requests.create_user(message.chat.id)
    requests.create_playlist(message.chat.id, 'Добавленные')
    img = open('images/lightning.jpg', 'rb')
    text = """
    Привет, я ⚡️ Music Storm - твой музыкальный бот!\n
    Я могу сохранять для тебя музыку из:\n
    1) ВК - открытые страницы и плейлисты\n
    2) Youtube видео\n
    В отличии от многих других ботов, я сохраняю твою музыку в плейлисты.\n
    В будущем ты сможешь делиться ими со своими друзьями и получать рекомендации исходя из твоих предпочтений.\n
    """
    await message.answer_photo(
        photo=img,
        caption=text,
        reply_markup=keyboards.hello_keyboard
    )
    await UserStates.introduction.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
