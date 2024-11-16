from abc import abstractmethod, ABC
import math
from typing import Self, Tuple, List, TYPE_CHECKING
import uuid
if TYPE_CHECKING:
    from containers import Container
    from ship import Ship
    from item import Item


class IPort(ABC):
    """
    Abstract base class for ports in the ship management system.

    This class defines the interface for managing incoming and outgoing ships.
    """
    @abstractmethod
    def incoming_ship(self, ship:'Ship') -> bool:
        """
        Processes an incoming ship at the port.

        Args:
            ship (Ship): The ship that is arriving at the port.

        Returns:
            bool: True if the ship is successfully processed; otherwise, False.
        """

    @abstractmethod
    def outgoing_ship(self, ship:'Ship') -> bool:
        """
        Processes an outgoing ship from the port.

        Args:
            ship (Ship): The ship that is departing from the port.

        Returns:
            bool: True if the ship is successfully processed; otherwise, False.
        """

class Port(IPort):
    """
    Represents a port where ships can dock, load, and unload containers.

    Attributes:
        id (UUID): A unique identifier for the port.
        coordinates (Tuple[float, float]): The geographical coordinates 
        (latitude, longitude) of the port.
        list_of_ship (List[Ship]): A list of ships currently at the port.
        history_of_ship (List[Ship]): A list of ships that have previously docked at the port.
        containers (List[Container]): A list of containers available at the port.
    """
    def __init__(self, coordinates: Tuple[float, float]) -> None:
        self.port_id = str(uuid.uuid4())
        self.coordinates = coordinates
        self.list_of_ship: List[Ship] = []
        self.history_of_ship: List[Ship] = []
        self.containers: List[Container] = []
        self.items: List[Item] = []

    def port_data(self):
        """
        Returns a dictionary containing data about the port.

        This method constructs and returns the port data in the form of a dictionary. 
        The dictionary includes the port's ID, coordinates, the list of containers currently 
        in the port, and the list of ships docked at the port.

        Returns:
            dict: A dictionary with the following keys:
                - "Port ID": The unique identifier of the port (UUID).
                - "Coordinates": A tuple representing the geographical coordinates of the port.
                - "Containers in the port": A list of dictionaries, each representing 
                a container currently in the port.
                - "List of ship": A list of dictionaries, each representing a ship currently docked at the port.
        """
        return {
            "Port ID": self.port_id,
            "Coordinates": self.coordinates,
            "Containers in the port": [container.container_data() for container in self.containers],
            "List of ship": [ship.ship_data() for ship in self.list_of_ship]
        }

    def get_distance(self, other_port: Self) -> float:
        """
        Calculates the great-circle distance between this port and 
        another port using the Haversine formula.

        Args:
            other_port (Port): The port to calculate the distance to.

        Returns:
            float: The distance in kilometers between the two ports.
        """
        radius = 6371.0
        x_1, y_1 = math.radians(self.coordinates[0]), math.radians(self.coordinates[1])
        x_2, y_2 = math.radians(other_port.coordinates[0]), math.radians(other_port.coordinates[1])
        latitude = x_1 - x_2
        longitude = y_1 - y_2
        haversine = math.pow(math.sin(latitude / 2), 2) + (math.cos(x_1) * math.cos(x_2) * math.pow(math.sin(longitude / 2), 2))
        central_angle = 2 * math.atan2(math.sqrt(haversine), math.sqrt(1 - haversine))
        distance = radius * central_angle
        return distance

    def incoming_ship(self, ship: 'Ship') -> bool:
        """
        Adds an incoming ship to the list of ships at the port.`

        Args:
            ship (Ship): The ship that is arriving at the port.

        Returns:
            bool: True if the ship was successfully added, False if it was already 
            present in the list.
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
        