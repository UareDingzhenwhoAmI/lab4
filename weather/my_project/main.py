from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from weather import load_city_coordinates, fetch_weather_for_all

app = FastAPI()
templates = Jinja2Templates(directory="my_project/templates")


# 异步函数 get_weather, load_city_coordinates, fetch_weather_for_all 放在这里

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/update")
async def fetch_weather():
    cities = await load_city_coordinates('europe.csv')
    weather_results = await fetch_weather_for_all(cities)
    return weather_results

# 其他API端点...
