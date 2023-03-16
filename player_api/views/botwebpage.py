from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from services.users import find_user
from services.playlists import insertion
from models import LinkModel

from fastapi.templating import Jinja2Templates


web_page_router = APIRouter()

templates = Jinja2Templates(directory="templates")


class LinksForm:
    def __init__(self, request: Request) -> None:
        self.requst = request
        self.vk_profile = None
        self.vk_playlist = None
        self.vk_youtube = None

    async def load_data(self):
        data = await self.requst.form()
        self.vk_profile = data.get('vk_profile')
        self.vk_playlist = data.get('vk_playlist')
        self.vk_youtube = data.get('vk_youtube')

    async def get_result(self):
        if not self.vk_profile and not self.vk_playlist and not self.vk_youtube:
            return 0
        elif self.vk_profile and not self.vk_playlist and not self.vk_youtube:
            return 1
        elif not self.vk_profile and self.vk_playlist and not self.vk_youtube:
            return 2
        elif not self.vk_profile and not self.vk_playlist and self.vk_youtube:
            return 3
        else:
            return 4


@web_page_router.get('/page/add-songs/{telegram_id}/{playlist_id}')
async def add_songs(request: Request, telegram_id, playlist_id):
    if not find_user(telegram_id):
        return JSONResponse({'info': 'cant find this user'})
    else:
        return templates.TemplateResponse(
            "song-request.html",
            {"request": request, "id": f'{telegram_id}/{playlist_id}'}
        )


@web_page_router.post('/page/add-songs/{telegram_id}/{playlist_id}')
async def add_songs(request: Request, telegram_id, playlist_id):
    form = LinksForm(request)
    await form.load_data()
    result = await form.get_result()
    if result == 0:
        return templates.TemplateResponse(
            "web-response.html",
            {"request": request, "message": f'Ни одно из полей не заполненно'}
        )
    elif result == 1:
        link = LinkModel(
            telegram_id=telegram_id,
            playlist_id=playlist_id,
            url=form.vk_profile
        )
        data = insertion(link)['message']
        if data == 'music starts downloading':
            return templates.TemplateResponse(
                "web-response.html",
                {"request": request, "message": f'Если ваши аудио являются открытыми для всех, то скоро, в порядке вашей очереди музыка будет скачана, добавленна в соответствующий плейлист и отправленна вам.'}
            )
        else:
            return templates.TemplateResponse(
                "web-response.html",
                {"request": request, "message": f'Произошла ошибка : {data}'}
            )
    elif result == 2:
        link = LinkModel(
            telegram_id=telegram_id,
            playlist_id=playlist_id,
            url=form.vk_playlist
        )
        data = insertion(link)['message']
        if data == 'music starts downloading':
            return templates.TemplateResponse(
                "web-response.html",
                {"request": request, "message": f'Если ваши аудио являются открытыми для всех, то скоро, в порядке вашей очереди музыка будет скачана, добавленна в соответствующий плейлист и отправленна вам.'}
            )
        else:
            return templates.TemplateResponse(
                "web-response.html",
                {"request": request, "message": f'Произошла ошибка : {data}'}
            )
    elif result == 3:
        link = LinkModel(
            telegram_id=telegram_id,
            playlist_id=playlist_id,
            url=form.vk_youtube
        )
        data = insertion(link)['message']
        if data == 'music starts downloading':
            return templates.TemplateResponse(
                "web-response.html",
                {"request": request, "message": f'Если видео не является слишком длинным, то скоро, в порядке вашей очереди оно будет скачано, преобразованно в музыку, добавленно в соответствующий плейлист и отправленно вам.'}
            )
        else:
            return templates.TemplateResponse(
                "web-response.html",
                {"request": request, "message": f'Произошла ошибка : {data}'}
            )
    elif result == 4:
        return templates.TemplateResponse(
            "web-response.html",
            {"request": request, "message": f'ОШИБКА: вы заполнили слишком много полей'}
        )
