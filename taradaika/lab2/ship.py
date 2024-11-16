from port import *
from typing import List
from container import Container
if TYPE_CHECKING:
    from port import *
    from container import *


class Capacity:
    def __init__(self, total_weight_capacity: float, max_all_containers: float, 
                 max_heavy_containers: float, max_refrigerated_containers: float, 
                 max_liquid_containers: float, list_of_containers: List['Container']):
        self.total_weight_capacity = total_weight_capacity
        self.max_all_containers = max_all_containers
        self.max_heavy_containers = max_heavy_containers
        self.max_refrigerated_containers = max_refrigerated_containers
        self.max_liquid_containers = max_liquid_containers
        
        self.current_total_weight = 0.0
        self.current_all_containers = 0.0
        self.current_heavy_containers = 0.0 
        self.current_refrigerated_containers = 0.0
        self.current_liquid_containers = 0.0
        
        
        
    def check_if_enough_space(self, list_of_containers: list, container: 'Container') -> bool:
        if (self.current_total_weight + container.weight >=  self.total_weight_capacity or self.current_all_containers > max_all_containers):
            return False
        
        if isinstance(container, HeavyContainer) and self.current_heavy_containers > self.max_heavy_containers:
            return False
            
        if isinstance(container, LiquidContainer) and self.current_liquid_containers > self.max_liquid_containers:
            return False
        
        if isinstance(container, HeavyContainer) and self.current_heavy_containers > self.max_heavy_containers:
            return False
       
        return True


    def add_container(self, container: 'Container') -> None:
        self.current_total_weight += container.weight
        self.current_all_containers += 1
        
        if isinstance(container, HeavyContainer):
            self.current_heavy_containers += 1
        elif isinstance(container, RefrigeratedContainer):
            self.current_refrigerated_containers += 1
        elif isinstance(container, LiquidContainer):
            self.current_liquid_containers += 1
    
    def remove_container(self, container: 'Container') -> None:
        self.current_total_weight -= container.weight
        self.current_all_containers -= 1
        
        if isinstance(container, HeavyContainer):
            self.current_heavy_containers -= 1
        elif isinstance(container, RefrigeratedContainer):
            self.current_refrigerated_containers -= 1
        elif isinstance(container, LiquidContainer):
            self.current_liquid_containers -= 1
    
class IShip(ABC):
    def __init__(self, id: int, current_port: 'Port', fuel: float, capacity: Capacity, fuel_consuption_per_km: float, list_of_containers: List['Container'] ) -> None:
        self.id: int  = id
        self.current_port: Port = current_port
        self.fuel: float  = fuel
        self.capacity: Capacity = capacity
        self.fuel_consuption_per_km: float = fuel_consuption_per_km
        self.list_of_containers: List[Container] = []
        
        
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
    def re_fuel(self, fuel: float, fuel_consuption_per_km: float ) -> None:
        pass
    
class Ship(IShip):
    def __init__(self, id: int, current_port: 'Port', fuel: float, capacity: Capacity, fuel_consumption_per_km: float, list_of_containers: List['Container']) -> None:
        super().__init__(id, current_port, fuel, capacity, fuel_consumption_per_km, list_of_containers)
       
       
    def sail_to(self, port: 'Port') -> bool:
        
        distance = self.current_port.get_distance(port)
        
        required_fuel = distance * self.total_fuel_consumption_per_km()
        print(f"Необхідно палива для подорожі: {required_fuel:.2f} літрів")
        if self.fuel >= required_fuel:
            self.fuel -= required_fuel
        
            self.current_port = port
            print(f"Корабель успішно приплив до порту B.")
            return True
        else:
            print(f"Не вистачає палива для подорожі. Дозаправка необхідна.")
            return False
     
     
    def total_fuel_consumption_per_km(self) -> float:
        total_consumption = self.fuel_consuption_per_km
        
        for container in self.list_of_containers:
            total_consumption += container.consumption()
            
        return total_consumption
        
        
        
    def load(self, container: Container) -> bool:
        if self.capacity.check_if_enough_space(self.list_of_containers, container):
            self.list_of_containers.append(container)
            self.capacity.add_container(container)
            print(f"Контейнери успішно завантажені у порт B.")
            return True
        return False
    
    def unload(self, container: Container) -> bool:
        if container in self.list_of_containers:
            self.list_of_containers.remove(container)
            self.capacity.remove_container(container)
            print(f"Контейнери успішно розвантажені у порт B.")
            return True
        return False
            
            
    def re_fuel(self, fuel: float, fuel_consuption_per_km: float ) -> None:
        self.fuel += fuel