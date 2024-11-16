from abc import abstractmethod, ABC
from typing import List, Self
from typing import TYPE_CHECKING
from port import Port
from container import *

            


class Capacity:    
    def __init__(self, total_weight_capacity: float, max_all_containers: float, max_basic_containers: float,
                max_heavy_containers: float, max_refrigerated_containers: float, 
                max_liquid_containers: float,  list_of_containers: List['Container'] or []):
        self.list_of_containers = list_of_containers if list_of_containers is not None else []
        
        self.total_weight_capacity = total_weight_capacity
        self.max_all_containers = max_all_containers
        self.max_basic_containers = max_basic_containers
        self.max_heavy_containers = max_heavy_containers
        self.max_refrigerated_containers = max_refrigerated_containers
        self.max_liquid_containers = max_liquid_containers
        
        self.current_total_weight = 0.0
        self.current_all_containers = 0.0
        self.current_basic_containers  = 0.0
        self.current_heavy_containers = 0.0 
        self.current_refrigerated_containers = 0.0
        self.current_liquid_containers = 0.0
        
        self.list_of_containers = list_of_containers if list_of_containers is not None else []
        
        
    def check_if_enough_space(self, list_of_containers: list, container: 'Container') -> bool:
        """
        Checks if there is enough space and capacity for a given container.

        Args:
            list_of_containers (list): The list of containers already on the ship.
            container (Container): The container to be checked.

        Returns:
            bool: True if the container can be loaded onto the ship, False otherwise.
        """
        if (self.current_total_weight + container.weight >=  self.total_weight_capacity or self.current_all_containers >= self.max_all_containers):
            return False
        
        if isinstance(container, HeavyContainer) and self.current_heavy_containers >= self.max_heavy_containers:
            return False
            
        if isinstance(container, LiquidContainer) and self.current_liquid_containers >= self.max_liquid_containers:
            return False
        
        if isinstance(container, HeavyContainer) and self.current_heavy_containers >= self.max_heavy_containers:
            return False
       
        return True
    
    def add_container(self, container: 'Container') -> None:
        """
         Adds a container to the ship's current load and updates capacity statistics.

         Args:
             container (Container): The container to be added.
        """
        self.current_total_weight += container.weight
        self.current_all_containers += 1
        
        
        
        if isinstance(container, HeavyContainer):
            self.current_heavy_containers += 1
        elif isinstance(container, BasicContainer):
            self.current_basic_containers += 1
        elif isinstance(container, RefrigeratedContainer):
            self.current_refrigerated_containers += 1
        elif isinstance(container, LiquidContainer):
            self.current_liquid_containers += 1
    
    def remove_container(self, container: 'Container') -> None:
        """
        Removes a container from the ship's current load and updates capacity statistics.

        Args:
            container (Container): The container to be removed.
        """
        self.current_total_weight -= container.weight
        self.current_all_containers -= 1
        
        if isinstance(container, HeavyContainer):
            self.current_heavy_containers -= 1
        elif isinstance(container, RefrigeratedContainer):
            self.current_refrigerated_containers -= 1
        elif isinstance(container, LiquidContainer):
            self.current_liquid_containers -= 1
        
        
        
        
               

class IShip(ABC):
    def __init__(self, id: int, current_port: 'Port', fuel: float, capacity: 'Capacity', fuel_consumption_per_km: float, list_of_containers: List['Container'] = None) -> None:
        self.id: int = id
        self.current_port: Port = current_port
        self.fuel: float = fuel
        self.capacity: Capacity = capacity
        self.fuel_consumption_per_km: float = fuel_consumption_per_km
        self.list_of_containers: List['Container'] = list_of_containers if list_of_containers is not None else []

        
        
    @abstractmethod
    def sail_to(self, port: 'Port') -> bool:
        pass
    
    @abstractmethod
    def load(self, container: 'Container', list_of_containers: List['Container'], capacity) -> bool:
        pass
    
    @abstractmethod
    def unload(self, container: 'Container', list_of_containers: List['Container'] ) -> bool:
        pass
    
    @abstractmethod
    def re_fuel(self, fuel: float, fuel_consumption_per_km: float ) -> None:
        pass
    
    
    
    
class Ship(IShip):
    
    def __init__(self, id: int, current_port: 'Port', fuel: float, capacity: 'Capacity', fuel_consumption_per_km: float, list_of_containers: List['Container'] = None) -> None:
        self.id: int = id
        self.current_port: Port = current_port
        self.fuel: float = fuel
        self.capacity = capacity
        self.fuel_consumption_per_km: float = fuel_consumption_per_km
        self.list_of_containers: List['Container'] = list_of_containers if list_of_containers is not None else []
    
    def re_fuel(self, fuel: float ) -> None:
        """
        Refuels the ship by a specified amount.

        Args:
            fuel (float): The amount of fuel to add in liters.
        """
        self.fuel += fuel
        print(f"Ship {self.id} has been refueled with {fuel:.2f} liters. Current fuel: {self.fuel:.2f} liters")
       
    def sail_to(self, port: 'Port') -> bool:
        """
        Attempts to sail to another port. Checks if the ship has enough fuel for the journey.

        Args:
            port (Port): The destination port.

        Returns:
            bool: True if the journey is successful, False if there's not enough fuel.
        """
        
        distance = self.current_port.get_distance(port)
        
        required_fuel = distance * self.total_fuel_consumption_per_km()
        print(f"Required fuel for journey is {required_fuel:.2f} l")
        if self.fuel >= required_fuel:
            self.fuel -= required_fuel

            self.current_port.outgoing_ship(self)
            
            self.current_port = port
            
            print(f"Ship {self.id} has succesfully got to the port")
            port.incoming_ship(self)
            return True
        else:
            print(f"Not enough fuel for the trip. Refueling is necessary.")
            return False
     
   
    def total_fuel_consumption_per_km(self) -> float:
        """
        Calculates the total fuel consumption per kilometer, including containers' consumption.

        Returns:
            float: The total fuel consumption per kilometer.
        """
        total_consumption = self.fuel_consumption_per_km
        
        for container in self.list_of_containers:
            total_consumption += container.consumption()
            
        return total_consumption
        
        
      
    def load(self, container: 'Container') -> bool:
        """
        Loads a container onto the ship if there's enough space and capacity.

        Args:
            container (Container): The container to be loaded.

        Returns:
            bool: True if the container is successfully loaded, False otherwise.
        """
        if self.capacity.check_if_enough_space(self.list_of_containers, container):
            self.list_of_containers.append(container)
            self.capacity.add_container(container)
            if container in self.current_port.list_of_containers:
                self.current_port.list_of_containers.remove(container)
            # print(f"Container {container.id} has been succesfully loaded to the ship {self.id}")
            return True
        return False
    
    
    def unload(self, container: 'Container') -> bool:
        """
        Unloads a container from the ship and updates capacity.

        Args:
            container (Container): The container to be unloaded.

        Returns:
            bool: True if the container is successfully unloaded, False otherwise.
        """
        if container in self.list_of_containers:
            self.list_of_containers.remove(container)
            self.capacity.remove_container(container)
            self.current_port.list_of_containers.append(container)
            # print(f"Container {container.id} has been succesfully unloaded to the ship {self.id}")
            return True
        return False
            
            
    
    
    
