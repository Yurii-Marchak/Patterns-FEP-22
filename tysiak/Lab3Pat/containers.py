from abc import ABC, abstractmethod
import json

class Container(ABC):
    def __init__(self, id: int, weight: float):
        self.id = id
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        pass

    def to_json(self):
        return {
            "id": self.id,
            "weight": self.weight,
            "type": self.__class__.__name__
        }

    @classmethod
    def from_json(cls, data):
        container_type = data["type"]
        if container_type == "BasicContainer":
            return BasicContainer(data["id"], data["weight"])
        elif container_type == "HeavyContainer":
            return HeavyContainer(data["id"], data["weight"])
        elif container_type == "RefrigeratedContainer":
            return RefrigeratedContainer(data["id"], data["weight"])
        elif container_type == "LiquidContainer":
            return LiquidContainer(data["id"], data["weight"])

class BasicContainer(Container):
    UNIT = 2.5

    def consumption(self) -> float:
        return self.weight * self.UNIT

class HeavyContainer(Container):
    UNIT = 3.0

    def consumption(self) -> float:
        return self.weight * self.UNIT

class RefrigeratedContainer(Container):
    UNIT = 5.0

    def consumption(self) -> float:
        return self.weight * self.UNIT

class LiquidContainer(Container):
    UNIT = 4.0

    def consumption(self) -> float:
        return self.weight * self.UNIT

def create_container(id: int, weight: float, container_type: str = '') -> Container:
    if container_type == 'R':
        return RefrigeratedContainer(id=id, weight=weight)
    elif container_type == 'L':
        return LiquidContainer(id=id, weight=weight)
    elif weight <= 3000:
        return BasicContainer(id=id, weight=weight)
    else:
        return HeavyContainer(id=id, weight=weight)