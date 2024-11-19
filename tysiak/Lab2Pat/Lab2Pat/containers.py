from abc import ABC, abstractmethod

class Container(ABC):
    """
    Abstract base class representing a generic container.

    Attributes:
    -----------
    id : int
        Unique identifier for the container.
    weight : float
        The weight of the container.

    Methods:
    --------
    consumption() -> float:
        Abstract method to calculate the fuel consumption based on the container's weight.

    equals(other_container: Container) -> bool:
        Compares two containers for equality based on their class and weight.
    """
    def __init__(self, id: int, weight: float) -> None:
        """
        Initializes a container with a unique id and weight.

        Parameters:
        -----------
        id : int
            The unique identifier of the container.
        weight : float
            The weight of the container.
        """
        self.id = id
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        """
        Abstract method to calculate the fuel consumption for the container.
        Each subclass should implement its own consumption calculation.
        """
        pass

    def equals(self, other_container: 'Container') -> bool:
        """
        Compares two containers for equality based on their class and weight.

        Parameters:
        -----------
        other_container : Container
            The container to compare against.

        Returns:
        --------
        bool
            True if the containers are of the same type and have the same weight, False otherwise.
        """
        return isinstance(other_container, self.__class__) and self.weight == other_container.weight


class BasicContainer(Container):
    """
    Represents a basic container with a unit consumption multiplier.

    Attributes:
    -----------
    UNIT : float
        The fuel consumption multiplier for a basic container.
    """
    UNIT = 2.5

    def __init__(self, id: int, weight: float) -> None:
        """
        Initializes a basic container with a unique id and weight.

        Parameters:
        -----------
        id : int
            The unique identifier of the container.
        weight : float
            The weight of the container.
        """
        super().__init__(id, weight)

    def consumption(self) -> float:
        """
        Calculates the fuel consumption for a basic container.

        Returns:
        --------
        float
            The fuel consumption based on the weight and the basic unit multiplier.
        """
        return self.weight * self.UNIT


class HeavyContainer(Container):
    """
    Represents a heavy container with a unit consumption multiplier.

    Attributes:
    -----------
    UNIT : float
        The fuel consumption multiplier for a heavy container.
    """
    UNIT = 3.0

    def __init__(self, id: int, weight: float) -> None:
        """
        Initializes a heavy container with a unique id and weight.

        Parameters:
        -----------
        id : int
            The unique identifier of the container.
        weight : float
            The weight of the container.
        """
        super().__init__(id, weight)

    def consumption(self) -> float:
        """
        Calculates the fuel consumption for a heavy container.

        Returns:
        --------
        float
            The fuel consumption based on the weight and the heavy unit multiplier.
        """
        return self.weight * self.UNIT


class RefrigeratedContainer(HeavyContainer):
    """
    Represents a refrigerated container, inheriting from HeavyContainer.

    Attributes:
    -----------
    UNIT : float
        The fuel consumption multiplier for a refrigerated container.
    """
    UNIT = 5.0

    def __init__(self, id: int, weight: float) -> None:
        """
        Initializes a refrigerated container with a unique id and weight.

        Parameters:
        -----------
        id : int
            The unique identifier of the container.
        weight : float
            The weight of the container.
        """
        super().__init__(id, weight)


class LiquidContainer(HeavyContainer):
    """
    Represents a liquid container, inheriting from HeavyContainer.

    Attributes:
    -----------
    UNIT : float
        The fuel consumption multiplier for a liquid container.
    """
    UNIT = 4.0

    def __init__(self, id: int, weight: float) -> None:
        """
        Initializes a liquid container with a unique id and weight.

        Parameters:
        -----------
        id : int
            The unique identifier of the container.
        weight : float
            The weight of the container.
        """
        super().__init__(id, weight)


def create_container(id: int, weight: float, container_type: str = '') -> Container:
    """
    Factory function to create a container based on the provided weight and type.

    Parameters:
    -----------
    id : int
        The unique identifier of the container.
    weight : float
        The weight of the container.
    container_type : str, optional
        The type of container to create ('R' for Refrigerated, 'L' for Liquid, '' for basic or heavy based on weight).

    Returns:
    --------
    Container
        A container object of the appropriate type based on the given parameters.
    """
    if container_type == 'R':
        return RefrigeratedContainer(id=id, weight=weight)
    elif container_type == 'L':
        return LiquidContainer(id=id, weight=weight)
    elif weight <= 3000:
        return BasicContainer(id=id, weight=weight)
    else:
        return HeavyContainer(id=id, weight=weight)
