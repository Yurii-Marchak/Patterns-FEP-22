from abc import abstractmethod, ABC
from typing import Self, Any, Tuple, List 

import math

from container import BasicContainer, HeavyContainer, LiquidContainer, RefrigeratedContainer

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ship import Ship
    from container import Container, BasicContainer, HeavyContainer, LiquidContainer, RefrigeratedContainer



class IPort(ABC): 
    @abstractmethod
    def incoming_ship(self, s: Any) -> None: 
        """
        Registers an incoming ship at the port.

        Args:
            s (Ship): The incoming ship.

        Effect:
            Updates the port's list of current and historical ships.
        """
        pass
    
    
    @abstractmethod
    def outgoing_ship(self, s: Any) -> None: 
        """
        Removes a departing ship from the port's current list of ships.

        Args:
            s (Ship): The ship leaving the port.

        Effect:
            Removes the ship from the list of currently docked ships.
        """
        pass
    

class Port(IPort):
    
    
    def __init__(self, id: int, coordinates: Tuple[float, float]) -> None:
        """
        Initializes a new port with an ID and geographic coordinates.

        Args:
            id (int): The unique identifier for the port.
            coordinates (Tuple[float, float]): The latitude and longitude of the port.

        Effect:
            Sets up the port's basic information and initializes empty lists for containers and ships.
        """
        self.id = id
        self.coordinates = coordinates
        self.list_of_containers: List[Container] = []
        self.current_ships: List[Ship] = []
        self.history_list_of_ships: List[Ship] = []
     
     
     
    def to_dict(self):
        return {
            "id": self.id,
            "coordinates": self.coordinates,
            "containers in port": self.list_of_containers,
            "ships": [ship.to_dict() for ship in self.current_ships]
        } 
     
    def get_distance(self, port: Self) -> float:
        """
        Calculates the distance between this port and another using geographic coordinates.

        Args:
            port (Port): The other port to calculate the distance to.

        Effect:
            Computes the distance between the two ports in kilometers using the Haversine formula.
        """
        lat1, lon1 = self.coordinates
        lat2, lon2 = port.coordinates

        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        R = 6371.0
        distance = R * c
        print(f"Distance between port A and port B: {distance:.2f} км")
        return distance
    
    
    def incoming_ship(self, s: 'Ship') -> None:
        """
        Adds an incoming ship to the port's current and history lists.
        """
        if s not in self.current_ships:
            self.current_ships.append(s)
        if s not in self.history_list_of_ships:
            self.history_list_of_ships.append(s)

    def outgoing_ship(self, s: 'Ship') -> None:
        """
        Removes a departing ship from the port's current list of ships.
        """
        if s in self.current_ships:
            self.current_ships.remove(s)
        