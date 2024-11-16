from abc import abstractmethod, ABC
from typing import Self, Any, Tuple, List
import math


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ship import *
    from container import *


class IPort(ABC): 
    @abstractmethod
    def incoming_ship(s: Any) -> None: 
        pass
    
    
    @abstractmethod
    def outgoing_ship(s: Any) -> None: 
        pass
    

class Port(IPort):
    
    def __init__(self, id: int, coordinates: Tuple[float, float], list_of_containers: List['Container'], 
                 current_ships: List['Ship'], history_list_of_ships: List['Ship'] ) -> None:
        self.id = id
        self.coordinates = coordinates
        self.list_of_containers: List[Container] = []
        self.current_ships: List[Ship] = []
        self.history_list_of_ships: List[Ship] = []
     
     
    def get_distance(self, port: Self) -> float:
        lat1, lon1 = self.coordinates
        lat2, lon2 = port.coordinates

        
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        R = 6371.0
        distance = R * c
        print(f"Відстань між портом A і портом B: {distance:.2f} км")
        return distance
    
    
    def incoming_ship(self, s: 'Ship') -> None:
        if s.sail_to(self.port):
            if s not in self.current_ships:
                self.current_ships.append(s)
            if s not in self.history_list_of_ships:
                self.history_list_of_ships.append(s)

    def outgoing_ship(self, s: 'Ship') -> None:
        if s not in self.current_ships:
            self.current_ships.remove(s)
        