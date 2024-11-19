from device_interface import LightingDevice

class LightingSystem(LightingDevice):
    def turn_on(self):
        print("Lights turned on")
    
    def turn_off(self):
        print("Lights turned off")
    
    def start(self):
        self.turn_on()
    
    def stop(self):
        self.turn_off()