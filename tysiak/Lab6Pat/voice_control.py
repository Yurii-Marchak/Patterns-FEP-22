class VoiceControl:
    def __init__(self, smart_home_facade):
        self.smart_home_facade = smart_home_facade

    def execute_command(self, command):
        if command == "turn on the lights":
            self.smart_home_facade.control_lighting("on")
        elif command == "turn off the lights":
            self.smart_home_facade.control_lighting("off")
        elif command.startswith("set temperature to"):
            temperature = int(command.split()[-1])
            self.smart_home_facade.set_climate_control(temperature)
        elif command == "play music":
            self.smart_home_facade.play_music()
        elif command == "stop music":
            self.smart_home_facade.stop_music()
