class SettingsManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SettingsManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.temperature = 22  # default temperature
        self.lighting_level = 50  # default lighting level

    def set_temperature(self, temperature):
        self.temperature = temperature

    def get_temperature(self):
        return self.temperature

    def set_lighting_level(self, level):
        self.lighting_level = level

    def get_lighting_level(self):
        return self.lighting_level
