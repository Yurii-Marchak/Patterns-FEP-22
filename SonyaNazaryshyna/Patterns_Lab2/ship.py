from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Self
from dataclasses import dataclass
from containers import *
import uuid
if TYPE_CHECKING:
    from port import Port


class IShip(ABC):
    
    @abstractmethod
    def sail_to(self, port: 'Port') -> bool:
        pass
    
    @abstractmethod
    def re_fuel(self, new_fuel) -> None:
        pass
    
    @abstractmethod
    def load(self, cont: 'Container') -> bool:
        pass
    
    @abstractmethod
    def un_load(self, cont: 'Container') -> bool:
        pass
    
@dataclass
class Ship_Configuration:
    total_weight_capasity: int 
    max_number_of_all_containers: int
    max_number_of_heavy_containers: int
    max_number_of_refrigerated_containers: int
    max_number_of_liquid_containers: int
    max_number_of_basic_containers: int
    fuel_consumption_per_km: float
    maximum_amount_of_fuel: float
    

class Ship(IShip):
    """
    Represents a ship that can sail between ports, load and unload containers, and manage fuel.

    Attributes:
        id (UUID): A unique identifier for the ship.
        fuel (float): The current fuel level of the ship.
        current_port (Port): The port where the ship is currently docked.
        ship_configurations (Ship_Configuration): Configuration settings for the ship's capacity and fuel.
        containers_on_the_ship (List[Container]): A list of containers currently loaded on the ship.
    """

    def __init__(self, fuel: float, current_port: 'Port', ship_configurations: Ship_Configuration, containers: List['Container']) -> None:
        self.id = uuid.uuid4()
        self.fuel: float = fuel
        self.current_port = current_port
        self.ship_configurations = ship_configurations
        self.containers_on_the_ship: List[Container] = containers
        self.current_port.incoming_ship(self)

    def _find_nearest_port(self, current_port:'Port', all_ports: List['Port']) -> 'Port':
        """
        Finds the nearest port that the ship can reach based on its current fuel level.

        Args:
            current_port (Port): The current port where the ship is docked.
            all_ports (List[Port]): A list of all available ports.

        Returns:
            Port: The nearest port that can be reached with the remaining fuel.
        """
        neareast_port = None
        min_distance = float('inf')
        for port in all_ports:
            if port == current_port:
                continue
            distance = self.current_port.get_distance(port)
            fuel_consumption = distance * self.ship_configurations.fuel_consumption_per_km
            if neareast_port is None or (distance < min_distance and fuel_consumption <= self.fuel):
                min_distance = distance
                neareast_port = port
        return neareast_port


    def sail_to(self, other_port: 'Port', all_ports: List['Port']) -> bool:
        """
        Sails the ship to a specified port, calculating the distance and fuel consumption.
        If there is not enough fuel, it finds the nearest port to refuel.

        Args:
            other_port (Port): The destination port to sail to.
            all_ports (List[Port]): A list of all available ports for finding the nearest port.

        Returns:
            bool: True if the ship successfully sails to the destination port; otherwise, False.
        """
        distance = self.current_port.get_distance(other_port)
        fuel_consumption = distance * self.ship_configurations.fuel_consumption_per_km
        # print(f"Distance between ports: {distance:.2f} km.")
        
        if fuel_consumption > self.fuel:
            # print(f"Not enough fuel")
            near_port = self._find_nearest_port(self.current_port, all_ports)
            self.current_port.outgoing_ship(self)
            # print(f"Nearest port {near_port}")
            self.current_port = near_port
            self.current_port.incoming_ship(self)
            self.re_fuel(self.ship_configurations.maximum_amount_of_fuel - self.fuel)
            self.sail_to(other_port, all_ports)
        else:
            self.current_port.outgoing_ship(self)
            self.fuel -= fuel_consumption
            self.current_port = other_port
            self.current_port.incoming_ship(self)
            self.current_port = other_port
            
        return distance

    def re_fuel(self, new_fuel) -> None:
        """
        Refuels the ship, ensuring that the fuel level does not exceed the maximum capacity.

        Args:
            new_fuel (float): The amount of fuel to add to the ship's current fuel.
        """
        if self.fuel + new_fuel <= self.ship_configurations.maximum_amount_of_fuel and self.fuel + new_fuel > 0:
            self.fuel += new_fuel
        elif self.fuel + new_fuel >= self.ship_configurations.maximum_amount_of_fuel:
            dif = self.fuel + new_fuel - self.ship_configurations.maximum_amount_of_fuel
            self.fuel = self.ship_configurations.maximum_amount_of_fuel
            
    def get_current_containers(self) -> int:
        """
        Returns the current number of containers loaded on the ship.

        Returns:
            int: The number of containers currently on the ship.
        """
        return len(self.containers_on_the_ship)
     
    def total_weight_on_the_ship(self) -> float:
        """
        Calculates the total weight of all containers currently on the ship.

        Returns:
            float: The total weight of the containers.
        """
        total_weight = sum(container.weight for container in self.containers_on_the_ship)
        return total_weight
    
    def count_container_type(self, container_type) -> int:
        """
        Counts the number of containers of a specific type currently on the ship.

        Args:
            container_type: The type of container to count.

        Returns:
            int: The number of containers of the specified type.
        """
        return sum(1 for container in self.containers_on_the_ship if isinstance(container, container_type))
    
    def _checking_the_type_of_containers(self, cont: 'Container') -> bool:
        """
        Checks if a given container can be loaded onto the ship based on type limits.

        Args:
            cont (Container): The container to check.

        Returns:
            bool: True if the container can be loaded; otherwise, False.
        """
        container_limits = {
            BasicContainer: self.ship_configurations.max_number_of_basic_containers,
            HeavyContainer: self.ship_configurations.max_number_of_heavy_containers,
            RefrigeratedContainer: self.ship_configurations.max_number_of_refrigerated_containers,
            LiquidContainer: self.ship_configurations.max_number_of_liquid_containers
        }
        for container_type, limit in container_limits.items():
            if isinstance(cont, container_type) and self.count_container_type(container_type) >= limit:
                print(f"Cannot load more '{container_type.__name__}': limit reached.")
                return False
        return True

    def load(self, cont: 'Container') -> bool:
        """
        Loads a container onto the ship if it meets capacity and type restrictions.

        Args:
            cont (Container): The container to load onto the ship.

        Returns:
            bool: True if the container was successfully loaded; otherwise, False.
        """
        container_on_ship = self.get_current_containers()
        if cont in self.containers_on_the_ship:
            return False
            
        if container_on_ship >= self.ship_configurations.max_number_of_all_containers:
            return False
        
        if self.total_weight_on_the_ship() + cont.weight > self.ship_configurations.total_weight_capasity:
            return False
                
        if self._checking_the_type_of_containers(cont):
            self.containers_on_the_ship.append(cont)
            return True
        return False
    
    def un_load(self, cont: 'Container', port: 'Port') -> bool:
        """
        Unloads a container from the ship to the specified port.

        Args:
            cont (Container): The container to unload from the ship.
            port (Port): The port to which the container will be unloaded.

        Returns:
            bool: True if the container was successfully unloaded; otherwise, False.
        """
        if cont in self.containers_on_the_ship:
            if cont not in port.containers:
                port.containers.append(cont)
                self.containers_on_the_ship.remove(cont)
            return True
        else:
            return False