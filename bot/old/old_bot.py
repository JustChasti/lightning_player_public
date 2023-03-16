from config import bot
from modules import requests
from bot.modules import old_keyboards
from bot.modules import old_playlists


@bot.message_handler(commands=['help', 'start'])
def start_message(message):
    text = """
Привет, я ⚡️ Music Storm - твой музыкальный бот!\n
Я могу сохранять для тебя музыку из:\n
1) ВК - открытые страницы и плейлисты\n
2) Youtube видео\n
В отличии от многих других ботов, я сохраняю твою музыку в плейлисты.\n
В будущем ты сможешь делиться ими со своими друзьями и получать рекомендации исходя из твоих предпочтений.\n
Чтобы добавить музыку, необходимо выбрать плейлист, в который она будет добавлена.\n
По умолчанию доступен плейлист добавленные, ты можешь использовать его или создать свой.\n
Для добавления трека необходимо лишь нажать кнопку добавить и отправить ссылку на интересующий ресурс.\n
И если песня доступна всем желающим она будет добавлена к тебе в плейлист.\n
"""
    requests.create_user(message.chat.id)
    requests.create_playlist(message.chat.id, 'Добавленные')
    img = open('images/lightning.jpg', 'rb')
    bot.send_photo(
        message.chat.id,
        img,
        text,
        reply_markup=old_keyboards.start_keyboard
    )


@bot.message_handler(content_types=['text'])
def raw_text_handler(message):
    if message.text == 'Мои плейлисты':
        data = requests.get_playlists(message.chat.id)['message']
        old_playlists.send_playlists(message, data)
    elif message.text == 'Назад':
        text = 'вы в главном меню бота'
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=old_keyboards.start_keyboard
        )
    else:
        text = 'Такой комманды я не знаю'
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=old_keyboards.start_keyboard
        )


@bot.callback_query_handler(func=lambda call: True)
def playlist_worker(call):
    element_id, element, func = call.data.split('/')
    if func == 'add':
        text = f"""
При добавлении песен со страниц или плейлистов в ВК, убедись,\n
что профиль является ОТКРЫТЫМ, а его музыка ДОСТУПНА всем желающим:
Ссылки обрабатываются в таких форматах:
1) Ссылка на страницу (для получения такой ссылки зайдите в раздел музыка через версию для браузера, либо замените в данной ссылке цифры на свой id ВК. Id - это не короткая буквенная ссылка !): https://vk.com/audios111111111 \n
2) Ссылка на плейлист: https://vk.com/music/playlist/111111111_2 \n
3) Ссылка на видео youtube: https://www.youtube.com/watch?v= \n
"""
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=old_keyboards.playlists_keyboard
        )
        bot.register_next_step_handler(
            call.message,
            old_playlists.insert_to_playlist,
            element_id
        )
    elif func == 'get':
        data = requests.get_playlist_songs(call.message.chat.id, element_id)
        text = f"Плейлист: {data['name']}\nОписание: {data['description']}\n"
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=old_keyboards.start_keyboard
        )
        text = f"{data['message']}"
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=old_keyboards.start_keyboard
        )
    elif func == 'del':
        bot.send_message(
            call.message.chat.id,
            'Вы уверены?',
            reply_markup=old_keyboards.yes_not_keyborad
        )
        bot.register_next_step_handler(
            call.message,
            old_playlists.deletion_confirm,
            element_id
        )

    elif func == 'delete':
        result = requests.delete_song(playlist=element, song=element_id)
        if result:
            text = f"Песня будет удалена из этого плейлиста"
        else:
            text = f"Ошибка, попробуйте позже"
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=old_keyboards.start_keyboard
        )
    else:
        print(call.data)
        text = 'Такой комманды я не знаю'
        bot.send_message(
            call.message.chat.id,
            text,
            reply_markup=old_keyboards.start_keyboard
        )


bot.infinity_polling()
