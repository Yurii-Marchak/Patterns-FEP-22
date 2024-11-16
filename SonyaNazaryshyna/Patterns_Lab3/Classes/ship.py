from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import uuid
from containers import Container, HeavyContainer, BasicContainer, LiquidContainer, RefrigeratedContainer
from port import Port
from item import Item


class IShip(ABC):
    """
    Interface for ships defining basic operations:
    - sailing to a port
    - refueling
    - loading containers
    - unloading containers
    """
    @abstractmethod
    def sail_to(self, other_port: 'Port', all_ports: List['Port']) -> bool:
        """
        Describes the process of sailing the ship to a specified port.

        Args:
            port (Port): The port to sail to.

        Returns:
            bool: True if the ship successfully reaches the port, False otherwise.
        """

    @abstractmethod
    def re_fuel(self, new_fuel) -> None:
        """
        Refuels the ship with the specified amount of fuel.

        Args:
            new_fuel (float): The amount of fuel to be added.
        """

    @abstractmethod
    def load(self, cont: 'Container') -> bool:
        """
        Loads a container onto the ship.

        Args:
            cont (Container): The container to be loaded.

        Returns:
            bool: True if the container is successfully loaded, False otherwise.
        """

    @abstractmethod
    def un_load(self, cont: 'Container', port: 'Port') -> bool:
        """
        Unloads a container from the ship.

        Args:
            cont (Container): The container to be unloaded.

        Returns:
            bool: True if the container is successfully unloaded, False otherwise.
        """


