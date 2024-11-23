from Iport import IPort

class Port(IPort):
    def __init__(self, id: int, latitude: float, longitude: float):
        self.ID = id
        self.latitude = latitude
        self.longitude = longitude
        self.ships = []

    def incomingShip(self, ship):
        self.ships.append(ship)

    def outgoingShip(self, ship):
        self.ships.remove(ship)

    def getDistance(self, other_port):

        return ((self.latitude - other_port.latitude) ** 2 + (self.longitude - other_port.longitude) ** 2) ** 0.5

    def to_dict(self):
        return {"ID": self.ID, "latitude": self.latitude, "longitude": self.longitude, "ships": len(self.ships)}
