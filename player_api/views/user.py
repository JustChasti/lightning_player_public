from fastapi import APIRouter
from fastapi.responses import JSONResponse, FileResponse
from services import users
from models import UserModel, AllMailModel, AdminModel
import os


user_router = APIRouter()


@user_router.post('/user/create', response_class=JSONResponse)
async def create_user(user: UserModel):
    return users.creation(user)


@user_router.post('/user/send', response_class=JSONResponse)
async def send_to_all(mail: AllMailModel):
    return users.send_all(mail)


@user_router.post('/getbasedump', response_class=FileResponse)
async def get_dump(dump: AdminModel):
    collections = [
        'users',
        'playlists',
        'songs'
    ]
    filename = users.get_dump(collections)
    try:
        return FileResponse(path=filename, filename=filename)
    finally:
        for i in collections:
            try:
                os.remove(f'{i}.json')
            except Exception as e:
                pass


@user_router.post('/getlogs', response_class=FileResponse)
async def get_logs(logs: AdminModel):
    filename = users.get_logs()
    return FileResponse(path=filename, filename=filename)


@user_router.get('/user/get_playlists/{telegram_id}', response_class=JSONResponse)
async def get_playlist(telegram_id: str):
    return users.get_user_playlists(telegram_id)
