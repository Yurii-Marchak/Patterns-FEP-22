from abc import abstractmethod, ABC
from typing import Self, List
import uuid
from item import Item
from port import Port

class Container(ABC):
    """
    Abstract base class representing a generic container.

    Attributes:
        id (str): A unique identifier for the container.
        weight (float): The weight of the container.
        items_in_the_container (List[Item]): A list of items stored in the container.
        max_item (int): Maximum number of items the container can hold.
    """

    def __init__(self, weight: float, max_item: int) -> None:
        self.container_id = str(uuid.uuid4())
        self.weight = weight
        self.items_in_the_container: List[Item] = []
        self.max_item = max_item

    def container_data(self):
        """
        Returns a dictionary containing data about the container.

        This method constructs and returns the container data in the form of a dictionary. 
        The dictionary includes the container's unique identifier, its type, and a list of 
        items currently stored inside the container.

        Returns:
            dict: A dictionary with the following keys:
                - "Container ID": The unique identifier of the container (UUID).
                - "Container type": The type of the container, 
                represented by the container's class name.
                - "Items in the container": A list of dictionaries, 
                each representing an item stored in the container.
        """
        return {
            "Container ID": self.container_id,
            "Container type": self.__class__.__name__,
            "Items in the container": [item.item_data() for item in self.items_in_the_container]
        }


    def load_item(self, item: 'Item') -> None:
        """
        Loads an item into the container if there is space.

        Args:
            item (Item): The item to be loaded into the container.
        """
        if len(self.items_in_the_container) < self.max_item and item not in self.items_in_the_container:
            self.items_in_the_container.append(item)
            return True
        return False

    def unload_item(self, item: 'Item', port: 'Port') -> bool:
        """
        Unloads an item from the container to the specified port.

        Args:
            item (Item): The item to be unloaded.
            port (Port): The port where the item will be unloaded.

        Returns:
            bool: True if the item was successfully unloaded, False otherwise.
        """
        if item in self.items_in_the_container:
            if item not in port.items:
                port.items.append(item)
                self.items_in_the_container.remove(item)
            return True
        return False

    @abstractmethod
    def consumption(self) -> float:
        """
        Calculates the consumption of resources based on the container's weight.

        Returns:
            float: The calculated consumption value.
        """

    def equals(self, other_container: Self) -> bool:
        """
        Compares this container with another for equality.

        Args:
            other_container (Self): Another container instance to compare with.

        Returns:
            bool: True if both containers have the same class name and weight, 
            False otherwise.
        """
        return (
            self.__class__.__name__ == other_container.__class__.__name__
            and self.weight == other_container.weight
        )


class BasicContainer(Container):
    """
    Represents a basic container with standard resource consumption.

    Inherits from Container.

    Attributes:
        UNIT (float): Resource consumption factor for basic containers.
    """
    UNIT = 2.5

    def consumption(self) -> float:
        return self.weight * BasicContainer.UNIT


class HeavyContainer(Container):
    """
    Represents a heavy container with increased resource consumption.

    Inherits from Container.

    Attributes:
        UNIT (float): Resource consumption factor for heavy containers.
    """
    UNIT = 3.0

    def consumption(self) -> float:
        return self.weight * HeavyContainer.UNIT


class RefrigeratedContainer(HeavyContainer):
    """
    Represents a refrigerated heavy container with specific resource consumption.

    Inherits from HeavyContainer.

    Attributes:
        UNIT (float): Resource consumption factor for refrigerated containers.
    """
    UNIT = 5.0

    def consumption(self) -> float:
        return self.weight * RefrigeratedContainer.UNIT


class LiquidContainer(HeavyContainer):
    """
    Represents a liquid heavy container with specific resource consumption.

    Inherits from HeavyContainer.

    Attributes:
        UNIT (float): Resource consumption factor for liquid containers.
    """
    UNIT = 4.0

    def consumption(self) -> float:
        return self.weight * LiquidContainer.UNIT


def create_container(weight: float, max_item: int, container_type: str) -> Container:
    """
    Creates and returns an instance of a Container subclass based on the specified type and weight.

    Args:
        weight (float): The weight of the container.
        max_item (int): Maximum number of items the container can hold.
        items (List[Item]): The list of items initially in the container.
        container_type (str): The type of container to create. Valid options are:
            - 'basic'
            - 'refrigerated'
            - 'liquid'
            - 'heavy'

    Returns:
        Container: An instance of the specified Container subclass.

    Raises:
        ValueError: If the container type is invalid.
    """
    if container_type == 'basic' and weight <= 3000:
        return BasicContainer(weight, max_item)
    elif container_type == 'refrigerated':
        return RefrigeratedContainer(weight, max_item)
    elif container_type == 'liquid':
        return LiquidContainer(weight, max_item)
    elif container_type == 'heavy':
        return HeavyContainer(weight, max_item)
    else:
        raise ValueError("Invalid container type or weight exceeds limit for BasicContainer")
