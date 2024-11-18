"""
Ship classes

This module defines the structure and behavior of ships within a shipping simulation.

Classes:
    IShip: An abstract base class that defines the interface for ship operations.
    Ship: A concrete implementation of the IShip interface, representing a cargo ship
          capable of loading and unloading different types of containers, sailing to ports,
          and managing fuel consumption.

Key Functionalities:
    - Loading and unloading containers with weight and type checks.
    - Sailing to different ports while calculating fuel consumption based on distance
      and current container loads.
    - Refueling operations to manage the ship's fuel reserves.
    - Retrieving the list of currently loaded containers, sorted by their identifier.

This module relies on other modules such as `port` and `container`, which define
the port and container classes used in ship operations.
"""
from abc import abstractmethod, ABC
from dataclasses import dataclass
from container import HeavyContainer
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from port import Port, IPort
    from container import Container


class IShip(ABC):
    """Abstract base class for ships."""

    @abstractmethod
    def sail_to(self, port: 'IPort') -> bool:
        """Sails the ship to the specified port.

        Args:
            port (IPort): The port to sail to.

        Returns:
            bool: True if the ship successfully sails to the port, False otherwise.
        """
        pass

    @abstractmethod
    def re_fuel(self, new_fuel: float) -> None:
        """Refuels the ship with the specified amount of fuel.

        Args:
            new_fuel (float): The amount of fuel to add.
        """
        pass

    @abstractmethod
    def load(self, cont: 'Container') -> bool:
        """Loads a container onto the ship.

        Args:
            cont (Container): The container to load.

        Returns:
            bool: True if the container is successfully loaded, False otherwise.
        """
        pass

    @abstractmethod
    def unload(self, cont: 'Container') -> bool:
        """Unloads a container from the ship.

        Args:
            cont (Container): The container to unload.

        Returns:
            bool: True if the container is successfully unloaded, False otherwise.
        """
        pass


class Ship(IShip):
    """Class representing a ship with cargo management capabilities."""

    def __init__(self, identifier: int, fuel: float, current_port: 'Port', total_weight_capacity: float,
                 max_number_of_containers: Dict[str, int], fuel_consumption: float):
        """Initializes a Ship instance.

        Args:
            identifier (int): Unique identifier for the ship.
            fuel (float): Initial fuel amount.
            current_port (Port): The port the ship is currently docked at.
            total_weight_capacity (float): Maximum weight capacity of the ship.
            max_number_of_containers (Dict[str, int]): Maximum number of each type of container.
            fuel_consumption (float): Fuel consumption per kilometer.
        """
        self.id: int = identifier
        self.fuel: float = fuel
        self.current_port: 'Port' = current_port
        self.total_weight_capacity: float = total_weight_capacity
        self.fuel_consumption_per_KM: float = fuel_consumption
        self.max_number_of_containers: Dict[str, int] = max_number_of_containers
        self.number_of_containers: Dict[str, int] = {
            'Container': 0,
            'HeavyContainer': 0,
            'LiquidContainer': 0,
            'RefrigeratedContainer': 0
        }
        self.weight_of_containers: float = 0
        self.containers: List['Container'] = []

    def re_fuel(self, new_fuel: float) -> None:
        """Refuels the ship with the specified amount of fuel.

        Args:
            new_fuel (float): The amount of fuel to add.
        """
        self.fuel += new_fuel

    def sail_to(self, port: 'IPort') -> bool:
        """Sails the ship to the specified port.

        Args:
            port (IPort): The port to sail to.

        Returns:
            bool: True if the ship successfully sails to the port, False otherwise.
        """
        if not isinstance(port, self.current_port.__class__):
            raise Exception('Cannot reach this port (maybe is not a port)')
        consumed_fuel = self.current_port.get_distance(port) * self.fuel_consumption_per_KM
        for container in self.containers:
            consumed_fuel += container.consumption()
        if consumed_fuel <= self.fuel:
            self.fuel -= consumed_fuel
            self.current_port.outgoing_ship(self)
            self.current_port = port
            self.current_port.incoming_ship(self)
            return True
        return False

    def load(self, cont: 'Container') -> bool:
        """Loads a container onto the ship.

        Args:
            cont (Container): The container to load.

        Returns:
            bool: True if the container is successfully loaded, False otherwise.
        """
        if cont not in self.current_port.containers:
            return False
        if self.weight_of_containers + cont.weight > self.total_weight_capacity:
            return False
        if self.max_number_of_containers['Container'] == self.number_of_containers['Container']:
            return False
        if isinstance(cont, HeavyContainer):
            if self.max_number_of_containers['HeavyContainer'] == self.number_of_containers['HeavyContainer']:
                return False
            if self.max_number_of_containers[cont.__class__.__name__] == self.number_of_containers[cont.__class__.__name__]:
                return False
        self.weight_of_containers += cont.weight
        self.number_of_containers['Container'] += 1
        if isinstance(cont, HeavyContainer):
            self.number_of_containers['HeavyContainer'] += 1
            if cont.__class__.__name__ != 'HeavyContainer':
                self.number_of_containers[cont.__class__.__name__] += 1
        self.containers.append(cont)
        self.current_port.containers.remove(cont)
        return True

    def unload(self, cont: 'Container') -> bool:
        """Unloads a container from the ship.

        Args:
            cont (Container): The container to unload.

        Returns:
            bool: True if the container is successfully unloaded, False otherwise.
        """
        if cont not in self.containers:
            return False
        self.weight_of_containers -= cont.weight
        self.number_of_containers['Container'] -= 1
        if isinstance(cont, HeavyContainer):
            self.number_of_containers['HeavyContainer'] -= 1
            self.number_of_containers[cont.__class__.__name__] -= 1
        self.containers.remove(cont)
        self.current_port.containers.append(cont)
        return True

    def get_current_containers(self) -> List['Container']:
        """Gets a sorted list of the current containers on the ship.

        Returns:
            List[Container]: A sorted list of containers currently on board.
        """
        containers = self.containers.copy()
        containers.sort(key=lambda cont: cont.id)
        return containers

    def get_fuel(self) -> float:
        """Returns the current amount of fuel in the ship.

        Returns:
            float: Current fuel amount.
        """
        return self.fuel


