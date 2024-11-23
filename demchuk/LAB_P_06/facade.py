class LightingSystem:
    def turnOnLights(self):
        print("Освітлення увімкнено.")

    def turnOffLights(self):
        print("Освітлення вимкнено.")

    def setBrightness(self, level):
        print(f"Яскравість встановлена на рівень {level}.")

class SecuritySystem:
    def armSystem(self):
        print("Система безпеки активована.")

    def disarmSystem(self):
        print("Система безпеки вимкнена.")

    def triggerAlarm(self):
        print("Тривога! Тривога!")

class ClimateControlSystem:
    def setTemperature(self, target_temp):
        print(f"Температура встановлена на {target_temp}°C.")

    def turnOnHeater(self):
        print("Обігрівач увімкнено.")

    def turnOnAC(self):
        print("Кондиціонер увімкнено.")

class EntertainmentSystem:
    def playMusic(self):
        print("Музика увімкнена.")

    def stopMusic(self):
        print("Музика вимкнена.")

    def setVolume(self, level):
        print(f"Гучність встановлена на рівень {level}.")

class SettingsManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance.preferences = {}
        return cls._instance

    def setPreference(self, key, value):
        self.preferences[key] = value
        print(f"Налаштування '{key}' встановлено на '{value}'.")

    def getPreference(self, key):
        return self.preferences.get(key, None)

class EnergyManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnergyManager, cls).__new__(cls)
            cls._instance.energy_data = {}
        return cls._instance

    def monitorUsage(self):
        print("Моніторинг енергоспоживання...")

    def optimizeEnergy(self):
        print("Оптимізація енергоспоживання завершена.")

class SmartHomeFacade:
    def __init__(self, lighting, security, climate, entertainment):
        self.lighting = lighting
        self.security = security
        self.climate = climate
        self.entertainment = entertainment
        self.settings = SettingsManager()
        self.energy = EnergyManager()

    def activateSecuritySystem(self):
        self.security.armSystem()
        print("Система безпеки активована через фасад.")

    def deactivateSecuritySystem(self):
        self.security.disarmSystem()
        print("Система безпеки деактивована через фасад.")

    def setClimateControl(self, target_temp):
        self.climate.setTemperature(target_temp)
        self.settings.setPreference("temperature", target_temp)
        print(f"Клімат налаштовано через фасад на {target_temp}°C.")

    def controlLighting(self, action, brightness=None):
        if action == "on":
            self.lighting.turnOnLights()
        elif action == "off":
            self.lighting.turnOffLights()
        if brightness is not None:
            self.lighting.setBrightness(brightness)
            self.settings.setPreference("brightness", brightness)
        print(f"Освітлення керується через фасад: дія {action}, яскравість: {brightness}")

    def playMusic(self):
        self.entertainment.playMusic()
        print("Музика увімкнена через фасад.")

    def stopMusic(self):
        self.entertainment.stopMusic()
        print("Музика вимкнена через фасад.")
