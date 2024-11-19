from device_interface import SecurityDevice

class SecuritySystem(SecurityDevice):
    def arm_system(self):
        print("Security system armed")
    
    def disarm_system(self):
        print("Security system disarmed")
    
    def start(self):
        self.arm_system()
    
    def stop(self):
        self.disarm_system()
