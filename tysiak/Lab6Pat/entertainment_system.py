from device_interface import EntertainmentDevice

class EntertainmentSystem(EntertainmentDevice):
    def play_music(self):
        print("Playing music")
    
    def stop_music(self):
        print("Music stopped")
    
    def start(self):
        self.play_music()
    
    def stop(self):
        self.stop_music()
