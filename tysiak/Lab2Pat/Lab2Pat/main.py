from containers import create_container, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from port import Port
from ship import Ship

def main():
       
    """
    Main function to simulate a port management system.
    
    The function performs the following tasks:
    - Creates ports and ships.
    - Assigns ships to their respective ports.
    - Loads containers onto ships.
    - Simulates ships sailing between ports.
    - Unloads containers from ships.
    - Refuels ships.
    - Outputs the status of ports, ships, and containers.
    """

    # Create ports 
    ports = {
        1: Port(1, (46.48, 30.73)),  # Odessa
        2: Port(2, (38.37, 21.24)),  # Agrinio
        3: Port(3, (38.91, 16.35))   # Catanzaro
        
    }

    # Create ships 
    ships = {
        101: Ship(
            id=101,
            fuel=13000.0,
            current_port=ports[1],  # Initially in Odessa
            total_weight_capacity=10000,
            max_containers=10,
            max_heavy=5,
            max_refrigerated=2,
            max_liquid=2,
            fuel_per_km=7.0
        ),
        102: Ship(
            id=102,
            fuel=13600.0,
            current_port=ports[2],  # Initially in Agrinio
            total_weight_capacity=12000,
            max_containers=12,
            max_heavy=6,
            max_refrigerated=3,
            max_liquid=3,
            fuel_per_km=8.0
        ),
        103: Ship(
            id=103,
            fuel=15000.0,
            current_port=ports[3],  # Initially in Catanzaro
            total_weight_capacity=9000,
            max_containers=8,
            max_heavy=4,
            max_refrigerated=2,
            max_liquid=2,
            fuel_per_km=10.0
        )
    }

    # Add ships to ports
    ports[1].incoming_ship(ships[101])
    ports[2].incoming_ship(ships[102])
    ports[3].incoming_ship(ships[103])

    # Ship 101 (Odessa)
    container1 = create_container(id=1, weight=2000, container_type='')  # BasicContainer
    container2 = create_container(id=2, weight=4000, container_type='')  # HeavyContainer
    ships[101].load(container1)
    ships[101].load(container2)

    # Ship 102 (Agrinio) 
    container3 = create_container(id=3, weight=2500, container_type='')  # BasicContainer
    container4 = create_container(id=4, weight=4500, container_type='L')  # LiquidContainer
    ships[102].load(container3)
    ships[102].load(container4)

    # Ship 103 (Catanzaro) 
    container5 = create_container(id=5, weight=3000, container_type='')  # BasicContainer
    container6 = create_container(id=6, weight=5000, container_type='R')  # RefrigeratedContainer
    ships[103].load(container5)
    ships[103].load(container6)

  
    print("\nShip 101 is sailing from Odessa to Catanzaro:")
    ships[101].sail_to(ports[3]) 

   
    print("\nShip 102 is sailing from Agrinio to Catanzaro:")
    ships[102].sail_to(ports[1])

    
    print("\nShip 103 is sailing from Catanzaro to Odessa:")
    ships[103].sail_to(ports[2])

   
    print("\nUnloading containers successful!")
    ships[101].unload(container1)
    ships[102].unload(container3)
    ships[103].unload(container6)

    
    print("\nRefueling ships successful!")
    ships[101].refuel(300.0)
    ships[102].refuel(350.0)
    ships[103].refuel(400.0)

   
    print("\nResults:")
    for port in sorted(ports.values(), key=lambda p: p.id):
        print(f"Port {port.id}: ({port.coordinates[0]:.2f}, {port.coordinates[1]:.2f})")
        print("  Ships:")
        for ship in sorted(port.current_ships, key=lambda s: s.id):
            print(f"    Ship {ship.id}: {ship.fuel:.2f} fuel left")
            print("    Containers:")
            for container in sorted(ship.containers, key=lambda c: c.id):
                print(f"      {container.__class__.__name__} {container.id}: Weight {container.weight}")

if __name__ == "__main__":
    main()
