from abc import ABC, abstractmethod
from container import Container
from Iship import IShip

class Ship(IShip):
    def __init__(self, id: int, weight_capacity: float, port, fuel_capacity: float, maxNumberOfAllContainers: int,
                 maxNumberOfHeavyContainers: int, maxNumberOfRefrigeratedContainers: int,
                 maxNumberOfLiquidContainers: int, fuelConsumptionPerKM: float):
        self.ID = id
        self.weight_capacity = weight_capacity
        self.port = port
        self.fuel_capacity = fuel_capacity
        self.containers = []
        self.fuel = fuel_capacity
        self.maxNumberOfAllContainers = maxNumberOfAllContainers
        self.maxNumberOfHeavyContainers = maxNumberOfHeavyContainers
        self.maxNumberOfRefrigeratedContainers = maxNumberOfRefrigeratedContainers
        self.maxNumberOfLiquidContainers = maxNumberOfLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM

    def sailTo(self, port):
        distance = self.port.getDistance(port)
        fuel_needed = distance * self.fuelConsumptionPerKM
        if fuel_needed <= self.fuel:
            self.fuel -= fuel_needed
            self.port.outgoingShip(self)
            self.port = port
            port.incomingShip(self)
            return True
        return False

    def reFuel(self, fuel_amount):
        if self.fuel + fuel_amount <= self.fuel_capacity:
            self.fuel += fuel_amount

    def load(self, container):
        if len(self.containers) < self.maxNumberOfAllContainers:
            self.containers.append(container)

    def unLoad(self, container):
        self.containers.remove(container)

    def to_dict(self):
        return {
            "ID": self.ID,
            "fuel_left": round(self.fuel, 2),
            "containers": [container.to_dict() for container in self.containers]
        }

class LightWeightShip(Ship):
    def __init__(self, id: int, port, fuel_capacity: float):
        super().__init__(id, 2000.0, port, fuel_capacity, 10, 5, 3, 2, 1.0)

class MediumShip(Ship):
    def __init__(self, id: int, port, fuel_capacity: float):
        super().__init__(id, 5000.0, port, fuel_capacity, 20, 10, 5, 4, 2.0)

class HeavyShip(Ship):
    def __init__(self, id: int, port, fuel_capacity: float):
        super().__init__(id, 10000.0, port, fuel_capacity, 30, 15, 10, 6, 3.0)
