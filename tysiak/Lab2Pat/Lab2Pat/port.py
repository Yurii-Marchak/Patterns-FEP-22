from abc import ABC, abstractmethod
from typing import List, Tuple, Any
from math import radians, cos, sin, sqrt, atan2
from containers import Container

class IPort(ABC):
    """
    Abstract Base Class (ABC) for a port interface.

    Methods:
    --------
    incoming_ship(s: Any) -> None:
        Abstract method to handle incoming ships to the port.

    outgoing_ship(s: Any) -> None:
        Abstract method to handle outgoing ships from the port.
    """
    @abstractmethod
    def incoming_ship(self, s: Any) -> None:
        """
        Abstract method for handling an incoming ship.
        
        Parameters:
        -----------
        s : Any
            The ship object arriving at the port.
        """
        pass

    @abstractmethod
    def outgoing_ship(self, s: Any) -> None:
        """
        Abstract method for handling an outgoing ship.
        
        Parameters:
        -----------
        s : Any
            The ship object leaving the port.
        """
        pass


class Port(IPort):
    """
    A class to represent a port where ships can dock.

    Attributes:
    -----------
    id : int
        Unique identifier for the port.
    coordinates : Tuple[float, float]
        Coordinates (latitude, longitude) of the port.
    containers : List[Container]
        List of containers stored at the port.
    current_ships : List[Any]
        List of ships currently docked at the port.
    ship_history : List[Any]
        History of all ships that have ever docked at the port.

    Methods:
    --------
    incoming_ship(ship: Any) -> None:
        Handles a ship arriving at the port, updating the current ships and ship history.
    outgoing_ship(ship: Any) -> None:
        Handles a ship leaving the port, removing it from the list of current ships.
    get_distance(other_port: Port) -> float:
        Calculates the distance in kilometers between this port and another port using their coordinates.
    """
    def __init__(self, id: int, coordinates: Tuple[float, float]) -> None:
        """
        Initialize a new Port object.

        Parameters:
        -----------
        id : int
            Unique identifier for the port.
        coordinates : Tuple[float, float]
            The geographical coordinates (latitude, longitude) of the port.
        """
        self.id = id
        self.coordinates = coordinates
        self.containers: List[Container] = []
        self.current_ships: List[Any] = []
        self.ship_history: List[Any] = []

    def incoming_ship(self, ship: Any) -> None:
        """
        Handles a ship arriving at the port. Adds the ship to the list of current ships 
        and updates the ship history if it hasn't been recorded before.

        Parameters:
        -----------
        ship : Any
            The ship object that is arriving at the port.
        """
        if ship not in self.current_ships:
            self.current_ships.append(ship)
        if ship not in self.ship_history:
            self.ship_history.append(ship)

    def outgoing_ship(self, ship: Any) -> None:
        """
        Handles a ship leaving the port. Removes the ship from the list of current ships.

        Parameters:
        -----------
        ship : Any
            The ship object that is leaving the port.
        """
        if ship in self.current_ships:
            self.current_ships.remove(ship)

    def get_distance(self, other_port):
        """
        Calculates the distance in kilometers between this port and another port using their latitude and longitude.

        Parameters:
        -----------
        other_port : Port
            The other port object to calculate the distance to.

        Returns:
        --------
        float
            The distance between the two ports in kilometers.
        """
        R = 6371.0  # Радіус Землі в км
        lat1, lon1 = self.coordinates
        lat2, lon2 = other_port.coordinates

        # Перетворення координат у радіани
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
