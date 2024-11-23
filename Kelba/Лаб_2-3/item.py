from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, id: int, weight: float, count: int, container_id: int):
        self.ID = id
        self.weight = weight
        self.count = count
        self.containerID = container_id

    @abstractmethod
    def getTotalWeight(self):
        """Calculate the total weight of the item."""
        pass

class Small(Item):
    def getTotalWeight(self):
        return self.weight * self.count

class Heavy(Item):
    def getTotalWeight(self):
        return self.weight * self.count * 1.5

class Refrigerated(Item):
    def getTotalWeight(self):
        return self.weight * self.count * 1.2

class Liquid(Item):
    def getTotalWeight(self):
        return self.weight * self.count * 1.1
