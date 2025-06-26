import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, FileResponse
from starlette.staticfiles import StaticFiles

from router import lottery, bot, auth



app = FastAPI()
app.include_router(router=lottery.router)
app.include_router(router=bot.router)
app.include_router(router=auth.router)

app.mount('/front', StaticFiles(directory='front', html=True), name='front')

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:80",
    "http://127.0.0.1:80",
    "http://127.0.0.1",
    "http://31.207.44.172",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get():
    return FileResponse("front/index.html", media_type="text/html")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
