from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from containers import Container
import json
from math import radians, cos, sin, sqrt, atan2

class IPort(ABC):
    @abstractmethod
    def incoming_ship(self, s: Any) -> None:
        pass

    @abstractmethod
    def outgoing_ship(self, s: Any) -> None:
        pass

class Port(IPort):
    def __init__(self, id: int, coordinates: Tuple[float, float]) -> None:
        self.id = id
        self.coordinates = coordinates
        self.containers: List[Container] = []
        self.current_ships: List[Any] = []
        self.ship_history: List[Any] = []

    def incoming_ship(self, ship: Any) -> None:
        if ship not in self.current_ships:
            self.current_ships.append(ship)
        if ship not in self.ship_history:
            self.ship_history.append(ship)

    def outgoing_ship(self, ship: Any) -> None:
        if ship in self.current_ships:
            self.current_ships.remove(ship)

    def load_container(self, container: Container) -> None:
        self.containers.append(container)

    def unload_container(self, ship: Any, container: Container) -> None:
        if container in ship.containers:
            ship.unload(container)  # Вивантажуємо з корабля
            self.load_container(container)  # Завантажуємо в порт
            print(f"Container {container.id} unloaded from Ship {ship.id} to Port {self.id}")

    def get_distance(self, other_port):
        R = 6371.0  # Radius of the Earth in km
        lat1, lon1 = self.coordinates
        lat2, lon2 = other_port.coordinates

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    def to_json(self):
        return {
            "id": self.id,
            "coordinates": self.coordinates,
            "containers": [container.to_json() for container in self.containers]
        }

    @classmethod
    def from_json(cls, data):
        port = cls(id=data["id"], coordinates=tuple(data["coordinates"]))
        port.containers = [Container.from_json(c) for c in data["containers"]]
        return port
