import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import uuid
from ship import ShipFactory
from port import Port
from item import ItemFactory
from containers import create_container


class Main:

    def __init__(self) -> None:
        self.item_factory = ItemFactory()
        self.ship_factory = ShipFactory()
        self.items, self.ports, self.containers, self.ships = self.load_from_json('Classes/output_data.json')

    def load_from_json(self, filename: str):
        with open(filename, 'r') as f:
            data = json.load(f)

        items = []
        for item_data in data['items']:
            item_id = item_data.get('id', str(uuid.uuid4()))

            item = self.item_factory.create_items(
                item_type = item_data['type'],
                weight = item_data['weight'],
                count = item_data['count']
            )

            item.item_id = item_id
            items.append(item)

        ports = []
        for port_data in data['port']:
            port_id = port_data.get('port_id', str(uuid.uuid4()))
            coordinates = tuple(port_data['coordinates'])

            port = Port(coordinates=coordinates)
            port.port_id = port_id
            ports.append(port)

        containers = []
        for container_data in data['container']:
            container_id = container_data.get('id', str(uuid.uuid4()))
            weight = float(container_data['weight'])
            max_item = container_data['max_item']
            container_type = container_data['container_type']

            container = create_container(weight, max_item, container_type)

            container.container_id = container_id
            containers.append(container)

        ships = []
        for ship_data in data['ship']:
            ship_type = ship_data['type']
            current_port_id = ship_data.get('current_port', None)
            current_port = next((port for port in ports if port.port_id == current_port_id), None)
            if current_port:
                ship = self.ship_factory.create_ship(ship_type, current_port)
                ships.append(ship)

        return items, ports, containers, ships

    def save_data_to_json(self, filename='Classes/data.json'):
        data = {
            "ports": [port.port_data() for port in self.ports],
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


    def test(self):
        ship_1 = self.ships[0]
        ship_2 = self.ships[1]
        ship_3 = self.ships[2]

        port_1 = self.ports[0]
        port_2 = self.ports[1]
        port_3 = self.ports[2]

        cont_1 = self.containers[0]
        cont_1.load_item(self.items[0])
        cont_2 = self.containers[1]
        cont_2.load_item(self.items[1])
        cont_3 = self.containers[2]
        cont_3.load_item(self.items[2])

        ship_1.load(cont_1)
        ship_1.load(cont_2)
        ship_3.load(cont_3)

        ship_3.sail_to(port_1, self.ports)
        ship_3.un_load(cont_3, port_1)

        ship_3.sail_to(port_2, self.ports)

main = Main()
main.test()
main.save_data_to_json()
