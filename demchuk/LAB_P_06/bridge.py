class Appliance:
    def start(self):
        pass

    def stop(self):
        pass

class Light(Appliance):
    def start(self):
        print("Світло увімкнено.")

    def stop(self):
        print("Світло вимкнено.")

class Switch:
    def __init__(self, appliance):
        self.appliance = appliance

    def turn_on(self):
        self.appliance.start()

    def turn_off(self):
        self.appliance.stop()
