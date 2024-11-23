from abc import ABC, abstractmethod
from uuid import uuid4


class Container(ABC):
    def __init__(self, weight: float) -> None:
        self.id = uuid4() 
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        pass

    def __eq__(self, other) -> bool:
        id_check = self.id == other.id
        weight_check = self.weight == other.weight
        type_check = self.__class__ == other.__class__
        return id_check and weight_check and type_check


class BasicContainer(Container):
    def consumption(self) -> float:
        return self.weight * 2.5

class HeavyContainer(Container):
    def consumption(self) -> float:
        return self.weight * 3.0

class RefrigeratedContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 5.0

class LiquidContainer(HeavyContainer):
    def consumption(self) -> float:
        return self.weight * 4.0

class AbstractContainerFactory(ABC):
    @abstractmethod
    def create_container(self, weight: float) -> Container:
        pass

class BasicContainerFactory(AbstractContainerFactory):
    def create_container(self, weight: float) -> BasicContainer:
        return BasicContainer(weight=weight)

class HeavyContainerFactory(AbstractContainerFactory):
    def create_container(self, weight: float) -> HeavyContainer:
        return HeavyContainer(weight=weight)

class RefrigeratedContainerFactory(AbstractContainerFactory):
    def create_container(self, weight: float) -> RefrigeratedContainer:
        return RefrigeratedContainer(weight=weight)

class LiquidContainerFactory(AbstractContainerFactory):
    def create_container(self, weight: float) -> LiquidContainer:
        return LiquidContainer(weight=weight)
