from abc import abstractmethod, ABC
import math
from typing import Self, Tuple, List, TYPE_CHECKING
import uuid
if TYPE_CHECKING:
    from containers import Container
    from ship import Ship


class IPort(ABC):
    @abstractmethod
    def incoming_ship(self, ship:'Ship') -> bool:
        pass
    
    @abstractmethod
    def outgoing_ship(self, ship:'Ship') -> bool:
        pass

class Port(IPort):
    """
    Represents a port where ships can dock, load, and unload containers.

    Attributes:
        id (UUID): A unique identifier for the port.
        coordinates (Tuple[float, float]): The geographical coordinates (latitude, longitude) of the port.
        list_of_ship (List[Ship]): A list of ships currently at the port.
        history_of_ship (List[Ship]): A list of ships that have previously docked at the port.
        containers (List[Container]): A list of containers available at the port.
    """
    def __init__(self, coordinates: Tuple[float, float]) -> None:
        self.id = uuid.uuid4()
        self.coordinates = coordinates
        self.list_of_ship: List[Ship] = []
        self.history_of_ship: List[Ship] = []
        self.containers: List[Container] = []
        
    def get_distance(self, other_port: Self) -> float:
        """
        Calculates the great-circle distance between this port and another port using the Haversine formula.

        Args:
            other_port (Port): The port to calculate the distance to.

        Returns:
            float: The distance in kilometers between the two ports.
        """
        R = 6371.0
        x1, y1 = math.radians(self.coordinates[0]), math.radians(self.coordinates[1])
        x2, y2 = math.radians(other_port.coordinates[0]), math.radians(other_port.coordinates[1])
        latitude = x1 - x2
        longitude = y1 - y2
        a = math.pow(math.sin(latitude / 2), 2) + (math.cos(x1) * math.cos(x2) * math.pow(math.sin(longitude / 2), 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def incoming_ship(self, ship: 'Ship') -> bool:
        """
        Adds an incoming ship to the list of ships at the port.

        Args:
            ship (Ship): The ship that is arriving at the port.

        Returns:
            bool: True if the ship was successfully added, False if it was already present in the list.
        """
        if ship not in self.list_of_ship:
            self.list_of_ship.append(ship)
            return True
        return False
    
    def outgoing_ship(self, ship: 'Ship') -> bool:
        """
        Removes a ship from the port's list of ships and adds it to the history of ships.

        Args:
            ship (Ship): The ship that is departing from the port.

        Returns:
            bool: True if the ship was successfully removed, False if it was not found in the list.
        """
        if ship in self.list_of_ship:
            self.list_of_ship.remove(ship)
            self.history_of_ship.append(ship)                
            return True
        return False
        