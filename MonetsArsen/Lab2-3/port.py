"""
Port Classes

This module defines an interface `IPort` and a concrete implementation `Port` for a port
in a shipping system. The `Port` class handles the incoming and outgoing of ships,
as well as the management of containers and ship history.

Classes:
    IPort (ABC): An abstract interface for a port.
    Port: A concrete implementation of a port.

Dependencies:
    - container.Container (for type checking)
    - ship.IShip (for type checking)
"""

from abc import abstractmethod, ABC
from typing import Tuple, List, Self, TYPE_CHECKING
import math

if TYPE_CHECKING:
    from container import Container
    from ship import IShip

class IPort(ABC):
    """
    An abstract interface for a port.

    This interface defines the common methods for handling incoming and outgoing ships.
    """

    @abstractmethod
    def incoming_ship(self, ship: 'IShip') -> None:
        """
        Handle an incoming ship.

        Args:
            ship (IShip): The ship that is arriving at the port.

        Returns:
            None
        """
        pass

    @abstractmethod
    def outgoing_ship(self, ship: 'IShip') -> None:
        """
        Handle an outgoing ship.

        Args:
            ship (IShip): The ship that is departing from the port.

        Returns:
            None
        """
        pass

class Port(IPort):
    """
    A concrete implementation of a port.

    This class handles the incoming and outgoing of ships, as well as the management
    of containers and ship history.

    Attributes:
        id (int): The unique identifier for the port.
        coordinates (Tuple[float, float]): The geographic coordinates of the port.
        containers (List[Container]): The list of containers at the port.
        ship_history (List[IShip]): The list of ships that have visited the port.
        ship_current (List[IShip]): The list of ships currently at the port.
    """

    def __init__(self, identifier: int, coordinates: Tuple[float, float]) -> None:
        """
        Initialize a Port object.

        Args:
            identifier (int): The unique identifier for the port.
            coordinates (Tuple[float, float]): The geographic coordinates of the port.
        """
        self.id = identifier
        self.coordinates = coordinates
        self.containers: List[Container] = []
        self.ship_history: List['IShip'] = []
        self.ship_current: List['IShip'] = []

    def get_distance(self, port: Self) -> float:
        """
        Calculate the distance between two ports.

        Args:
            port (Port): The other port to calculate the distance to.

        Returns:
            float: The distance between the two ports.
        """
        return math.sqrt((self.coordinates[0] - port.coordinates[0]) ** 2 + (self.coordinates[1] - port.coordinates[1]) ** 2)

    def incoming_ship(self, ship: 'IShip') -> None:
        """
        Handle an incoming ship.

        Add the ship to the list of ships currently at the port.

        Args:
            ship (IShip): The ship that is arriving at the port.

        Returns:
            None
        """
        self.ship_current.append(ship)

    def outgoing_ship(self, ship: 'IShip') -> None:
        """
        Handle an outgoing ship.

        Remove the ship from the list of ships currently at the port and add it to the
        list of ships that have visited the port.

        Args:
            ship (IShip): The ship that is departing from the port.

        Returns:
            None
        """
        if ship in self.ship_current:
            self.ship_current.remove(ship)

            if ship not in self.ship_history:
                self.ship_history.append(ship)