@dataclass
class Ship_Configuration:
    """
    Data class representing the configuration of a ship, including its capacities 
    and fuel consumption.
    Attributes:
        total_weight_capacity (int): Maximum weight capacity of the ship.
        max_number_of_all_containers (int): Maximum number of containers the ship can carry.
        max_number_of_heavy_containers (int): Maximum number of heavy containers allowed.
        max_number_of_refrigerated_containers (int): Maximum of refrigerated containers allowed.
        max_number_of_liquid_containers (int): Maximum number of liquid containers allowed.
        max_number_of_basic_containers (int): Maximum number of basic containers allowed.
        fuel_consumption_per_km (float): Fuel consumption per kilometer.
        maximum_amount_of_fuel (float): Maximum fuel capacity of the ship.
    """
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
    Represents a ship that can sail between ports, 
    load and unload containers, and manage fuel.

    Attributes:
        id (UUID): A unique identifier for the ship.
        fuel (float): The current fuel level of the ship.
        current_port (Port): The port where the ship is currently docked.
        ship_configurations (Ship_Configuration): Configuration settings 
        for the ship's capacity and fuel.
        containers_on_the_ship (List[Container]): A list of containers currently 
        loaded on the ship.
    """

    def __init__(self, fuel: float, current_port: 'Port', ship_configurations: Ship_Configuration, containers: List['Container'], items: List['Item']) -> None:
        self.ship_id = str(uuid.uuid4())
        self.fuel: float = fuel
        self.current_port = current_port
        self.ship_configurations = ship_configurations
        self.containers_on_the_ship: List[Container] = []
        self.current_port.incoming_ship(self)
        self.items = []

    def ship_data(self):
        """
        Returns a dictionary containing data about the ship.

        This method constructs and returns the ship's data in the form of a dictionary.
        The dictionary includes the ship's unique identifier, current fuel level, the ID 
        of the port the ship is currently at (if any), and a list of containers currently 
        on the ship.

        Returns:
            dict: A dictionary with the following keys:
                - 'Ship ID: ': The unique identifier of the ship (UUID).
                - 'Fuel ': The current fuel level of the ship.
                - 'Port_id': The ID of the port the ship is currently at. Returns None if 
                the ship is not at a port.
                - 'Containers on the ship: ': A list of dictionaries representing the data 
                of each container on the ship.
        """
        return {
            'Ship ID: ': self.ship_id,
            'Fuel ': self.fuel,
            'Port_id': self.current_port.port_id if self.current_port else None,
            'Containers on the ship: ': [container.container_data() for container in self.containers_on_the_ship]
        }

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

        if fuel_consumption > self.fuel:
            near_port = self._find_nearest_port(self.current_port, all_ports)
            self.current_port.outgoing_ship(self)
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
            self.re_fuel(self.ship_configurations.maximum_amount_of_fuel)
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

        Args:`
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
                self.containers_on_the_ship.remove(cont)
                port.containers.append(cont)
            return True
        return False

#-------------------------LAB3------------------------------#

class IShipFactory(ABC):
    """
    Abstract base class for creating ships.

    This class defines the interface for ship factories, which are responsible for
    creating instances of ships based on specific configurations. Concrete factory
    classes must implement the create_ship method to return a new ship instance.
    """

    @abstractmethod
    def create_ship(self, current_port: 'Port') -> IShip:
        """
        Abstract method to create a ship at a specified port.

        This method must be implemented by subclasses of the factory to create a specific
        type of ship and associate it with the provided port. The method returns an object
        implementing the `IShip` interface.

        Args:
            current_port (Port): The port where the newly created ship will be located.

        Returns:
            IShip: An instance of a class that implements the `IShip` interface.
        """


class ShipFactory(IShipFactory):
    """
    ShipFactory is responsible for creating ships of different types. 
    It delegates the creation of 'light', 'medium', and 'heavy' ships to 
    their respective specialized factories: `LightShipFactory`, `MediumShipFactory`, 
    and `HeavyShipFactory`.

    Attributes:
        light_ship_factory (LigthShipFactory): Factory for creating light ships.
        medium_ship_factory (MediumShipFactory): Factory for creating medium ships.
        heavy_ship_factory (HeavyShipFactory): Factory for creating heavy ships.

    Methods:
        create_ship(ship_type: str, current_port: 'Port') -> IShip:
            Creates a ship instance based on the given type ('light', 'medium', 'heavy')
            and assigns it to the specified port.
    """
    def __init__(self):
        self.light_ship_factory = LigthShipFactory()
        self.medium_ship_factory = MediumShipFactory()
        self.heavy_ship_factory = HeavyShipFactory()

    def create_ship(self, ship_type: str, current_port: 'Port') -> IShip:
        """
        Create a new ship instance based on the specified type.

        Args:
            ship_type (str): The type of ship to create ('light', 'medium', 'heavy').
            current_port (Port): The port where the ship will be initially docked.

        Returns:
            IShip: A new instance of the specified type of ship.
        """
        if ship_type == 'light':
            return self.light_ship_factory.create_ship(current_port)
        elif ship_type == 'medium':
            return self.medium_ship_factory.create_ship(current_port)
        elif ship_type == 'heavy':
            return self.heavy_ship_factory.create_ship(current_port)
        else:
            raise ValueError(f"Unknown ship type: {ship_type}")

class LigthShipFactory(IShipFactory):
    """
    Factory class for creating light ships.

    This factory creates instances of light ships with predefined configurations
    such as weight capacity, fuel consumption, and container limits.
    """

    def create_ship(self, current_port: 'Port') -> IShip:
        """
        Create a new light ship instance.

        Args:
            current_port (Port): The port where the ship will be initially docked.

        Returns:
            IShip: A new instance of a light ship.
        """

        ship_config = Ship_Configuration(
            total_weight_capasity=20000,
            max_number_of_all_containers=15,
            max_number_of_heavy_containers=3,
            max_number_of_refrigerated_containers=4,
            max_number_of_liquid_containers=3,
            max_number_of_basic_containers=5,
            fuel_consumption_per_km=1.2,
            maximum_amount_of_fuel=20200
        )
        return Ship(fuel=ship_config.maximum_amount_of_fuel, current_port=current_port, ship_configurations=ship_config, containers=[], items=[])


class MediumShipFactory(IShipFactory):
    """
    Factory class for creating medium ships.

    This factory creates instances of medium ships with predefined configurations
    such as weight capacity, fuel consumption, and container limits.
    """

    def create_ship(self, current_port: 'Port') -> IShip:
        """
        Create a new medium ship instance.

        Args:
            current_port (Port): The port where the ship will be initially docked.

        Returns:
            IShip: A new instance of a medium ship.
        """

        ship_config = Ship_Configuration(
            total_weight_capasity=25000,
            max_number_of_all_containers=20,
            max_number_of_heavy_containers=5,
            max_number_of_refrigerated_containers=7,
            max_number_of_liquid_containers=3,
            max_number_of_basic_containers=5,
            fuel_consumption_per_km=1.5,
            maximum_amount_of_fuel=25000
        )
        return Ship(fuel=ship_config.maximum_amount_of_fuel, current_port=current_port, ship_configurations=ship_config, containers=[], items=[])


class HeavyShipFactory(IShipFactory):
    """
    Factory class for creating heavy ships.

    This factory creates instances of heavy ships with predefined configurations
    such as weight capacity, fuel consumption, and container limits.
    """

    def create_ship(self, current_port: 'Port') -> IShip:
        """
        Create a new heavy ship instance.

        Args:
            current_port (Port): The port where the ship will be initially docked.

        Returns:
            IShip: A new instance of a heavy ship.
        """

        ship_config = Ship_Configuration(
            total_weight_capasity=35000,
            max_number_of_all_containers=30,
            max_number_of_heavy_containers=7,
            max_number_of_refrigerated_containers=6,
            max_number_of_liquid_containers=8,
            max_number_of_basic_containers=9,
            fuel_consumption_per_km=2.2,
            maximum_amount_of_fuel=35000
        )
        return Ship(fuel=ship_config.maximum_amount_of_fuel, current_port=current_port, ship_configurations=ship_config, containers=[], items=[])
