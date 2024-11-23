from abc import ABC, abstractmethod

class IShip(ABC):
    @abstractmethod
    def sailTo(self, port):
        """Sails the ship to the specified port."""
        pass

    @abstractmethod
    def reFuel(self, fuel_amount):
        """Refuels the ship with the specified amount of fuel."""
        pass

    @abstractmethod
    def load(self, container):
        """Loads a container onto the ship."""
        pass

    @abstractmethod
    def unLoad(self, container):
        """Unloads a container from the ship."""
        pass

    @abstractmethod
    def to_dict(self):
        """Returns a dictionary representation of the ship."""
        pass