from ship import Ship, Ship_Configuration
from port import Port
from containers import *
from typing import List


class Main:
    def __init__(self) -> None:
        self.containers: List['Container'] = [
            create_container(weight=2500, container_type='basic'),
            create_container(weight=3500, container_type='heavy'),
            create_container(weight=1500, container_type='basic'),
            create_container(weight=5000, container_type='heavy'),
            create_container(weight=2000, container_type='refrigerated'),
            create_container(weight=4000, container_type='liquid'),
            create_container(weight=2700, container_type='basic'),
            create_container(weight=5500, container_type='heavy'),
            create_container(weight=3200, container_type='refrigerated'),
            create_container(weight=4500, container_type='liquid'),
            create_container(weight=1800, container_type='basic'),
            create_container(weight=3800, container_type='heavy'),
            create_container(weight=2900, container_type='refrigerated'),
            create_container(weight=4200, container_type='liquid'),
            create_container(weight=2900, container_type='basic')
        ]
        self.ports: List['Port'] = [
            Port(coordinates=(51.0, 4.4)),
            Port(coordinates=(33.7, -118.2)),
            Port(coordinates=(1.3, 103.8))
        ]
        config1 = Ship_Configuration(
            total_weight_capasity=20000,
            max_number_of_all_containers=10,
            max_number_of_heavy_containers=3,
            max_number_of_refrigerated_containers=2,
            max_number_of_liquid_containers=2,
            max_number_of_basic_containers=3,
            fuel_consumption_per_km=1.2,
            maximum_amount_of_fuel=30000
        )

        config2 = Ship_Configuration(
            total_weight_capasity=30000,
            max_number_of_all_containers=15,
            max_number_of_heavy_containers=5,
            max_number_of_refrigerated_containers=3,
            max_number_of_liquid_containers=4,
            max_number_of_basic_containers=3,
            fuel_consumption_per_km=1.5,
            maximum_amount_of_fuel=20200
        )
        self.ships: List['Ship'] = [
            Ship(fuel=3500, current_port=self.ports[0], ship_configurations=config1, containers=[]),
            Ship(fuel=1900, current_port=self.ports[1], ship_configurations=config2, containers=[]),
            Ship(fuel=2600, current_port=self.ports[2], ship_configurations=config1, containers=[])
        ]

    def port_ship_info(self):
        
        for port in self.ports:
            print(f"Port id: {port.id}")
            print(f"Port coordinates: {port.coordinates}")
            if port.containers:
                print("\tContainers at the port:")
                print(f"\tBasic containers: {[c.id for c in port.containers if isinstance(c, BasicContainer)]}")
                print(f"\tRefrigerated containers: {[c.id for c in port.containers if isinstance(c, RefrigeratedContainer)]}")
                print(f"\tLiquid containers: {[c.id for c in port.containers if isinstance(c, LiquidContainer)]}")
                print(f"\tHeavy containers: {[c.id for c in port.containers if isinstance(c, HeavyContainer) and not isinstance(c, (RefrigeratedContainer, LiquidContainer))]}\n")

            else:
                print(f"No containers in this port")
            
            if port.list_of_ship:
                for ship in port.list_of_ship:
                    print(f"\t\tShip id: {ship.id}")
                    print(f"\t\tFuel level: {ship.fuel:.2f}")
                    print("\t\tContainers on a ship:")
                    print(f"\t\tBasic containers: {[c.id for c in ship.containers_on_the_ship if isinstance(c, BasicContainer)]}")
                    print(f"\t\tRefrigerated containers: {[c.id for c in ship.containers_on_the_ship if isinstance(c, RefrigeratedContainer)]}")
                    print(f"\t\tLiquid containers: {[c.id for c in ship.containers_on_the_ship if isinstance(c, LiquidContainer)]}")
                    print(f"\t\tHeavy containers: {[c.id for c in ship.containers_on_the_ship if isinstance(c, HeavyContainer) and not isinstance(c, (RefrigeratedContainer, LiquidContainer))]}\n")

            else:
                print("No ships in this port\n")

     
    def test(self):
        Ship_1 = self.ships[0]
        Ship_2 = self.ships[1]
        Ship_3 = self.ships[2]
        
        Port_1 = self.ports[0]
        Port_2 = self.ports[1]
        Port_3 = self.ports[2]
        
        Ship_1.load(self.containers[0])
        Ship_1.load(self.containers[1])
        Ship_1.load(self.containers[2])
        Ship_1.un_load(self.containers[0], Ship_1.current_port)
        
        Ship_2.load(self.containers[5])
        Ship_2.load(self.containers[6])
        Ship_2.load(self.containers[7])
        Ship_2.load(self.containers[8])
        Ship_2.sail_to(Port_3, self.ports)
        Ship_2.un_load(self.containers[7], Ship_2.current_port)
        Ship_2.un_load(self.containers[6], Ship_2.current_port)

        
main = Main()
main.port_ship_info()
main.test()
print('------------------------------')
main.port_ship_info()

