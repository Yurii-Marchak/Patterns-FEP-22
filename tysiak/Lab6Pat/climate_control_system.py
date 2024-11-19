from device_interface import ClimateDevice

class ClimateControlSystem(ClimateDevice):
    def set_temperature(self, temperature: int):
        print(f"Temperature set to {temperature}°C")
    
    def start(self):
        print("Climate control started")
    
    def stop(self):
        print("Climate control stopped")
