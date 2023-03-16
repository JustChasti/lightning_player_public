from fastapi import FastAPI
from loguru import logger
from views.main import main_router
from views.info import info_router
import uvicorn


app = FastAPI()
logger.add("test.log", rotation="100 MB")
app.include_router(main_router)
app.include_router(info_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
