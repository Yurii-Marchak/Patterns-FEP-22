from abc import ABC, abstractmethod
import uuid


class Item(ABC):
    """
    Abstract base class for items in the inventory system.

    Attributes:
        ID (str): Unique identifier for the item.
        weight (float): Weight of a single item.
        count (int): Number of items.
    """
    def __init__(self, weight: float, count: int) -> None:
        self.item_id = str(uuid.uuid4())
        self.weight: float = weight
        self.count: int = count

    def item_data(self):
        """
        Returns a dictionary containing data about the item.

        This method constructs and returns the item's data in the form of a dictionary.
        The dictionary includes the item's unique identifier, type, weight, and count.

        Returns:
            dict: A dictionary with the following keys:
                - "Item ID: ": The unique identifier of the item (UUID).
                - "Item type": The type of the item, represented by the item's class name.
                - "Weight: ": The weight of the item.
                - "Count: ": The quantity or number of the item.
        """
        return {
            "Item ID: ": self.item_id,
            "Item type": self.__class__.__name__,
            "Weight: ": self.weight,
            "Count: ": self.count
        }

    @abstractmethod
    def get_total_weight(self) -> float:
        """Calculates total weight."""

    def __str__(self):
        """
        Provides a string representation of the item.

        Returns:
            str: Description of the item including ID, weight, and count.
        """
        return f"Item type: {self.item_id}, weight: {self.weight}, count: {self.count}"


class Small(Item):
    """
    Class representing a small item.

    Inherits from Item and implements the total weight calculation.
    """

    def get_total_weight(self) -> float:
        """
        Calculates the total weight of the liquid items.

        Returns:
            float: Total weight of the small items.
        """
        return self.count * self.weight


class Heavy(Item):
    """
    Class representing a heavy item.

    Inherits from Item and implements the total weight calculation.
    """
    def get_total_weight(self) -> float:
        """
        Calculates the total weight of the liquid items.

        Returns:
            float: Total weight of the heavy items.
        """
        return self.count * self.weight


class Refrigerated(Item):
    """
    Class representing a refrigerated item.

    Inherits from Item and implements the total weight calculation.
    """

    def get_total_weight(self) -> float:
        """
        Calculates the total weight of the liquid items.

        Returns:
            float: Total weight of the refrigerated items.
        """
        return self.count * self.weight


class Liquid(Item):
    """
    Class representing a liquid item.

    Inherits from Item and implements the total weight calculation.
    """

    def get_total_weight(self) -> float:
        """
        Calculates the total weight of the liquid items.

        Returns:
            float: Total weight of the liquid items.
        """
        return self.count * self.weight


class ItemFactory:
    """
    Factory class to create different types of items.

    It maps item types to their corresponding classes.
    """
    def __init__(self):
        self.factories = {
            "small": Small,
            "heavy": Heavy,
            "refrigerator": Refrigerated,
            "liquid": Liquid
        }

    def create_items(self, item_type: str, weight: float, count: int) -> Item:
        """
        Creates an item of a specified type.

        Args:
            item_type (str): Type of the item to create.
            weight (float): Weight of the item.
            count (int): Number of items to create.

        Returns:
            Item: The created item of the specified type.

        Raises:
            ValueError: If the item type is unknown.
        """
        if item_type in self.factories:
            return self.factories[item_type](weight, count)
        raise ValueError(f"Unknown item type: {item_type}")
