import json
import math
from abc import ABC, abstractmethod

# -------------------- Interfaces
class IPort(ABC):
    @abstractmethod
    def incomingShip(self, ship):
        pass

    @abstractmethod
    def outgoingShip(self, ship):
        pass

class IShip(ABC):
    @abstractmethod
    def sailTo(self, port):
        pass

    @abstractmethod
    def reFuel(self, fuel):
        pass

    @abstractmethod
    def load(self, container):
        pass

    @abstractmethod
    def unLoad(self, container):
        pass

# -----Container Classes
class Container(ABC):
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight
    
    @abstractmethod
    def consumption(self):
        pass

    def __eq__(self, other):
        return isinstance(other, Container) and self.ID == other.ID and self.weight == other.weight

class BasicContainer(Container):
    def consumption(self):
        return 2.5 * self.weight

class HeavyContainer(Container):
    def consumption(self):
        return 3.0 * self.weight

class RefrigeratedContainer(HeavyContainer):
    def consumption(self):
        return 5.0 * self.weight

class LiquidContainer(HeavyContainer):
    def consumption(self):
        return 4.0 * self.weight

# --------------------Ship Class
class Ship(IShip):
    def __init__(self, ID, currentPort, totalWeightCapacity, maxAllContainers, maxHeavyContainers,
                 maxRefrigeratedContainers, maxLiquidContainers, fuelConsumptionPerKM):
        self.ID = ID
        self.fuel = 0
        self.currentPort = currentPort
        self.totalWeightCapacity = totalWeightCapacity
        self.maxAllContainers = maxAllContainers
        self.maxHeavyContainers = maxHeavyContainers
        self.maxRefrigeratedContainers = maxRefrigeratedContainers
        self.maxLiquidContainers = maxLiquidContainers
        self.fuelConsumptionPerKM = fuelConsumptionPerKM
        self.containers = []

    def sailTo(self, port):
        distance = self.currentPort.getDistance(port)
        required_fuel = self.fuelConsumptionPerKM * distance + sum(c.consumption() * distance for c in self.containers)
        if self.fuel >= required_fuel:
            self.fuel -= required_fuel
            self.currentPort.outgoingShip(self)
            port.incomingShip(self)
            self.currentPort = port
            return True
        return False

    def reFuel(self, fuel):
        self.fuel += fuel

    def load(self, container):
        if len(self.containers) < self.maxAllContainers and sum(c.weight for c in self.containers) + container.weight <= self.totalWeightCapacity:
            self.containers.append(container)
            return True
        return False

    def unLoad(self, container):
        if container in self.containers:
            self.containers.remove(container)
            return True
        return False

    def getCurrentContainers(self):
        return sorted(self.containers, key=lambda c: c.ID)

