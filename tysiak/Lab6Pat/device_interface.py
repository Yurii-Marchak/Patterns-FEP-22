from abc import ABC, abstractmethod

class Device(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

class LightingDevice(Device):
    @abstractmethod
    def turn_on(self):
        pass
    
    @abstractmethod
    def turn_off(self):
        pass

class ClimateDevice(Device):
    @abstractmethod
    def set_temperature(self, temperature: int):
        pass

class EntertainmentDevice(Device):
    @abstractmethod
    def play_music(self):
        pass
    
    @abstractmethod
    def stop_music(self):
        pass

class SecurityDevice(Device):
    @abstractmethod
    def arm_system(self):
        pass
    
    @abstractmethod
    def disarm_system(self):
        pass
