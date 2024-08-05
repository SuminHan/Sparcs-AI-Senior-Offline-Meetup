from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse


import news_crawler
import news_summarizer

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/login/{singer_name}/{user_name}/{latitude}/{longitude}")
# def submit(request: Request):
#     print(request)
#     return {'success': True}

# @app.get("/geocode/{lat}/{lon}")
# def submit(request: Request):
#     addr = ''
#     return {'result': addr}



import image_uploader
@app.post("/upload-image/{uid}/{comment}")
async def upload_image(file: UploadFile, uid: str, comment: str):
    return await image_uploader.upload_file(file, uid, comment)




###############

import fanevent_loader
@app.get("/fanevent/{singer_name}/{region}")
def submit(request: Request, singer_name: str, region: str):
    return fanevent_loader.fanevent_search(singer_name, region)

@app.get("/event-checkins/{uid}")
def submit(request: Request, uid: str):
    return fanevent_loader.event_checkins(uid)


import naver_reversegeo
@app.get("/geocode/{lat}/{lon}")
def geocode(request: Request, lat: float, lon: float):
    return naver_reversegeo.naver_geocode(lat, lon)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

import elevenlabs
from pydantic import BaseModel


class Item(BaseModel):
    text: str

@app.post("/herovoice")
def index(item: Item):
    return elevenlabs.hero_voice_test(item.text)

@app.post("/againvoice")
def index(item: Item):
    return elevenlabs.again_voice_test(item.text)


@app.post("/submit")
def submit(request: Request, name: str = Form(...)):
    return RedirectResponse(url=f"/news/{name}")

@app.get("/result/{name}")
def result(request: Request, name: str):
    return templates.TemplateResponse("result.html", {"request": request, "name": name})

@app.get("/news/{name}")
def news_result(name: str):
    return news_crawler.crawl(name)

@app.get("/news-summary/{name}")
def news_summary_result(name: str):
    news_crawler.crawl(name)
    return {"result": news_summarizer.clova_summarize(name)}

@app.get("/news-summary-aegyo/{name}/{name2}")
def news_summary_aegyo_result(name: str, name2: str):
    text = news_summarizer.clova_summarize_aegyo(name, name2)
    if name == '임영웅':
        elevenlabs.hero_voice_test(text)
    else:
        elevenlabs.again_voice_test(text)
    return {"result": text}

if __name__ == '__main__':
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')

    args = parser.parse_args()

    if args.test:
        uvicorn.run(app, host='0.0.0.0', port=5000, log_level="debug", timeout_keep_alive=1000)