class LightWeightShip(Ship):

        
    def __init__(self, id, current_port, fuel, capacity, fuel_consumption_per_km):
        capacity = Capacity(total_weight_capacity=15, max_all_containers=10, max_basic_containers=6,
                        max_heavy_containers=4, max_refrigerated_containers=0, max_liquid_containers=0, list_of_containers=[])
        super().__init__(id, current_port, fuel, capacity, fuel_consumption_per_km)
     
   
    def to_dict(self):
        try:
            containers_list = [container.to_dict() for container in self.list_of_containers if hasattr(container, 'to_dict')]
        except Exception as e:
            print(f"Error while converting containers to dict: {e}")
            containers_list = []
    
        
        return {
            "id": self.id,
            "fuel": self.fuel,
            "containers": containers_list
        }
 
  
class MediumShip(Ship):
    def __init__(self, id, current_port, fuel, capacity, fuel_consumption_per_km):
        capacity = Capacity(total_weight_capacity=25, max_all_containers=12, max_basic_containers=4,
                            max_heavy_containers=4, max_refrigerated_containers=2, max_liquid_containers=2, list_of_containers=[])
        super().__init__(id, current_port, fuel, capacity, fuel_consumption_per_km)
        
    def to_dict(self):
        try:
            containers_list = [container.to_dict() for container in self.list_of_containers if hasattr(container, 'to_dict')]
        except Exception as e:
            print(f"Error while converting containers to dict: {e}")
            containers_list = []
    
        
        return {
            "id": self.id,
            "fuel": self.fuel,
            "containers": containers_list
        }
      
      
class HeavyShip(Ship):
    def __init__(self, id, current_port, fuel, capacity, fuel_consumption_per_km):
        capacity = Capacity(total_weight_capacity=40, max_all_containers=20, max_basic_containers=7,
                            max_heavy_containers=5, max_refrigerated_containers=4, max_liquid_containers=4, list_of_containers=[])
        super().__init__(id, current_port, fuel, capacity, fuel_consumption_per_km)
               
               
               
    def to_dict(self):
        try:
            containers_list = [container.to_dict() for container in self.list_of_containers if hasattr(container, 'to_dict')]
        except Exception as e:
            print(f"Error while converting containers to dict: {e}")
            containers_list = []
    
        
        return {
            "id": self.id,
            "fuel": self.fuel,
            "containers": containers_list
        }
      
class IShipFactory(ABC):
    @abstractmethod
    def create_lightweight_ship(self, id: int, current_port: 'Port', fuel: float) -> LightWeightShip:
        pass
    
    
    @abstractmethod
    def create_medium_ship(self, id: int, current_port: 'Port', fuel: float) -> MediumShip:
        pass
    
    
    @abstractmethod
    def create_heavy_ship(self, id: int, current_port: 'Port', fuel: float) -> HeavyShip:
        pass
    
    
    
class ShipFactory(IShipFactory):
    def create_lightweight_ship(self, id: int, current_port: 'Port', fuel: float) -> LightWeightShip:
        capacity = Capacity(15, 10, 6, 4, 0, 0, [])
        return LightWeightShip(id, current_port, fuel, capacity, fuel_consumption_per_km=0.5)
        
    def create_medium_ship(self, id: int, current_port: 'Port', fuel: float) -> MediumShip:
        capacity = Capacity(25, 12, 4, 4, 2, 2, [])
        return MediumShip(id, current_port, fuel, capacity, fuel_consumption_per_km=1.5)
    
    def create_heavy_ship(self, id: int, current_port: 'Port', fuel: float) -> HeavyShip:
        capacity = Capacity(40, 20, 7, 5, 4, 4, [])
        return HeavyShip(id, current_port, fuel, capacity, fuel_consumption_per_km=4.0)
    
from port import Port
port_a = Port(id=1, coordinates=(54.3520, 18.6466))
factory = ShipFactory()
ship_1 = factory.create_lightweight_ship(id=1, current_port=port_a, fuel = 10000)
print(ship_1)
ship_2 = factory.create_heavy_ship(id=2, current_port=port_a, fuel=15000)
print(ship_2)
ship_2 = factory.create_medium_ship(id=3, current_port=port_a, fuel=12000)
print(ship_2)