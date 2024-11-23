import json
import math


# Абстрактний клас Container
class Container:
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight

    def consumption(self):
        raise NotImplementedError("Must be implemented by subclasses")

    def __eq__(self, other):
        return isinstance(other, Container) and self.ID == other.ID and self.weight == other.weight and type(self) == type(other)


# Різновиди контейнерів
class BasicContainer(Container):
    def consumption(self):
        return self.weight * 2.5


class HeavyContainer(Container):
    def consumption(self):
        return self.weight * 3.0


class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return self.weight * 5.0


class LiquidContainer(HeavyContainer):
    def consumption(self):
        return self.weight * 4.0


# Клас Port
class Port:
    def __init__(self, ID, latitude, longitude):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = []
        self.history = []
        self.current = []

    def incoming_ship(self, ship):
        if ship not in self.current:
            self.current.append(ship)
        if ship not in self.history:
            self.history.append(ship)

    def outgoing_ship(self, ship):
        if ship in self.current:
            self.current.remove(ship)

    def get_distance(self, other_port):
        lat_diff = math.radians(self.latitude - other_port.latitude)
        lon_diff = math.radians(self.longitude - other_port.longitude)
        a = (math.sin(lat_diff / 2) ** 2 +
             math.cos(math.radians(self.latitude)) *
             math.cos(math.radians(other_port.latitude)) *
             math.sin(lon_diff / 2) ** 2)
        return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))  # 6371 - радіус Землі


# Клас Ship
class Ship:
    def __init__(self, ID, current_port, fuel, total_weight_capacity, max_number_of_all_containers,
                 max_number_of_heavy_containers, max_number_of_refrigerated_containers,
                 max_number_of_liquid_containers, fuel_consumption_per_km):
        self.ID = ID
        self.current_port = current_port
        self.fuel = fuel
        self.total_weight_capacity = total_weight_capacity
        self.max_number_of_all_containers = max_number_of_all_containers
        self.max_number_of_heavy_containers = max_number_of_heavy_containers
        self.max_number_of_refrigerated_containers = max_number_of_refrigerated_containers
        self.max_number_of_liquid_containers = max_number_of_liquid_containers
        self.fuel_consumption_per_km = fuel_consumption_per_km
        self.containers = []
        self.current_port.incoming_ship(self)

    def sail_to(self, destination_port):
        distance = self.current_port.get_distance(destination_port)
        total_consumption = (self.fuel_consumption_per_km * distance +
                             sum(container.consumption() for container in self.containers))
        if self.fuel >= total_consumption:
            self.fuel -= total_consumption
            self.current_port.outgoing_ship(self)
            destination_port.incoming_ship(self)
            self.current_port = destination_port
            return True
        return False

    def refuel(self, amount):
        self.fuel += amount

    def load(self, container):
        current_weight = sum(c.weight for c in self.containers)
        if len(self.containers) < self.max_number_of_all_containers and \
                current_weight + container.weight <= self.total_weight_capacity:
            if isinstance(container, HeavyContainer):
                if sum(1 for c in self.containers if isinstance(c, HeavyContainer)) >= self.max_number_of_heavy_containers:
                    return False
                if isinstance(container, RefrigeratedContainer) and \
                        sum(1 for c in self.containers if isinstance(c, RefrigeratedContainer)) >= self.max_number_of_refrigerated_containers:
                    return False
                if isinstance(container, LiquidContainer) and \
                        sum(1 for c in self.containers if isinstance(c, LiquidContainer)) >= self.max_number_of_liquid_containers:
                    return False
            self.containers.append(container)
            return True
        return False

    def unload(self, container):
        if container in self.containers:
            self.containers.remove(container)
            self.current_port.containers.append(container)
            return True
        return False


# Головна програма
def main():
    # Читання вхідного JSON
    with open("input.json", "r") as f:
        data = json.load(f)

    ports = []
    ships = []
    containers = []

    # Створення портів
    for port_data in data["ports"]:
        ports.append(Port(port_data["id"], port_data["latitude"], port_data["longitude"]))

    # Створення контейнерів
    for container_data in data["containers"]:
        id = container_data["id"]
        weight = container_data["weight"]
        type_ = container_data["type"]
        if type_ == "Basic":
            containers.append(BasicContainer(id, weight))
        elif type_ == "Refrigerated":
            containers.append(RefrigeratedContainer(id, weight))
        elif type_ == "Liquid":
            containers.append(LiquidContainer(id, weight))
        else:
            containers.append(HeavyContainer(id, weight))

    # Створення кораблів
    for ship_data in data["ships"]:
        ships.append(Ship(
            ship_data["id"],
            ports[ship_data["currentPort"]],
            ship_data["fuel"],
            ship_data["totalWeightCapacity"],
            ship_data["maxNumberOfAllContainers"],
            ship_data["maxNumberOfHeavyContainers"],
            ship_data["maxNumberOfRefrigeratedContainers"],
            ship_data["maxNumberOfLiquidContainers"],
            ship_data["fuelConsumptionPerKM"]
        ))

    # Виконання дій
    for action in data["actions"]:
        if action["action"] == "load":
            ship = ships[action["shipId"]]
            container = containers[action["containerId"]]
            result = ship.load(container)
            print(f"Ship {ship.ID} loading container {container.ID}: {'Success' if result else 'Failed'}")
        elif action["action"] == "unload":
            ship = ships[action["shipId"]]
            container = containers[action["containerId"]]
            result = ship.unload(container)
            print(f"Ship {ship.ID} unloading container {container.ID}: {'Success' if result else 'Failed'}")
        elif action["action"] == "sail":
            ship = ships[action["shipId"]]
            port = ports[action["portId"]]
            result = ship.sail_to(port)
            print(f"Ship {ship.ID} sailing to port {port.ID}: {'Success' if result else 'Failed'}")
        elif action["action"] == "refuel":
            ship = ships[action["shipId"]]
            ship.refuel(action["fuel"])
            print(f"Ship {ship.ID} refueled: {ship.fuel} fuel remaining")


    for ship in ships:
        print(f"Ship {ship.ID} status:")
        print(f"  Fuel: {ship.fuel}")
        print(f"  Current Port: {ship.current_port.ID}")
        print(f"  Containers: {', '.join(str(container.ID) for container in ship.containers)}")
        print()


if __name__ == "__main__":
    main()
