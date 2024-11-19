from typing import List
from math import radians, cos, sin, sqrt, atan2
from port import Port
from containers import Container, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer, create_container

class Ship:
    """
    A class to represent a Ship.

    Attributes:
    -----------
    id : int
        Unique identifier for the ship.
    fuel : float
        Current amount of fuel in the ship.
    current_port : Port
        Port where the ship is currently docked.
    total_weight_capacity : int
        Maximum weight capacity of the ship in kilograms.
    max_containers : int
        Maximum number of containers the ship can carry.
    max_heavy : int
        Maximum number of heavy containers allowed on the ship.
    max_refrigerated : int
        Maximum number of refrigerated containers allowed on the ship.
    max_liquid : int
        Maximum number of liquid containers allowed on the ship.
    fuel_per_km : float
        Amount of fuel consumed per kilometer.
    containers : List[Container]
        List of containers currently loaded onto the ship.

    Methods:
    --------
    sail_to(destination_port: Port):
        Moves the ship to a new port if it has enough fuel to cover the distance.
    load(container: Container) -> bool:
        Loads a container onto the ship if capacity and container limits are not exceeded.
    unload(container: Container) -> bool:
        Unloads a container from the ship if it is present.
    refuel(amount: float) -> None:
        Refuels the ship with the specified amount of fuel.
    """
    def __init__(self, id: int, fuel: float, current_port: Port, total_weight_capacity: int, max_containers: int, max_heavy: int, max_refrigerated: int, max_liquid: int, fuel_per_km: float):
        """
        Initialize a new Ship object.

        Parameters:
        -----------
        id : int
            Unique identifier for the ship.
        fuel : float
            Initial fuel level for the ship.
        current_port : Port
            The port where the ship is initially docked.
        total_weight_capacity : int
            Maximum weight capacity of the ship in kilograms.
        max_containers : int
            Maximum number of containers the ship can carry.
        max_heavy : int
            Maximum number of heavy containers allowed.
        max_refrigerated : int
            Maximum number of refrigerated containers allowed.
        max_liquid : int
            Maximum number of liquid containers allowed.
        fuel_per_km : float
            Amount of fuel the ship consumes per kilometer.
        """
        self.id = id
        self.fuel = fuel
        self.current_port = current_port
        self.total_weight_capacity = total_weight_capacity
        self.max_containers = max_containers
        self.max_heavy = max_heavy
        self.max_refrigerated = max_refrigerated
        self.max_liquid = max_liquid
        self.fuel_per_km = fuel_per_km
        self.containers: List[Container] = []

    def sail_to(self, destination_port):
        """
        Moves the ship to the specified destination port if it has enough fuel to cover the distance.
        Deducts the necessary fuel and updates the current port of the ship.

        Parameters:
        -----------
        destination_port : Port
        The port to which the ship will sail.
        """
        distance = self.current_port.get_distance(destination_port)
        fuel_needed = distance * self.fuel_per_km

        if self.fuel >= fuel_needed:
            self.fuel -= fuel_needed
            self.current_port.outgoing_ship(self)
            destination_port.incoming_ship(self)
            self.current_port = destination_port
            print(f"Ship {self.id} successfully sailed to port {destination_port.id}. Distance: {distance:.2f} km. Fuel used: {fuel_needed:.2f}. Remaining fuel: {self.fuel:.2f}.")
        else:
            print(f"Ship {self.id} does not have enough fuel to sail to port {destination_port.id}. Needed: {fuel_needed:.2f}, Available: {self.fuel:.2f}.")

    def load(self, container: Container) -> bool:
        """
        Loads a container onto the ship if there is space and weight capacity, and 
        the container type limits (heavy, refrigerated, liquid) are not exceeded.

        Parameters:
        -----------
        container : Container
        The container to be loaded onto the ship.

        Returns:
        --------
        bool
        True if the container is successfully loaded, False otherwise.
        """
        if len(self.containers) >= self.max_containers:
            print(f"Ship {self.id}: Max container capacity reached.")
            return False

        current_weight = sum(c.weight for c in self.containers)
        if current_weight + container.weight > self.total_weight_capacity:
            print(f"Ship {self.id}: Max weight capacity exceeded.")
            return False

        if isinstance(container, HeavyContainer) and len([c for c in self.containers if isinstance(c, HeavyContainer)]) >= self.max_heavy:
            print(f"Ship {self.id}: Max heavy containers reached.")
            return False

        if isinstance(container, RefrigeratedContainer) and len([c for c in self.containers if isinstance(c, RefrigeratedContainer)]) >= self.max_refrigerated:
            print(f"Ship {self.id}: Max refrigerated containers reached.")
            return False

        if isinstance(container, LiquidContainer) and len([c for c in self.containers if isinstance(c, LiquidContainer)]) >= self.max_liquid:
            print(f"Ship {self.id}: Max liquid containers reached.")
            return False

        self.containers.append(container)
        return True

    def unload(self, container: Container) -> bool:
        """
        Unloads a container from the ship if it is present.

        Parameters:
        -----------
        container : Container
        The container to be unloaded.

        Returns:
        --------
        bool
        True if the container is successfully unloaded, False if the container was not found.
        """
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

    def refuel(self, amount: float) -> None:
        """
        Refuels the ship by the specified amount.

        Parameters:
        -----------
        amount : float
            The amount of fuel to add to the ship.
        """
        self.fuel += amount
