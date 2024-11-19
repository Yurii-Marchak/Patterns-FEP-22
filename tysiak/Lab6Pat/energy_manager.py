class EnergyManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EnergyManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.usage = {}

    def monitor_usage(self):
        print("Monitoring energy usage")

    def optimize_energy(self):
        print("Optimizing energy consumption")