class LightWeightShip(Ship):
    """Lightweight ship class with lower weight capacity."""

    def __init__(self, identifier: int, fuel: float, current_port: 'Port'):
        """Initializes a LightWeightShip instance.

        Args:
            identifier (int): Unique identifier for the ship.
            fuel (float): Initial fuel amount.
            current_port (Port): The port the ship is currently docked at.
        """
        super().__init__(identifier, fuel, current_port, total_weight_capacity=30000.0,
                         max_number_of_containers={'Container': 10, 'HeavyContainer': 0, 'LiquidContainer': 0, 'RefrigeratedContainer': 0},
                         fuel_consumption=10)
        self.fuel_capacity = 2_000_000

    def re_fuel(self, new_fuel: float) -> None:
        """Refuels the ship with the specified amount of fuel, ensuring it does not exceed capacity.

        Args:
            new_fuel (float): The amount of fuel to add.
        """
        if super().get_fuel() + new_fuel <= self.fuel_capacity:
            super().re_fuel(new_fuel)


@dataclass
class Placeholder:
    """Placeholder class for container counts and types."""

    type: str
    count_of_cont: int


class MediumShip(Ship):
    """Medium ship class with moderate weight capacity and a fuel bank."""

    def __init__(self, identifier: int, fuel: float, current_port: 'Port', placeholder: Placeholder = Placeholder('', 0)):
        """Initializes a MediumShip instance.

        Args:
            identifier (int): Unique identifier for the ship.
            fuel (float): Initial fuel amount.
            current_port (Port): The port the ship is currently docked at.
            placeholder (Placeholder): Container specifications for loading.
        """
        l_container_number = 0
        r_container_number = 0
        if placeholder.type == 'L':
            l_container_number += placeholder.count_of_cont
        if placeholder.type == 'R':
            r_container_number += placeholder.count_of_cont
        super().__init__(identifier, fuel, current_port, total_weight_capacity=80000.0,
                         max_number_of_containers={'Container': 20, 'HeavyContainer': 5, 'LiquidContainer': l_container_number, 'RefrigeratedContainer': r_container_number},
                         fuel_consumption=30)
        self.fuel_capacity = 4_000_000

    def re_fuel(self, new_fuel: float) -> None:
        """Refuels the ship with the specified amount of fuel, ensuring it does not exceed capacity.

        Args:
            new_fuel (float): The amount of fuel to add.
        """
        if super().get_fuel() + new_fuel <= self.fuel_capacity:
            super().re_fuel(new_fuel)


class HeavyShip(Ship):
    """Heavy ship class with high weight capacity and extended fuel bank."""

    def __init__(self, identifier: int, fuel: float, current_port: 'Port', placeholder: Placeholder = Placeholder('', 0)):
        """Initializes a HeavyShip instance.

        Args:
            identifier (int): Unique identifier for the ship.
            fuel (float): Initial fuel amount.
            current_port (Port): The port the ship is currently docked at.
            placeholder (Placeholder): Container specifications for loading.
        """
        l_container_number = 0
        r_container_number = 0
        if placeholder.type == 'L':
            l_container_number += placeholder.count_of_cont
        if placeholder.type == 'R':
            r_container_number += placeholder.count_of_cont
        super().__init__(identifier, fuel, current_port, total_weight_capacity=100000.0,
                         max_number_of_containers={'Container': 30, 'HeavyContainer': 10, 'LiquidContainer': l_container_number, 'RefrigeratedContainer': r_container_number},
                         fuel_consumption=50)
        self.fuel_capacity = 6_000_000

    def re_fuel(self, new_fuel: float) -> None:
        """Refuels the ship with the specified amount of fuel, ensuring it does not exceed capacity.

        Args:
            new_fuel (float): The amount of fuel to add.
        """
        if super().get_fuel() + new_fuel <= self.fuel_capacity:
            super().re_fuel(new_fuel)
