from datetime import datetime
from bson.json_util import dumps
import requests
from zipfile import ZipFile

from config import core_host
from models import UserModel
from db.db import client
from services.decorators import default_decorator, files_decorator
from services.pikasender import send_telegram_text


@default_decorator('User find error, open logs to get more info')
def find_user(telegram_id):
    users = client['users']
    user = users.find_one({
        'telegram_id': telegram_id
    })
    if user:
        return True
    else:
        return False


@default_decorator('User creation error, open logs to get more info')
def creation(user: UserModel):
    users = client['users']
    users.insert_one({
        'telegram_id': user.telegram_id,
        'premium': False,
        'last_visit': datetime.today()
    })
    return {'message': "creation succesfull"}


@default_decorator('User playlists info error')
def get_user_playlists(telegram_id):
    playlists = client['playlists']
    playlists = playlists.find({
            'telegram_id': telegram_id,
    })
    message = []
    for i in playlists:
        message.append({
            'id': str(i['_id']),
            'name': i['name']
        })
    return {'message': message}


@default_decorator('User send info error')
def send_all(mail):
    users = client['users'].find({})
    for i in users:
        send_telegram_text(i['telegram_id'], mail.text)


@files_decorator('Get dump error')
def get_dump(collections):
    with ZipFile('dump.zip', 'w') as myzip:
        for c in collections:
            data = client[c].find({})
            with open(f'{c}.json', 'w') as file:
                file.write('[')
                for document in data:
                    file.write(dumps(document))
                    file.write(',')
                file.write(']')
            myzip.write(f"{c}.json")

    return 'dump.zip'


@files_decorator('Get logs error')
def get_logs():
    response = requests.get(f'{core_host}/getlogs')
    with open('core_logs.log', 'wb') as file:
        file.write(response.content)
    with ZipFile('logs.zip', 'w') as myzip:
        myzip.write(f"test.log")
        myzip.write(f"core_logs.log")
    return 'logs.zip'
