from fastapi import APIRouter
from fastapi.responses import FileResponse
from zipfile import ZipFile
from loguru import logger

info_router = APIRouter()


def files_decorator(errormessage: str):
    def internal_decorator(function):
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                logger.exception(e)
                logger.error(errormessage)
                open('empty.txt', 'a').close()
                return 'empty.txt'
        return wrapper
    return internal_decorator


@info_router.get('/getlogs', response_class=FileResponse)
async def get_logs():
    filename = get_api_logs()
    return FileResponse(path=filename, filename=filename)


@files_decorator('Get logs error')
def get_api_logs():
    with ZipFile('logs.zip', 'w') as myzip:
        myzip.write(f"test.log")
    return 'logs.zip'
