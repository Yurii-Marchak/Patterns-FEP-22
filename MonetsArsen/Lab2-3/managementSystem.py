"""
Management system class

This module defines the PortManagementSystem class for managing ports, ships, and containers
in a shipping simulation. It provides functionalities to create and manage containers, ports,
and ships, as well as to print information about the ports in the system.

Classes:
    PortManagementSystem: A system for managing ports, ships, and containers.
"""
from typing import List, Optional
from abc import ABC, abstractmethod

from port import Port, IPort
from ship import Ship, IShip, LightWeightShip, MediumShip, HeavyShip, Placeholder
from item import Item
from container import Container, BasicContainer, HeavyContainer, LiquidContainer, RefrigeratedContainer

class IPortManagementSystem(ABC):
    """Interface for port management system operations."""

    @abstractmethod
    def create_container(self, port_id: int, weight: float, state: str = 'N', *items: Item) -> Container:
        """Creates a new container and adds it to the specified port."""
        pass

    @abstractmethod
    def create_port(self, longitude: float, latitude: float) -> IPort:
        """Creates a new port and adds it to the system."""
        pass

    @abstractmethod
    def create_ship(self, port_id: int, max_weight: float, max_number: int,
                    max_heavy_cont_number: int, max_liquid_cont_number: int,
                    max_refrigerated_cont_number: int, consumption: float) -> IShip:
        """Creates a new ship and adds it to the specified port."""
        pass

    @abstractmethod
    def print_ports_information(self) -> None:
        """Prints information about all ports in the system."""
        pass


class PortManagementSystem(IPortManagementSystem):
    """A system for managing ports, ships, and containers."""

    def __init__(self):
        """Initializes the PortManagementSystem with counters and a list of ports."""
        self.container_id_count = 0
        self.port_id_count = 0
        self.ship_id_count = 0
        self.ports: List['Port'] = []

    def create_container(self, port_id: int, weight: float, state: str = 'N', *items: Item) -> Container:
        """Creates a new container and adds it to the specified port.

        Args:
            port_id (int): The ID of the port to which the container will be added.
            weight (float): The weight of the container.
            state (str): The state of the container ('N' for normal, 'L' for liquid,
                         'R' for refrigerated). Defaults to 'N'.

        Returns:
            Container: The created container.

        Raises:
            Exception: If the state is invalid.
        """
        if state not in ['N', 'L', 'R']:
            raise Exception('Invalid state')
        self.container_id_count += 1
        if weight <= 3000:
            container = BasicContainer(weight=weight, identifier=self.container_id_count)
        else:
            if state == 'L':
                container = LiquidContainer(weight=weight, identifier=self.container_id_count)
            elif state == 'R':
                container = RefrigeratedContainer(weight=weight, identifier=self.container_id_count)
            else:
                container = HeavyContainer(weight=weight, identifier=self.container_id_count)
        self.ports[port_id - 1].containers.append(container)
        return container

    def create_port(self, longitude: float, latitude: float) -> IPort:
        """Creates a new port and adds it to the system.

        Args:
            longitude (float): The longitude of the new port.
            latitude (float): The latitude of the new port.

        Returns:
            IPort: The newly created port.
        """
        self.port_id_count += 1
        self.ports.append(Port(self.port_id_count, (latitude, longitude)))
        return self.ports[self.port_id_count - 1]

    def create_ship(self, port_id: int, max_weight: float, max_number: int,
                    max_heavy_cont_number: int, max_liquid_cont_number: int,
                    max_refrigerated_cont_number: int, consumption: float) -> IShip:
        """Creates a new ship and adds it to the specified port.

        Args:
            port_id (int): The ID of the port where the ship will dock.
            max_weight (float): The maximum weight capacity of the ship.
            max_number (int): The maximum number of containers the ship can carry.
            max_heavy_cont_number (int): Maximum number of heavy containers.
            max_liquid_cont_number (int): Maximum number of liquid containers.
            max_refrigerated_cont_number (int): Maximum number of refrigerated containers.
            consumption (float): Fuel consumption per kilometer for the ship.

        Returns:
            IShip: The newly created ship.
        """
        self.ship_id_count += 1
        max_number_cont = {
            Container.__name__: max_number,
            HeavyContainer.__name__: max_heavy_cont_number,
            LiquidContainer.__name__: max_liquid_cont_number,
            RefrigeratedContainer.__name__: max_refrigerated_cont_number
        }
        ship = Ship(self.ship_id_count, 0, self.ports[port_id - 1], max_weight, max_number_cont, consumption)
        self.ports[port_id - 1].incoming_ship(ship)
        return ship

    def print_ports_information(self) -> None:
        """Prints information about all ports in the system, including
        their ID, coordinates, containers, ship history, and current ships."""
        for port in self.ports:
            print(
                f"Id: {port.id}. Coordinates: {port.coordinates}. Containers: {port.containers}. "
                f"Ship history: {port.ship_history}. Current ships: {port.ship_current}"
            )