# ---------------------------- Port Class
class Port(IPort):
    def __init__(self, ID, latitude, longitude, containers=None):
        self.ID = ID
        self.latitude = latitude
        self.longitude = longitude
        self.containers = containers if containers else []
        self.history = []
        self.current = []


    def incomingShip(self, ship):
        if ship not in self.current:
            self.current.append(ship)

    def outgoingShip(self, ship):
        if ship in self.current:
            self.current.remove(ship)
        if ship not in self.history:
            self.history.append(ship)

    def getDistance(self, otherPort):
        # Calculate distance using the Haversine formula for geospatial distance
        R = 6371  # Radius of the earth in kilometers
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(otherPort.latitude), math.radians(otherPort.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

# -------------------- Main Class
class Main:
    def __init__(self, input_file, output_file):
        self.ports = []
        self.ships = []
        self.containers = []
        self.actions = []
        self.input_file = input_file
        self.output_file = output_file

    def readInput(self):
        with open(self.input_file, 'r') as file:
            data = json.load(file)
            self.processData(data)

    def processData(self, data):
        # Process ports, ships, and containers from the input JSON
        for port_data in data.get('ports', []):
            port = Port(port_data['ID'], port_data['latitude'], port_data['longitude'])
            self.ports.append(port)
        
        for ship_data in data.get('ships', []):
            port = next(p for p in self.ports if p.ID == ship_data['portID'])
            ship = Ship(ship_data['ID'], port, ship_data['totalWeightCapacity'], ship_data['maxAllContainers'],
                        ship_data['maxHeavyContainers'], ship_data['maxRefrigeratedContainers'],
                        ship_data['maxLiquidContainers'], ship_data['fuelConsumptionPerKM'])
            self.ships.append(ship)
            port.incomingShip(ship)
        
        for container_data in data.get('containers', []):
            container = self.createContainer(container_data)
            self.containers.append(container)
            port = self.ports[0]  # Умовно додаємо контейнери в перший порт
            port.containers.append(container)

        self.actions = data.get('actions', [])
    
    def createContainer(self, container_data):
        if container_data['type'] == 'Basic':
            return BasicContainer(container_data['ID'], container_data['weight'])
        elif container_data['type'] == 'Heavy':
            return HeavyContainer(container_data['ID'], container_data['weight'])
        elif container_data['type'] == 'Refrigerated':
            return RefrigeratedContainer(container_data['ID'], container_data['weight'])
        elif container_data['type'] == 'Liquid':
            return LiquidContainer(container_data['ID'], container_data['weight'])

    def executeActions(self):
        for action in self.actions:
            ship = next(s for s in self.ships if s.ID == action['shipID'])
            
            # Завантаження контейнера на корабель
            if action['action'] == 'load_container':
                container = next(c for c in self.containers if c.ID == action['containerID'])
                port = ship.currentPort
                if container in port.containers:
                    if ship.load(container):
                        port.containers.remove(container)
                        print(f"Контейнер {container.ID} завантажено на корабель {ship.ID}.")
                    else:
                        print(f"Контейнер {container.ID} не може бути завантажений на корабель {ship.ID} через обмеження.")
                else:
                    print(f"Контейнер {container.ID} не знайдено в порту {port.ID}")
                        
            # Розвантаження контейнера з корабля
            elif action['action'] == 'unload_container':
                container = next((c for c in ship.getCurrentContainers() if c.ID == action['containerID']), None)
                if container is not None:
                    port = ship.currentPort
                    if ship.unLoad(container):
                        port.containers.append(container)
                        print(f"Контейнер {container.ID} розвантажено в порту {port.ID}.")
                else:
                    print(f"Контейнер {action['containerID']} не знайдено на кораблі {ship.ID}")
            
            # Заправка корабля
            elif action['action'] == 'refuel':
                ship.reFuel(action['fuelAmount'])
                print(f"Корабель {ship.ID} заправлено на {action['fuelAmount']} одиниць палива.")
            
            # Переміщення корабля в інший порт
            elif action['action'] == 'sail':
                destination_port = next(p for p in self.ports if p.ID == action['destinationPortID'])
                distance = ship.currentPort.getDistance(destination_port)
                required_fuel = ship.fuelConsumptionPerKM * distance
                if ship.fuel >= required_fuel:
                    if ship.sailTo(destination_port):
                        print(f"Корабель {ship.ID} успішно прибув до порту {destination_port.ID}.")
                    else:
                        print(f"Не вдалося переміститися до порту {destination_port.ID}.")
                else:
                    print(f"Недостатньо палива для переміщення корабля {ship.ID} до порту {destination_port.ID}.")
                    # Якщо корабель не має достатньо пального, ви можете запланувати заповнення
                    # або зробити це автоматично, як ви хотіли раніше.

    def writeOutput(self):
        output_data = {}
        for port in sorted(self.ports, key=lambda p: p.ID):
            port_info = {
                'lat': round(port.latitude, 2),
                'lon': round(port.longitude, 2),
                'basic_container': [c.ID for c in port.containers if isinstance(c, BasicContainer)],
                'heavy_container': [c.ID for c in port.containers if isinstance(c, HeavyContainer)],
                'refrigerated_container': [c.ID for c in port.containers if isinstance(c, RefrigeratedContainer)],
                'liquid_container': [c.ID for c in port.containers if isinstance(c, LiquidContainer)],
                'ships': {
                    ship.ID: {
                        'fuel_left': round(ship.fuel, 2),
                        'basic_container': [c.ID for c in ship.getCurrentContainers() if isinstance(c, BasicContainer)],
                        'heavy_container': [c.ID for c in ship.getCurrentContainers() if isinstance(c, HeavyContainer)],
                        'refrigerated_container': [c.ID for c in ship.getCurrentContainers() if isinstance(c, RefrigeratedContainer)],
                        'liquid_container': [c.ID for c in ship.getCurrentContainers() if isinstance(c, LiquidContainer)]
                    } for ship in port.current
                }
            }
            output_data[f'Port {port.ID}'] = port_info

        with open(self.output_file, 'w') as file:
            json.dump(output_data, file, indent=4)

    def run(self):
        self.readInput()
        self.executeActions()  # Виконуємо всі дії
        self.writeOutput()

# -------------------- Execution
if __name__ == "__main__":
    # You can replace 'input.json' and 'output.json' with your actual file paths.
    simulation = Main('input.json', 'output.json')
    simulation.run()
