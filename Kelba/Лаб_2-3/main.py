from ports import Port
from ship import LightWeightShip, MediumShip, HeavyShip
from container import BasicContainer, RefrigeratedContainer, LiquidContainer

def main():
    port1 = Port(1, 39.0, 74.0)
    port2 = Port(2, 42.0, 8.0)

    ship1 = LightWeightShip(1, port1, 5000)
    port1.incomingShip(ship1)

    container1 = BasicContainer(1, 2000)
    container2 = RefrigeratedContainer(2, 4000)
    container3 = LiquidContainer(3, 5000)

    ship1.load(container1)
    ship1.load(container2)
    ship1.load(container3)

    print(f"Ship's state before sailing: {ship1.to_dict()}")

    success = ship1.sailTo(port2)
    if success:
        print(f"Ship successfully arrived at port {port2.ID}")
    else:
        print("Not enough fuel to sail.")

    print(f"Ship's state after sailing: {ship1.to_dict()}")

    ship1.reFuel(1000)
    print(f"After refueling: {ship1.to_dict()}")

    ship1.unLoad(container2)
    ship1.unLoad(container3)
    ship1.unLoad(container1)
    print(f"Ship's state after unloading: {ship1.to_dict()}")

if __name__ == "__main__":
    main()