class AdvancedPortManagementSystem(IPortManagementSystem):
    """Advanced management system for managing ports with additional functionalities."""

    def __init__(self):
        """Initializes the AdvancedPortManagementSystem."""
        self.port_management = PortManagementSystem()

    def create_container(self, port_id: int, weight: float, state: str = 'N', *items: Item) -> Container:
        """Creates a container and adds it to the specified port, managing item placement.

        Args:
            port_id (int): The ID of the port to which the container will be added.
            weight (float): The weight of the container.
            state (str): The state of the container ('N', 'L', 'R'). Defaults to 'N'.
            items (Item): Additional items to add to the container.

        Returns:
            Container: The created container.

        Raises:
            Exception: If there is not enough space for the items or if their states do not match.
        """
        container = self.port_management.create_container(port_id, weight, state)
        total_weight = 0
        for item in items:
            if total_weight + item.get_total_weight() > weight:
                raise Exception(f"Cannot put item {item.get_item_details()} in container (no space)")
            item_state = 'N' if item.__class__.__name__ == 'Normal' else 'L' if item.__class__.__name__ == 'Liquid' else 'R'
            if state != item_state:
                raise Exception(f"Cannot put item {item.get_item_details()} in container (state mismatch)")
            total_weight += item.get_total_weight()
            container.add_item(item)
            item.set_container(container)
        return container

    def create_port(self, longitude: float, latitude: float) -> IPort:
        """Creates a new port in the advanced system.

        Args:
            longitude (float): The longitude of the new port.
            latitude (float): The latitude of the new port.

        Returns:
            IPort: The newly created port.
        """
        return self.port_management.create_port(latitude=latitude, longitude=longitude)

    def create_ship(self, port_id: int, max_weight: float, max_number: int, max_heavy_cont_number: int,
                    max_liquid_cont_number: int, max_refrigerated_cont_number: int, consumption: float) -> IShip:
        """Creates a new ship with specific constraints and adds it to the specified port.

        Args:
            port_id (int): The ID of the port where the ship will dock.
            max_weight (float): The maximum weight capacity of the ship.
            max_number (int): The maximum number of containers the ship can carry.
            max_heavy_cont_number (int): Maximum number of heavy containers.
            max_liquid_cont_number (int): Maximum number of liquid containers.
            max_refrigerated_cont_number (int): Maximum number of refrigerated containers.
            consumption (float): Fuel consumption per kilometer for the ship.

        Returns:
            IShip: The newly created ship.

        Raises:
            Exception: If the ship cannot be created due to constraints.
        """
        builders: List[IShipBuilder] = [
            LightWeightShipBuilder(self.port_management.ship_id_count + 1, self.port_management.ports[port_id - 1],
                                   max_weight, max_number, max_heavy_cont_number, max_liquid_cont_number,
                                   max_refrigerated_cont_number, consumption),
            MediumShipBuilder(self.port_management.ship_id_count + 1, self.port_management.ports[port_id - 1],
                                   max_weight, max_number, max_heavy_cont_number, max_liquid_cont_number,
                                   max_refrigerated_cont_number, consumption),
            HeavyShipBuilder(self.port_management.ship_id_count + 1, self.port_management.ports[port_id - 1],
                                   max_weight, max_number, max_heavy_cont_number, max_liquid_cont_number,
                                   max_refrigerated_cont_number, consumption),
        ]
        director = ShipDirector(builders[0])
        for builder in builders:
            director.change_builder(builder)
            ship = director.try_create_ship()
            if ship is not None:
                self.port_management.ship_id_count += 1
                self.port_management.ports[port_id - 1].incoming_ship(ship)
                return ship
        raise Exception(f"Too big requirements")

    def print_ports_information(self) -> None:
        """Prints information about all ports in the advanced system."""
        return self.port_management.print_ports_information()


