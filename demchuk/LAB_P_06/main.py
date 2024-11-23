from facade import SmartHomeFacade, LightingSystem, SecuritySystem, ClimateControlSystem, EntertainmentSystem
from bridge import Light, Switch

if __name__ == "__main__":
    # Ініціалізація підсистем
    lighting = LightingSystem()
    security = SecuritySystem()
    climate = ClimateControlSystem()
    entertainment = EntertainmentSystem()

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
        security=security,
        climate=climate,
        entertainment=entertainment
    )

    # Тестування
    smart_home.activateSecuritySystem()
    smart_home.setClimateControl(22)
    smart_home.controlLighting("on", brightness=80)
    smart_home.playMusic()
    smart_home.stopMusic()
    smart_home.deactivateSecuritySystem()
