from abc import ABC, abstractmethod
from typing import List
from containers import Container
from port import Port

class Ship(ABC):
    def __init__(self, id: int, fuel: float, current_port: Port, total_weight_capacity: int, max_containers: int, max_heavy: int, max_refrigerated: int, max_liquid: int, fuel_per_km: float) -> None:
        self.id = id
        self.fuel = fuel
        self.current_port = current_port
        self.total_weight_capacity = total_weight_capacity
        self.max_containers = max_containers
        self.max_heavy = max_heavy
        self.max_refrigerated = max_refrigerated
        self.max_liquid = max_liquid
        self.fuel_per_km = fuel_per_km
        self.containers: List[Container] = []

    @abstractmethod
    def add_item(self, item: Container) -> None:
        pass

    @abstractmethod
    def sail(self, distance: float) -> None:
        pass

    def sail_to(self, destination_port: Port) -> None:
        """Реалізація переміщення корабля до іншого порту."""
        distance = self.current_port.get_distance(destination_port)
        fuel_needed = distance * self.fuel_per_km

        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            self.current_port.outgoing_ship(self)
            destination_port.incoming_ship(self)
            self.current_port = destination_port
            print(f"Ship {self.id} successfully sailed to Port {destination_port.id}. Distance: {distance:.2f} km. Fuel left: {self.fuel:.2f}")
        else:
            print(f"Ship {self.id} does not have enough fuel to sail to Port {destination_port.id}. Needed: {fuel_needed:.2f}, Available: {self.fuel:.2f}")

    def unload(self, container: Container) -> bool:
        """Вивантажує контейнер з корабля."""
        if container in self.containers:
            self.containers.remove(container)  # Видаляємо контейнер з корабля
            return True
        return False

    def to_json(self):
        return {
            "id": self.id,
            "fuel": self.fuel,
            "current_port": self.current_port.id,
            "containers": [container.to_json() for container in self.containers],
            "type": self.__class__.__name__  # Додаємо тип корабля
        }

    @classmethod
    def from_json(cls, data, ports):
        """Відновлення корабля з JSON."""
        current_port = ports[data["current_port"]]
        ship_type = data["type"]

        if ship_type == "LightWeightShip":
            ship = LightWeightShip(data["id"], data["fuel"], current_port)
        elif ship_type == "MediumShip":
            ship = MediumShip(data["id"], data["fuel"], current_port)
        elif ship_type == "HeavyShip":
            ship = HeavyShip(data["id"], data["fuel"], current_port)

        # Завантажуємо контейнери на корабель
        ship.containers = [Container.from_json(c) for c in data["containers"]]
        return ship

class LightWeightShip(Ship):
    def __init__(self, id: int, fuel: float, current_port: Port) -> None:
        super().__init__(id, fuel, current_port, total_weight_capacity=5000, max_containers=5, max_heavy=2, max_refrigerated=1, max_liquid=1, fuel_per_km=2.0)

    def add_item(self, item: Container) -> None:
        if len(self.containers) < self.max_containers:
            self.containers.append(item)

    def sail(self, distance: float) -> None:
        fuel_needed = distance * self.fuel_per_km
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"LightWeightShip {self.id} sailed {distance} km. Fuel left: {self.fuel:.2f}")
        else:
            print(f"LightWeightShip {self.id} does not have enough fuel to sail.")

class MediumShip(Ship):
    def __init__(self, id: int, fuel: float, current_port: Port) -> None:
        super().__init__(id, fuel, current_port, total_weight_capacity=10000, max_containers=10, max_heavy=4, max_refrigerated=2, max_liquid=2, fuel_per_km=4.0)

    def add_item(self, item: Container) -> None:
        if len(self.containers) < self.max_containers:
            self.containers.append(item)

    def sail(self, distance: float) -> None:
        fuel_needed = distance * self.fuel_per_km
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"MediumShip {self.id} sailed {distance} km. Fuel left: {self.fuel:.2f}")
        else:
            print(f"MediumShip {self.id} does not have enough fuel to sail.")

class HeavyShip(Ship):
    def __init__(self, id: int, fuel: float, current_port: Port) -> None:
        super().__init__(id, fuel, current_port, total_weight_capacity=20000, max_containers=20, max_heavy=10, max_refrigerated=5, max_liquid=5, fuel_per_km=6.0)

    def add_item(self, item: Container) -> None:
        if len(self.containers) < self.max_containers:
            self.containers.append(item)

    def sail(self, distance: float) -> None:
        fuel_needed = distance * self.fuel_per_km
        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            print(f"HeavyShip {self.id} sailed {distance} km. Fuel left: {self.fuel:.2f}")
        else:
            print(f"HeavyShip {self.id} does not have enough fuel to sail.")

class ShipFactory:
    @staticmethod
    def create_lightweight_ship(id: int, fuel: float, current_port: Port) -> LightWeightShip:
        return LightWeightShip(id, fuel, current_port)

    @staticmethod
    def create_medium_ship(id: int, fuel: float, current_port: Port) -> MediumShip:
        return MediumShip(id, fuel, current_port)

    @staticmethod
    def create_heavy_ship(id: int, fuel: float, current_port: Port) -> HeavyShip:
        return HeavyShip(id, fuel, current_port)

    @staticmethod
    def from_json(data, ports):
        """Метод для відновлення кораблів із JSON."""
        return Ship.from_json(data, ports)
