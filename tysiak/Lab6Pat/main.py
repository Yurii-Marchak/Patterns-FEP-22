from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from smart_home_facade import SmartHomeFacade
#cd 6
#uvicorn main:app --reload --port 8080
app = FastAPI()
templates = Jinja2Templates(directory="templates")
smart_home = SmartHomeFacade()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/lighting/start")
@app.get("/lighting/start")  # Додаємо підтримку GET запитів для тестування
def activate_lighting():
    smart_home.activate_lighting()
    return {"message": "There is light🤩"}

@app.post("/lighting/stop")
@app.get("/lighting/stop")  # Додаємо підтримку GET запитів для тестування
def deactivate_lighting():
    smart_home.deactivate_lighting()
    return {"message": "There is no light😭"}


@app.post("/entertainment/play")
@app.get("/entertainment/play")  # Додаємо підтримку GET запитів для тестування
def play_music():
    smart_home.play_music()
    return {"message": "Playing music🎶"}

@app.post("/entertainment/stop")
@app.get("/entertainment/stop")  # Додаємо підтримку GET запитів для тестування
def stop_music():
    smart_home.stop_music()
    return {"message": "Music stopped😶‍🌫️"}

@app.post("/security/activate")
@app.get("/security/activate")  # Додаємо підтримку GET запитів для тестування
def activate_security():
    smart_home.activate_security_system()
    return {"message": "Security system activated😎"}

@app.post("/security/deactivate")
@app.get("/security/deactivate")  # Додаємо підтримку GET запитів для тестування
def deactivate_security():
    smart_home.deactivate_security_system()
    return {"message": "Security system deactivated🫣"}

@app.post("/climate/set")
@app.get("/climate/set")  # Додаємо підтримку GET запитів для тестування
def set_climate(temperature: int):
    smart_home.set_climate_control(temperature)
    return {"message": f"Climate set to {temperature}°C🌡️"}