class AbstractPlaceholderFactory(ABC):
    """Abstract factory class for creating placeholders."""

    @classmethod
    @abstractmethod
    def create_liquid_placeholder(cls) -> Placeholder:
        """Creates a liquid placeholder."""
        pass

    @classmethod
    @abstractmethod
    def create_refrigerated_placeholder(cls) -> Placeholder:
        """Creates a refrigerated placeholder."""
        pass

    @classmethod
    def create_default_placeholder(cls) -> Placeholder:
        """Creates a default placeholder."""
        return Placeholder('', 0)


class MediumPlaceHolderFactory(AbstractPlaceholderFactory):
    """Factory class for creating medium placeholders."""

    @classmethod
    def create_liquid_placeholder(cls) -> Placeholder:
        """Creates a medium liquid placeholder."""
        return Placeholder('L', 2)

    @classmethod
    def create_refrigerated_placeholder(cls) -> Placeholder:
        """Creates a medium refrigerated placeholder."""
        return Placeholder('R', 2)


class HeavyPlaceHolderFactory(AbstractPlaceholderFactory):
    """Factory class for creating heavy placeholders."""

    @classmethod
    def create_liquid_placeholder(cls) -> Placeholder:
        """Creates a heavy liquid placeholder."""
        return Placeholder('L', 5)

    @classmethod
    def create_refrigerated_placeholder(cls) -> Placeholder:
        """Creates a heavy refrigerated placeholder."""
        return Placeholder('R', 5)


class IShipBuilder(ABC):
    """Abstract base class for ship builders."""

    def __init__(self, ship_id: int, port: 'Port', max_weight: float, max_number: int,
                 max_heavy_cont_number: int, max_liquid_cont_number: int,
                 max_refrigerated_cont_number: int, consumption: float):
        """Initializes the ship builder with specifications."""
        self.ship_id = ship_id
        self.port = port
        self.weight = max_weight
        self.cont = max_number
        self.h_cont = max_heavy_cont_number
        self.l_cont = max_liquid_cont_number
        self.r_cont = max_refrigerated_cont_number
        self.consumption = consumption

    @abstractmethod
    def check_req(self) -> bool:
        """Checks if the requirements for building the ship are met."""
        pass

    @abstractmethod
    def get_placeholder(self) -> Placeholder:
        """Gets the placeholder needed for the ship."""
        pass

    @abstractmethod
    def create_ship(self, placeholder: 'Placeholder') -> IShip:
        """Creates a ship using the provided placeholder."""
        pass


class ShipDirector:
    """Director for constructing ships using builders."""

    def __init__(self, builder: IShipBuilder):
        """Initializes the director with a builder."""
        self.builder = builder

    def change_builder(self, builder: IShipBuilder):
        """Changes the current builder to a new one."""
        self.builder = builder

    def try_create_ship(self) -> Optional[IShip]:
        """Attempts to create a ship using the current builder.

        Returns:
            Optional[IShip]: The created ship, or None if the requirements are not met.
        """
        if not self.builder.check_req():
            return None
        placeholder = self.builder.get_placeholder()
        return self.builder.create_ship(placeholder)


