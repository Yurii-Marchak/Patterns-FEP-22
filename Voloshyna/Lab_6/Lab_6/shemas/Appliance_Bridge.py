
class Appliance:
    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

class Switch:
    def __init__(self, appliance):
        self.appliance = appliance

    def turn_on(self):
        self.appliance.start()

    def turn_off(self):
        self.appliance.stop()

class RemoteControl:
    def __init__(self, appliance):
        self.appliance = appliance

    def activate(self):
        self.appliance.start()

    def deactivate(self):
        self.appliance.stop()

class Light(Appliance):
    def start(self):
        print("Light turned on")

    def stop(self):
        print("Light turned off")

class Fan(Appliance):
    def start(self):
        print("Fan started")

    def stop(self):
        print("Fan stopped")
