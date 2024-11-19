from lighting_system import LightingSystem
from climate_control_system import ClimateControlSystem
from entertainment_system import EntertainmentSystem
from security_system import SecuritySystem

class SmartHomeFacade:
    def __init__(self):
        self.lighting = LightingSystem()
        self.climate = ClimateControlSystem()
        self.entertainment = EntertainmentSystem()
        self.security = SecuritySystem()
    
    def activate_lighting(self):
        self.lighting.start()
    
    def deactivate_lighting(self):
        self.lighting.stop()
    
    def set_climate_control(self, temperature: int):
        self.climate.set_temperature(temperature)
        self.climate.start()
    
    def stop_climate_control(self):
        self.climate.stop()
    
    def play_music(self):
        self.entertainment.start()
    
    def stop_music(self):
        self.entertainment.stop()
    
    def activate_security_system(self):
        self.security.start()
    
    def deactivate_security_system(self):
        self.security.stop()
