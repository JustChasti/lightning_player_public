import pika
import json
from config import bot_token
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from config import rabbit_host, queue_url_name


def send(message):
    connection = pika.BlockingConnection(
                pika.ConnectionParameters(rabbit_host)
            )
    channel = connection.channel()
    channel.queue_declare(queue=queue_url_name)
    channel.confirm_delivery()
    channel.basic_publish(
        exchange='',
        routing_key=queue_url_name,
        body=json.dumps(message)
    )
    connection.close()


def send_to_telegram(telegram_id, music_bytes, title, song_id, playlist_id):
    try:
        bot = telebot.TeleBot(bot_token)
        callback_keyboard = InlineKeyboardMarkup()
        button0 = InlineKeyboardButton(
            text='Удалить',
            callback_data=f"del{song_id}/{playlist_id}"
        )
        callback_keyboard.row(button0)
        if len(str(song_id)) == 24:
            bot.send_audio(
                telegram_id,
                title=title,
                audio=music_bytes,
                reply_markup=callback_keyboard
            )
        else:
            bot.send_audio(
                telegram_id,
                title=title,
                audio=music_bytes
            )
    except Exception as e:
        logger.exception(e)


def send_telegram_text(telegram_id, text):
    try:
        bot = telebot.TeleBot(bot_token)
        bot.send_message(telegram_id, text)
    except Exception as e:
        logger.exception(e)
