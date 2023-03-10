from fastapi import FastAPI, APIRouter
from one_app.routers.memes import router as memes_router


def create_app() -> FastAPI:
    meme_app = FastAPI(title="One app")

    router = APIRouter()

    router.include_router(memes_router, prefix="/memes")
    meme_app.include_router(router)
    return meme_app


app = create_app()
