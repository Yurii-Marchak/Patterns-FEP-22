from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from container import Container


class Item(ABC):
    """Abstract base class representing a generic item."""

    def __init__(self, identifier: int, weight: float, count: int):
        """
        Initializes an item with the given parameters.

        :param identifier: Unique ID of the item.
        :param weight: Weight of a single item.
        :param count: Number of items.
        """
        self.ID = identifier
        self.weight = weight
        self.count = count
        self.container_id = -1
        self.type = type

    @abstractmethod
    def get_total_weight(self) -> float:
        """
        Calculates the total weight of the items.

        :return: Total weight of the items.
        """
        pass

    @abstractmethod
    def get_item_details(self) -> str:
        """
        Provides details about the item.

        :return: String representation of the item details.
        """
        pass

    def set_container(self, cont: 'Container'):
        """Associates the item with a specific container.

        :param cont: The container to associate with the item.
        """
        self.container_id = cont.id


class Small(Item):
    """Class representing a small item."""

    def __init__(self, identifier: int, weight: float, count: int, description: str):
        """
        Initializes a small item.

        :param identifier: Unique ID of the item.
        :param weight: Weight of a single item.
        :param count: Number of items.
        :param description: Description of the small item.
        """
        super().__init__(identifier, weight, count)
        self.description = description

    def get_total_weight(self) -> float:
        """Calculates the total weight of the small items.

        :return: Total weight of the small items.
        """
        return self.weight * self.count

    def get_item_details(self) -> str:
        """Provides details about the small item.

        :return: String representation of the small item details.
        """
        return f"Small Item: {self.description}, Total Weight: {self.get_total_weight()}"


class Heavy(Item):
    """Class representing a heavy item."""

    def __init__(self, identifier: int, weight: float, count: int, max_load: int):
        """
        Initializes a heavy item.

        :param identifier: Unique ID of the item.
        :param weight: Weight of a single item.
        :param count: Number of items.
        :param max_load: Maximum load capacity of the heavy item.
        """
        super().__init__(identifier, weight, count)
        self.max_load = max_load

    def get_total_weight(self) -> float:
        """Calculates the total weight of the heavy items.

        :return: Total weight of the heavy items.
        """
        return self.weight * self.count

    def get_item_details(self) -> str:
        """Provides details about the heavy item.

        :return: String representation of the heavy item details.
        """
        return f"Heavy Item, Max Load: {self.max_load}, Total Weight: {self.get_total_weight()}"


class Refrigerated(Item):
    """Class representing a refrigerated item."""

    def __init__(self, identifier: int, weight: float, count: int, temperature: float):
        """
        Initializes a refrigerated item.

        :param identifier: Unique ID of the item.
        :param weight: Weight of a single item.
        :param count: Number of items.
        :param temperature: Temperature for the refrigerated item.
        """
        super().__init__(identifier, weight, count)
        self.temperature = temperature

    def get_total_weight(self) -> float:
        """Calculates the total weight of the refrigerated items.

        :return: Total weight of the refrigerated items.
        """
        return self.weight * self.count

    def get_item_details(self) -> str:
        """Provides details about the refrigerated item.

        :return: String representation of the refrigerated item details.
        """
        return f"Refrigerated Item, Temperature: {self.temperature}°C, Total Weight: {self.get_total_weight()}"


class Liquid(Item):
    """Class representing a liquid item."""

    def __init__(self, identifier: int, weight: float, count: int, liquid_type: str):
        """
        Initializes a liquid item.

        :param identifier: Unique ID of the item.
        :param weight: Weight of a single item.
        :param count: Number of items.
        :param liquid_type: Type of the liquid.
        """
        super().__init__(identifier, weight, count)
        self.liquid_type = liquid_type

    def get_total_weight(self) -> float:
        """Calculates the total weight of the liquid items.

        :return: Total weight of the liquid items.
        """
        return self.weight * self.count

    def get_item_details(self) -> str:
        """Provides details about the liquid item.

        :return: String representation of the liquid item details.
        """
        return f"Liquid Item: {self.liquid_type}, Total Weight: {self.get_total_weight()}"


class ItemFactory:
    """Factory class for creating items of various types."""

    @staticmethod
    def create_item(item_type: str, identifier: int, weight: float, count: int, *args) -> Item:
        """
        Creates an item based on the specified type.

        :param item_type: The type of item to create ('small', 'heavy', 'refrigerated', 'liquid').
        :param identifier: Unique ID of the item.
        :param weight: Weight of a single item.
        :param count: Number of items.
        :param args: Additional parameters specific to the item type.

        :return: An instance of the created item.

        :raises ValueError: If an unknown item type is provided.
        """
        if item_type.lower() == "small":
            return Small(identifier, weight, count, args[0])
        elif item_type.lower() == "heavy":
            return Heavy(identifier, weight, count, args[0])
        elif item_type.lower() == "refrigerated":
            return Refrigerated(identifier, weight, count, args[0])
        elif item_type.lower() == "liquid":
            return Liquid(identifier, weight, count, args[0])
        else:
            raise ValueError(f"Unknown item type: {item_type}")
