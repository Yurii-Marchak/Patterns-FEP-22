


from ship import ShipFactory, LightWeightShip, MediumShip, HeavyShip, Ship
from port import Port
from container import create_container, ItemFactory, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer, Container
import json
import os
from typing import List, Dict

def main():
    json_file_path = 'data.json'
    output_json_file_path = 'output.json'
    ship_factory = ShipFactory()

    ports = []
    ships = []
    containers = []


    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            data = json.load(f)


        for port_data in data.get('ports', []):
            port = Port(id=port_data['id'], coordinates=tuple(port_data['coordinates']))
            ports.append(port)

        for ship_data in data.get('ships', []):
            current_port_id = ship_data.get('current_port')
            current_port = next((port for port in ports if port.id == current_port_id), None)

            ship_type = ship_data['type']
            if ship_type == 'lightweight':
                ship = ship_factory.create_lightweight_ship(ship_data['id'], current_port, ship_data['fuel'])
            elif ship_type == 'heavy':
                ship = ship_factory.create_heavy_ship(ship_data['id'], current_port, ship_data['fuel'])
            elif ship_type == 'medium':
                ship = ship_factory.create_medium_ship(ship_data['id'], current_port, ship_data['fuel'])
            else:
                raise ValueError("Unknown ship type")

            ships.append(ship)


        for container_data in data.get('containers', []):
            container = create_container(container_type=container_data['type'], 
                                         max_weight=container_data['max_weight'], 
                                         max_items=container_data['max_items'])
            containers.append(container)
            for item_data in container_data['items']:
                item = ItemFactory.create_item(item_type=item_data['type'], 
                                               id=item_data['id'], 
                                               weight=item_data['weight'], 
                                               count=item_data['count'])
                container.add_item(item)


    for ship in ships:
        next_port_index = (ports.index(ship.current_port) + 1) % len(ports)
        ship.sail_to(ports[next_port_index])

    if containers and ships:
    
        ships[0].load(containers[0])


    save_to_json(output_json_file_path, ports, ships, containers)

def save_to_json(file_path: str, ports: List[Port], ships: List[Ship], containers: List[Container]) -> None:
    data = {
        "ports": [port.to_dict() for port in ports],
        "ships": [ship.to_dict() for ship in ships],
        "containers": [container.to_dict() for container in containers]
    }
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def custom_to_dict(obj):

    if hasattr(obj, 'to_dict'):
        return obj.to_dict()

    elif isinstance(obj, Ship):

        return {
            "id": obj.id,
            "current_port": custom_to_dict(obj.current_port) if obj.current_port else None,
            "fuel": obj.fuel,
            "containers": [custom_to_dict(container) for container in obj.list_of_containers]
        }

    elif isinstance(obj, Port):

        return {
            "id": obj.id,
            "coordinates": obj.coordinates,
            "containers": [custom_to_dict(container) for container in obj.list_of_containers],
            "ships": [custom_to_dict(ship) for ship in obj.current_ships]
        }

    elif isinstance(obj, Container):
        return obj.to_dict()
    else:
        raise TypeError(f"Object of type {obj.__class__.__name__} is not serializable")


if __name__ == '__main__':
    main()