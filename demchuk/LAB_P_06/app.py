from fastapi import FastAPI
from pydantic import BaseModel

# Імпортуємо ваші класи (наприклад, фасад і підсистеми) з попереднього коду
from facade import SmartHomeFacade, LightingSystem, SecuritySystem, ClimateControlSystem, EntertainmentSystem
from bridge import Light, Switch

# Створення FastAPI додатку
app = FastAPI()

# Інтеграція Bridge у фасад через пульт
light = Light()
light_switch = Switch(light)

class IntegratedLightingSystem:
    def turnOnLights(self):
        light_switch.turn_on()

    def turnOffLights(self):
        light_switch.turn_off()

    def setBrightness(self, level):
        print(f"Яскравість встановлена на рівень {level}.")

# Ініціалізація фасаду з новою інтегрованою системою освітлення
integrated_lighting = IntegratedLightingSystem()
smart_home = SmartHomeFacade(
    lighting=integrated_lighting,
    security=SecuritySystem(),
    climate=ClimateControlSystem(),
    entertainment=EntertainmentSystem()
)

# Pydantic моделі для параметрів API
class ClimateRequest(BaseModel):
    temperature: float

class LightingRequest(BaseModel):
    action: str
    brightness: int = None

# Створення ендпоінтів API

@app.post("/activate-security")
async def activate_security():
    smart_home.activateSecuritySystem()
    return {"message": "Система безпеки активована"}

@app.post("/deactivate-security")
async def deactivate_security():
    smart_home.deactivateSecuritySystem()
    return {"message": "Система безпеки деактивована"}

@app.post("/set-climate")
async def set_climate(request: ClimateRequest):
    smart_home.setClimateControl(request.temperature)
    return {"message": f"Температура встановлена на {request.temperature}°C"}

@app.post("/control-lighting")
async def control_lighting(request: LightingRequest):
    if request.action == "on":
        smart_home.controlLighting("on", brightness=request.brightness)
    elif request.action == "off":
        smart_home.controlLighting("off")
    return {"message": f"Освітлення {request.action} з яскравістю {request.brightness}"}

@app.post("/play-music")
async def play_music():
    smart_home.playMusic()
    return {"message": "Музика увімкнена"}

@app.post("/stop-music")
async def stop_music():
    smart_home.stopMusic()
    return {"message": "Музика вимкнена"}
