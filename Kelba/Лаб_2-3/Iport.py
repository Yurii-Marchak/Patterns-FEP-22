from abc import ABC, abstractmethod

class IPort(ABC):
    @abstractmethod
    def incomingShip(self, ship):
        """Registers an incoming ship to the port."""
        pass

    @abstractmethod
    def outgoingShip(self, ship):
        """Removes a ship from the port when it departs."""
        pass

    @abstractmethod
    def getDistance(self, other_port):
        """Calculates the distance to another port."""
        pass

    @abstractmethod
    def to_dict(self):
        """Returns a dictionary representation of the port."""
        pass