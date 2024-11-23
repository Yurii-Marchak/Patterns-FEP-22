from abc import ABC, abstractmethod

class Container(ABC):
    def __init__(self, id: int, capacity: float):
        self.ID = id
        self.capacity = capacity
        self.items = []

    @abstractmethod
    def to_dict(self):
        """Returns a dictionary representation of the container."""
        pass

    @abstractmethod
    def canLoad(self, item: 'Item') -> bool:
        """Check if the container can load the given item."""
        pass

    def getTotalWeight(self):
        """Calculate the total weight of all items in the container."""
        return sum(item.getTotalWeight() for item in self.items)

    def loadItem(self, item: 'Item'):
        """Load an item into the container if compatible."""
        if self.canLoad(item):
            self.items.append(item)
            return True
        return False

class BasicContainer(Container):
    def to_dict(self):
        return {"type": "BasicContainer", "ID": self.ID, "capacity": self.capacity}

    def canLoad(self, item: 'Item') -> bool:
        return (self.getTotalWeight() + item.getTotalWeight() <= self.capacity)

class RefrigeratedContainer(Container):
    def to_dict(self):
        return {"type": "RefrigeratedContainer", "ID": self.ID, "capacity": self.capacity}

    def canLoad(self, item: 'Item') -> bool:
        return (self.getTotalWeight() + item.getTotalWeight() <= self.capacity)

class LiquidContainer(Container):
    def to_dict(self):
        return {"type": "LiquidContainer", "ID": self.ID, "capacity": self.capacity}

    def canLoad(self, item: 'Item') -> bool:
        return (self.getTotalWeight() + item.getTotalWeight() <= self.capacity)