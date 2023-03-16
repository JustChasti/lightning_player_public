from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


hello_keyboard = ReplyKeyboardMarkup()
hello_keyboard.row(KeyboardButton('Добавить песню'))
hello_keyboard.row(KeyboardButton('Мои плейлисты'))
hello_keyboard.row(KeyboardButton('Популярное'))

my_playlists_keyboard = ReplyKeyboardMarkup()
my_playlists_keyboard.row(KeyboardButton('Создать новый плейлист'))
my_playlists_keyboard.row(KeyboardButton('Назад'))

popular_keyboard = ReplyKeyboardMarkup()
popular_keyboard.row(KeyboardButton('Назад'))
