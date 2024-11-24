from abc import ABC, abstractmethod
from typing import List

# --- Singleton Classes ---
class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]


class SettingsManager(Singleton):
    def __init__(self):
        self.preferred_temperature = 72
        self.lighting_preset = "Normal"
        self.energy_saving_mode = False

    def get_settings(self):
        return {
            "preferred_temperature": self.preferred_temperature,
            "lighting_preset": self.lighting_preset,
            "energy_saving_mode": self.energy_saving_mode
        }


class EnergyManager(Singleton):
    def __init__(self):
        self.energy_usage = 0

    def monitor_usage(self):
        print(f"Monitoring energy usage: {self.energy_usage} kWh")

    def optimize_energy(self):
        self.energy_usage -= 10  # Example logic for energy optimization
        print(f"Optimizing energy usage. Current usage: {self.energy_usage} kWh")

# --- Subsystems ---
class LightingSystem:
    def turn_on_lights(self):
        print("Turning on the lights.")

    def turn_off_lights(self):
        print("Turning off the lights.")

    def set_brightness(self, level):
        print(f"Setting brightness to {level}%.")

class SecuritySystem:
    def arm_system(self):
        print("Arming the security system.")

    def disarm_system(self):
        print("Disarming the security system.")

    def trigger_alarm(self):
        print("Triggering alarm!")

class ClimateControlSystem:
    def set_temperature(self, target_temp):
        print(f"Setting temperature to {target_temp}°F.")

    def turn_on_heater(self):
        print("Turning on the heater.")

    def turn_on_ac(self):
        print("Turning on the air conditioning.")

class EntertainmentSystem:
    def play_music(self):
        print("Playing music.")

    def stop_music(self):
        print("Stopping music.")

    def set_volume(self, level):
        print(f"Setting volume to {level}.")

# --- SmartHomeFacade ---
class SmartHomeFacade:
    def __init__(self):
        self.lighting_system = LightingSystem()
        self.security_system = SecuritySystem()
        self.climate_control = ClimateControlSystem()
        self.entertainment_system = EntertainmentSystem()

    def activate_security_system(self):
        self.security_system.arm_system()

    def deactivate_security_system(self):
        self.security_system.disarm_system()

    def set_climate_control(self, target_temp):
        self.climate_control.set_temperature(target_temp)

    def turn_on_lights(self):
        self.lighting_system.turn_on_lights()

    def turn_off_lights(self):
        self.lighting_system.turn_off_lights()

    def play_music(self):
        self.entertainment_system.play_music()

    def stop_music(self):
        self.entertainment_system.stop_music()

    def set_brightness(self, level):
        self.lighting_system.set_brightness(level)

# --- VoiceControl ---
class VoiceControl:
    def __init__(self, facade):
        self.facade = facade

    def process_command(self, command):
        if "turn on lights" in command:
            self.facade.turn_on_lights()
        elif "turn off lights" in command:
            self.facade.turn_off_lights()
        elif "play music" in command:
            self.facade.play_music()
        elif "stop music" in command:
            self.facade.stop_music()
        elif "set temperature" in command:
            temp = int(command.split()[-1])
            self.facade.set_climate_control(temp)
        elif "activate security" in command:
            self.facade.activate_security_system()
        elif "deactivate security" in command:
            self.facade.deactivate_security_system()

# --- Bridge Pattern Implementation ---
# Applinace Interface
class Appliance(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

# Concrete Appliances
class AC(Appliance):
    def start(self):
        print("AC is now ON.")

    def stop(self):
        print("AC is now OFF.")

class Refrigerator(Appliance):
    def start(self):
        print("Refrigerator is now ON.")

    def stop(self):
        print("Refrigerator is now OFF.")

class Fan(Appliance):
    def start(self):
        print("Fan is now ON.")

    def stop(self):
        print("Fan is now OFF.")

# Switch Interface
class Switch(ABC):
    def __init__(self, appliance: Appliance):
        self.appliance = appliance

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

# Concrete Switches
class AutomaticRemoteController(Switch):
    def turn_on(self):
        print("Using automatic remote to turn ON the appliance.")
        self.appliance.start()

    def turn_off(self):
        print("Using automatic remote to turn OFF the appliance.")
        self.appliance.stop()

class ManualRemoteController(Switch):
    def turn_on(self):
        print("Using manual remote to turn ON the appliance.")
        self.appliance.start()

    def turn_off(self):
        print("Using manual remote to turn OFF the appliance.")
        self.appliance.stop()

# --- Testing the Code ---

# Facade Test
facade = SmartHomeFacade()
facade.turn_on_lights()
facade.set_climate_control(72)
facade.activate_security_system()

# Voice Command Test
voice_control = VoiceControl(facade)
voice_control.process_command("turn on lights")
voice_control.process_command("set temperature 68")

# Bridge Pattern Test
ac = AC()
fan = Fan()

automatic_ac_switch = AutomaticRemoteController(ac)
manual_fan_switch = ManualRemoteController(fan)

automatic_ac_switch.turn_on()
manual_fan_switch.turn_off()
