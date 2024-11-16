from abc import abstractmethod, ABC
from typing import Self, Any, Tuple, List, Type



class Container(ABC): 
    _id_container = 0
    
    def __init__(self, weight: float, id: int) -> None:
        Container._id_container += 1
        self.id: int = Container._id_container
        self.weight = weight 
        
    @abstractmethod
    def consumption(self) -> float:
        pass
    
    def equals(self, other_container: Self) -> bool:
        other_container.__class__.__name__
        if self.__class__.__name__ == other.container.__class__.__name__ and self.weight == other_container.weight:
            return True
        return False 
        
class BasicContainer(Container):
    UNIT = 2.5
        
    def __init__(self, weight: float, id: int) -> None:
        super().__init__(weight, id)
            
    def consumption(self) -> float:
        return self.weight * self.UNIT
        
class HeavyContainer(Container):
    UNIT = 3.0
    
    def __init__(self, weight: float, id: int) -> None:
        super().__init__(weight, id)
        
    def consumption(self) -> float:
        return self.weight * self.UNIT  
    
    
class RefrigeratedContainer(HeavyContainer):
    UNIT = 5.0
    
    def __init__(self, weight: float, id: int) -> None:
        super().__init__(weight, id)
        
    def consumption(self) -> float:
        return self.weight * self.UNIT  
    
     
class LiquidContainer(HeavyContainer):
    UNIT = 4.0
    
    def __init__(self, weight: float, id: int) -> None:
        super().__init__(weight, id)
        
    def consumption(self) -> float:
        return self.weight * self.UNIT  


    
        
# def create_container(weight: float) -> Container:
#     if weight <= 3000:
#         return BasicContainer(weight=weight, id=1)
#     else:
#         return HeavyContainer(weight=weight, id=1)          
        
     
def create_container(weight: float, container_type: str ) -> Container:
    if container_type == 'basic' and weight <= 3000:
        return BasicContainer(weight=weight, id=Container._id_container)
    elif container_type == 'heavy' and weight > 3000:
        return HeavyContainer(weight=weight, id=Container._id_container)  
    elif container_type == "refrigerated":
        return RefrigeratedContainer(weight=weight, id=Container._id_container)
    elif container_type == "liquid":
        return LiquidContainer(weight=weight, id=Container._id_container)
    else:
        raise ValueError("Невідомий тип контейнера або вага не відповідає вимогам для заданого типу.")
     
        
        
     
     
        
        
    