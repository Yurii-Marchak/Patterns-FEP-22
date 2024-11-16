from abc import abstractmethod, ABC
from typing import List

class Item(ABC):
    def __init__(self, id: int, weight: float, count: int) -> None:
        self.id: int = id
        self.weight: float = weight
        self.count: int = count 
        
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "weight": self.weight,
            "count": self.count
        }
        
    @abstractmethod
    def get_total_weight(self) -> float:
        pass
        
class SmallItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count
    
class HeavyItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count

class RefrigeratedItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count
    
class LiquidItem(Item):
    def get_total_weight(self) -> float:
        return self.weight * self.count
    
class ItemFactory:
    @staticmethod
    def create_item(item_type: str, id: int, weight: float, count: int) -> Item:
        if item_type == 'small':
            return SmallItem(id, weight, count)
        elif item_type == 'heavy':
            return HeavyItem(id, weight, count)
        elif item_type == 'refrigerated':
            return RefrigeratedItem(id, weight, count)
        elif item_type == 'liquid':
            return LiquidItem(id, weight, count)

class Container(ABC): 
    _id_container = 0
    
    def __init__(self, max_weight: float, max_items: int) -> None:
        Container._id_container += 1
        self.id: int = Container._id_container
        self.max_weight = max_weight 
        self.max_items = max_items 
        self.items: List[Item] = []
        self.weight: float = 0.0
        
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "max_weight": self.max_weight,
            "max_items": self.max_items,
            "items": [item.to_dict() for item in self.items]
        }
        
    def add_item(self, item: 'Item') -> None:
        total_weight = self.get_current_weight() + item.get_total_weight()
        if len(self.items) < self.max_items and total_weight <= self.max_weight:
            self.items.append(item)
            item.containerId = self.id
        else:
            raise ValueError("Exceeded container capacity or weight limit")
              
    def get_current_weight(self) -> float:
        return sum(item.get_total_weight() for item in self.items)
        
    def __repr__(self) -> str:
        return f"Container(id={self.id}, container_type={self.__class__.__name__})"
        
    def load_items(self, item: 'Item') -> bool:
        if len(items) < max_items:
            items.append(item)
            return True
        return False
    
    @abstractmethod
    def consumption(self) -> float:
        """
        Calculates fuel consumption. 
        Must be implemented by subclasses.
        """
        pass
    
class BasicContainer(Container):
    UNIT = 2.5
        
    def __init__(self, max_weight: float, max_items: int) -> None:
        super().__init__(max_weight, max_items)
            
    def consumption(self) -> float:
        return self.get_current_weight() * self.UNIT
        
class HeavyContainer(Container):
    UNIT = 3.0
    
    def __init__(self, max_weight: float, max_items: int) -> None:
        super().__init__(max_weight, max_items)
        
    def consumption(self) -> float:
        return self.get_current_weight() * self.UNIT  
    
class RefrigeratedContainer(HeavyContainer):
    UNIT = 5.0
    
    def __init__(self, max_weight: float, max_items: int) -> None:
        super().__init__(max_weight, max_items)
        
    def consumption(self) -> float:
        return self.get_current_weight() * self.UNIT  
    
class LiquidContainer(HeavyContainer):
    UNIT = 4.0
    
    def __init__(self, max_weight: float, max_items: int) -> None:
        super().__init__(max_weight, max_items)
        
    def consumption(self) -> float:
        return self.get_current_weight() * self.UNIT  
    
def create_container(max_weight: float, max_items: int, container_type: str) -> Container:
    """
    Creates a container of the specified type and weight.
    
    Types include: 'basic', 'heavy', 'refrigerated', 'liquid'.
    Raises an error if the type or weight is invalid.
    """
    if container_type == 'basic':
        return BasicContainer(max_weight=max_weight, max_items=max_items)
    elif container_type == 'heavy':
        return HeavyContainer(max_weight=max_weight, max_items=max_items)  
    elif container_type == "refrigerated":
        return RefrigeratedContainer(max_weight=max_weight, max_items=max_items)
    elif container_type == "liquid":
        return LiquidContainer(max_weight=max_weight, max_items=max_items)
    else:
        raise ValueError("Unknown type of container")


# factory = ItemFactory()
# item1 = factory.create_item('small', 1, 4, 2)
# cont = create_container(1000, 10, 'basic')
# cont.add_item(item1)
# print(cont.items)