class LightWeightShipBuilder(IShipBuilder):
    """Builder for lightweight ships."""

    def __init__(self, ship_id: int, port: 'Port', max_weight: float, max_number: int,
                 max_heavy_cont_number: int, max_liquid_cont_number: int,
                 max_refrigerated_cont_number: int, consumption: float):
        """Initializes the lightweight ship builder with specifications."""
        super().__init__(ship_id, port, max_weight, max_number, max_heavy_cont_number,
                         max_liquid_cont_number, max_refrigerated_cont_number, consumption)

    def check_req(self) -> bool:
        """Checks if the requirements for building a lightweight ship are met."""
        return (self.cont <= 10 and self.h_cont == self.l_cont == self.r_cont == 0
                and self.consumption <= 10 and self.weight <= 30000)

    def get_placeholder(self) -> Placeholder:
        """Gets a default placeholder for a lightweight ship."""
        return AbstractPlaceholderFactory.create_default_placeholder()

    def create_ship(self, placeholder: 'Placeholder') -> IShip:
        """Creates a lightweight ship using the provided placeholder."""
        return LightWeightShip(identifier=self.ship_id, fuel=0, current_port=self.port)


class MediumShipBuilder(IShipBuilder):
    """Builder for medium ships."""

    def __init__(self, ship_id: int, port: 'Port', max_weight: float, max_number: int,
                 max_heavy_cont_number: int, max_liquid_cont_number: int,
                 max_refrigerated_cont_number: int, consumption: float):
        """Initializes the medium ship builder with specifications."""
        super().__init__(ship_id, port, max_weight, max_number, max_heavy_cont_number,
                         max_liquid_cont_number, max_refrigerated_cont_number, consumption)

    def check_req(self) -> bool:
        """Checks if the requirements for building a medium ship are met."""
        return (self.cont <= 20 and self.h_cont <= 5 and self.consumption <= 30
                and self.weight <= 80000 and
                ((self.l_cont <= 2 and self.r_cont == 0) or (self.l_cont == 0 and self.r_cont <= 2)))

    def get_placeholder(self) -> Placeholder:
        """Gets the appropriate placeholder for a medium ship."""
        if 2 >= self.l_cont > 0 and self.r_cont == 0:
            return MediumPlaceHolderFactory.create_liquid_placeholder()
        if self.l_cont == 0 and 0 < self.r_cont <= 2:
            return MediumPlaceHolderFactory.create_refrigerated_placeholder()
        return MediumPlaceHolderFactory.create_default_placeholder()

    def create_ship(self, placeholder: 'Placeholder') -> IShip:
        """Creates a medium ship using the provided placeholder."""
        return MediumShip(identifier=self.ship_id, fuel=0, current_port=self.port, placeholder=placeholder)


class HeavyShipBuilder(IShipBuilder):
    """Builder for heavy ships."""

    def __init__(self, ship_id: int, port: 'Port', max_weight: float, max_number: int,
                 max_heavy_cont_number: int, max_liquid_cont_number: int,
                 max_refrigerated_cont_number: int, consumption: float):
        """Initializes the heavy ship builder with specifications."""
        super().__init__(ship_id, port, max_weight, max_number, max_heavy_cont_number,
                         max_liquid_cont_number, max_refrigerated_cont_number, consumption)

    def check_req(self) -> bool:
        """Checks if the requirements for building a heavy ship are met."""
        return (self.cont <= 30 and self.h_cont <= 15 and self.consumption <= 50
                and self.weight <= 100000 and
                ((self.l_cont <= 5 and self.r_cont == 0) or (self.l_cont == 0 and self.r_cont <= 5)))

    def get_placeholder(self) -> Placeholder:
        """Gets the appropriate placeholder for a heavy ship."""
        if 5 >= self.l_cont > 0 and self.r_cont == 0:
            return HeavyPlaceHolderFactory.create_liquid_placeholder()
        if self.l_cont == 0 and 0 < self.r_cont <= 5:
            return HeavyPlaceHolderFactory.create_refrigerated_placeholder()
        return HeavyPlaceHolderFactory.create_default_placeholder()

    def create_ship(self, placeholder: 'Placeholder') -> IShip:
        """Creates a heavy ship using the provided placeholder."""
        return HeavyShip(identifier=self.ship_id, fuel=0, current_port=self.port, placeholder=placeholder)
