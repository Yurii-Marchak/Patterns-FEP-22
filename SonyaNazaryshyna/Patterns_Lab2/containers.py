from abc import abstractmethod, ABC
from typing import Self
import uuid

class Container(ABC):
    """
    Abstract base class representing a generic container.

    Attributes:
        id (str): A unique identifier for the container.
        weight (float): The weight of the container.

    Methods:
        consumption() -> float:
            Abstract method to calculate the consumption of resources based on the container's weight.
        equals(other_container: Self) -> bool:
            Compares this container with another for equality based on class name and weight.
    """
    
    def __init__(self, weight: float) -> None:
        self.id = str(uuid.uuid4())
        self.weight = weight
        
    @abstractmethod
    def consumption(self) -> float:
        pass
    
    def equals(self, other_container: Self) -> bool:
        if self.__class__.__name__ == other_container.__class__.__name__ and self.weight == other_container.weight:
            return True
        return False
    
class BasicContainer(Container):
    UNIT = 2.5
    
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)
        
    def consumption(self) -> float:
        return self.weight * BasicContainer.UNIT
    
class HeavyContainer(Container):
    UNIT = 3.0
    
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)
        
    def consumption(self) -> float:
        return self.weight * HeavyContainer.UNIT
             
class RefrigeratedContainer(HeavyContainer):
    UNIT = 5.0
    
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)
        
    def consumption(self) -> float:
        return self.weight * RefrigeratedContainer.UNIT
        
class LiquidContainer(HeavyContainer):
    UNIT = 4.0
    
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)
        
    def consumption(self) -> float:
        return self.weight * LiquidContainer.UNIT
        
def create_container(weight: float, container_type: str) -> Container:
    """
    Creates and returns an instance of a Container subclass based on the specified type and weight.

    Args:
        weight (float): The weight of the container. Must be less than or equal to 3000 for 'basic' containers.
        container_type (str): The type of container to create. Valid options are:
            - 'basic'
            - 'refrigerated'
            - 'liquid'
            - 'heavy'

    Returns:
        Container: An instance of the specified Container subclass.

    Raises:
        ValueError: If the container type is invalid or if the weight exceeds the limit for BasicContainer.
    """
    if container_type == 'basic' and weight <= 3000:
        return BasicContainer(weight=weight)
    elif container_type == 'refrigerated':
        return RefrigeratedContainer(weight=weight)
    elif container_type == 'liquid':
        return LiquidContainer(weight=weight)
    elif container_type == 'heavy':
        return HeavyContainer(weight=weight)
    else:
        raise ValueError("Invalid container type or weight exceeds limit for BasicContainer")

    
