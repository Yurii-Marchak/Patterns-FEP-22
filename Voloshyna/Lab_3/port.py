import haversine as hs
from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from container import Container

if TYPE_CHECKING:
    from ship import Ship

class IPort(ABC):
    @abstractmethod
    def incoming_ship(self, ship: 'Ship'):
        pass

    @abstractmethod
    def outgoing_ship(self, ship: 'Ship'):
        pass

class Port(IPort):
    def __init__(self, port_id: str, latitude: float, longitude: float) -> None:
        self.id = port_id
        self.containers: List[Container] = []
        self.ship_history = []
        self.current_ships = []
        self.latitude = latitude
        self.longitude = longitude

    def get_distance(self, port) -> float:
        return hs.haversine((self.latitude, self.longitude), (port.latitude, port.longitude))

    def incoming_ship(self, ship: 'Ship') -> bool:
        if isinstance(ship, Ship) and ship not in self.current_ships:
            self.current_ships.append(ship)
            return True
        return False

    def outgoing_ship(self, ship: 'Ship') -> bool:
        if isinstance(ship, Ship) and ship in self.current_ships:
            self.current_ships.remove(ship)
            self.ship_history.append(ship)
            return True
        return False
