"""
Container Class Hierarchy

This module defines an abstract base class `Container` and several concrete container
classes that inherit from it, each with its own consumption calculation logic.

Classes:
    Container (ABC): An abstract base class for containers.
    BasicContainer: A basic container with a fixed consumption rate.
    HeavyContainer: A heavy container with a higher consumption rate.
    LiquidContainer: A liquid container with an even higher consumption rate.
    RefrigeratedContainer: A refrigerated container with the highest consumption rate.
"""

from abc import abstractmethod, ABC
from typing import Self, List
from item import Item

class Container(ABC):
    """
    An abstract base class for containers.

    Attributes:
        id (int): The unique identifier for the container.
        weight (float): The weight of the container.
    """

    def __init__(self, identifier: int, weight: float) -> None:
        """
        Initialize a Container object.

        Args:
            identifier (int): The unique identifier for the container.
            weight (float): The weight of the container.
        """
        self.id = identifier
        self.weight = weight
        self.items: List[Item] = []

    @abstractmethod
    def consumption(self) -> float:
        """
        Calculate the consumption of the container.

        Returns:
            float: The consumption of the container.
        """
        pass

    def equals(self, other_container: Self) -> bool:
        """
        Check if two containers are equal.

        Args:
            other_container (Container): The other container to compare.

        Returns:
            bool: True if the containers are equal, False otherwise.
        """
        if self.__class__.__name__ == other_container.__class__.__name__ and self.weight == other_container.weight:
            return True
        return False

    def add_item(self, item: Item):
        """
        Add item to container
        :param item: item to add
        :return:
        """
        self.items.append(item)

class BasicContainer(Container):
    """
    A basic container with a fixed consumption rate.

    Attributes:
        UNIT (float): The constant consumption rate for basic containers.
    """

    UNIT = 2.5

    def __init__(self, identifier: int, weight: float) -> None:
        """
        Initialize a BasicContainer object.

        Args:
            identifier (int): The unique identifier for the container.
            weight (float): The weight of the container.
        """
        super().__init__(identifier, weight)

    def consumption(self) -> float:
        """
        Calculate the consumption of the basic container.

        Returns:
            float: The consumption of the basic container.
        """
        return self.weight * self.UNIT

class HeavyContainer(Container):
    """
    A heavy container with a higher consumption rate.

    Attributes:
        UNIT (float): The constant consumption rate for heavy containers.
    """

    UNIT = 3.0

    def __init__(self, identifier: int, weight: float) -> None:
        """
        Initialize a HeavyContainer object.

        Args:
            identifier (int): The unique identifier for the container.
            weight (float): The weight of the container.
        """
        super().__init__(identifier, weight)

    def consumption(self) -> float:
        """
        Calculate the consumption of the heavy container.

        Returns:
            float: The consumption of the heavy container.
        """
        return self.weight * self.UNIT

class LiquidContainer(HeavyContainer):
    """
    A liquid container with an even higher consumption rate.

    Attributes:
        UNIT (float): The constant consumption rate for liquid containers.
    """

    UNIT = 4.0

    def __init__(self, identifier: int, weight: float) -> None:
        """
        Initialize a LiquidContainer object.

        Args:
            identifier (int): The unique identifier for the container.
            weight (float): The weight of the container.
        """
        super().__init__(identifier, weight)

class RefrigeratedContainer(HeavyContainer):
    """
    A refrigerated container with the highest consumption rate.

    Attributes:
        UNIT (float): The constant consumption rate for refrigerated containers.
    """

    UNIT = 5.0

    def __init__(self, identifier: int, weight: float) -> None:
        """
        Initialize a RefrigeratedContainer object.

        Args:
            identifier (int): The unique identifier for the container.
            weight (float): The weight of the container.
        """
        super().__init__(identifier, weight)