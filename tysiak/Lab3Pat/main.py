import json
from port import Port
from containers import create_container
from ship import ShipFactory

def save_to_json(ports, ships, filename):
    data = {
        "ports": [port.to_json() for port in ports.values()],
        "ships": [ship.to_json() for ship in ships.values()]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    ports = {p['id']: Port.from_json(p) for p in data['ports']}
    ships = {s['id']: ShipFactory.from_json(s, ports) for s in data['ships']}
    
    return ports, ships

def main():
    # Створення портів
    ports = {
        1: Port(1, (46.48, 30.73)),  # Одеса
        2: Port(2, (38.37, 21.24)),  # Агрініо
        3: Port(3, (38.91, 16.35))   # Катандзаро
    }

    # Створення кораблів за допомогою фабрики
    ships = {
        101: ShipFactory.create_lightweight_ship(id=101, fuel=15000.0, current_port=ports[1]),
        102: ShipFactory.create_medium_ship(id=102, fuel=15000.0, current_port=ports[2]),
        103: ShipFactory.create_heavy_ship(id=103, fuel=15000.0, current_port=ports[3])
    }

    # Завантаження контейнерів на кораблі
    for i in range(1, 3):
        container_basic = create_container(id=i, weight=1000 + i * 500)  # BasicContainer
        ports[1].load_container(container_basic)  # Завантажуємо в порт
        ships[101].add_item(container_basic)  # Завантажуємо на корабель 101
        
        container_heavy = create_container(id=i + 2, weight=2000 + i * 500)  # HeavyContainer
        ports[1].load_container(container_heavy)  # Завантажуємо в порт
        ships[102].add_item(container_heavy)  # Завантажуємо на корабель 102

    # Переміщення кораблів
    print("\nShip 101 is sailing from Odessa to Agrinio:")
    ships[101].sail_to(ports[2])  # Легкий корабель пливе до Агрініо

    print("\nShip 102 is sailing from Agrinio to Catanzaro:")
    ships[102].sail_to(ports[3])  # Середній корабель пливе до Катандзаро

    print("\nShip 103 is sailing from Catanzaro to Odessa:")
    ships[103].sail_to(ports[1])  # Важкий корабель пливе до Одеси

    # Вивантаження контейнерів у портах
    for port in ports.values():
        for ship in port.current_ships:
            while ship.containers:  # Вивантажуємо всі контейнери
                container = ship.containers[0]  # Беремо перший контейнер
                ship.unload(container)  # Вивантажуємо контейнер
                port.load_container(container)  # Завантажуємо контейнер у порт
                print(f"Unloaded container {container.id} from Ship {ship.id} to Port {port.id}")

    # Збереження даних у JSON
    save_to_json(ports, ships, "simulation_data.json")

    # Завантаження даних з JSON
    loaded_ports, loaded_ships = load_from_json("simulation_data.json")
    print("\nЗавантажено з JSON:")
    for port in loaded_ports.values():
        print(f"Port {port.id}, coordinates: {port.coordinates}")

    for ship in loaded_ships.values():
        print(f"Ship {ship.id}, fuel: {ship.fuel}, max weight: {ship.total_weight_capacity}")

    # Виведення результатів
    print("\nResults:")
    for port in sorted(loaded_ports.values(), key=lambda p: p.id):
        print(f"Port {port.id}:")
        for ship in port.current_ships:
            print(f"  Ship {ship.id}, Fuel: {ship.fuel}")
        for container in port.containers:  # Виводимо контейнери в порту
            print(f"    Container {container.id}: {container.weight} kg")

if __name__ == "__main__":
    main()
