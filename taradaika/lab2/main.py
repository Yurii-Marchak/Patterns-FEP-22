from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from port import Port
    from container import create_container
    from ship import Ship, Capacity


def main():
  
    port_a = Port(id=1, coordinates=(49.8383, 24.0232), list_of_containers=[], current_ships=[], history_list_of_ships=[])
    port_b = Port(id=2, coordinates=(50.4501, 30.5234), list_of_containers=[], current_ships=[], history_list_of_ships=[])

    container1 = create_container(weight=2500, container_type="basic")
    container2 = create_container(weight=4000, container_type="heavy")
    container3 = create_container(weight=3000, container_type="refrigerated")
    container4 = create_container(weight=3500, container_type="liquid")


    ship_capacity = Capacity(
        total_weight_capacity=15000,
        max_all_containers=10,
        max_heavy_containers=5,
        max_refrigerated_containers=3,
        max_liquid_containers=2,
        list_of_containers=[]
    )


    ship = Ship(
        id=1,
        current_port=port_a,
        fuel=500,  
        capacity=ship_capacity,
        fuel_consumption_per_km=1.5, 
        list_of_containers=[]
    )

    
    ship.load(container1)
    ship.load(container2)
    ship.load(container3)
    ship.load(container4)





if __name__ == "__main__":
    main()

