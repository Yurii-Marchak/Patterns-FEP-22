import unittest
from managementSystem import AdvancedPortManagementSystem

class TestPortManagementSystemIntegration(unittest.TestCase):
    """
    Integration tests for the PortManagementSystem functionality.

    This test suite covers the creation of ports, containers, and ships,
    loading and unloading containers, refueling ships, and sailing between ports.
    """

    def setUp(self):
        """
        Set up the initial state for the tests by creating a PortManagementSystem instance,
        two ports, several containers, and a ship.
        """
        self.management_system = AdvancedPortManagementSystem()
        self.port1 = self.management_system.create_port(1000, 2000)
        self.port2 = self.management_system.create_port(1000, 3000)

        # Create containers at port1
        self.container1 = self.management_system.create_container(1, 4000)
        self.container2 = self.management_system.create_container(1, 3000)
        self.container3 = self.management_system.create_container(1, 4000, 'L')
        self.container4 = self.management_system.create_container(1, 4000, 'R')

        # Create a ship at port1
        self.ship = self.management_system.create_ship(1, 16000, 10, 3, 0, 1, 10)

    def test_port_management_integration(self):
        """
        Test the integration of the PortManagementSystem functionalities, including:
        - Loading and unloading containers onto/from the ship.
        - Refueling the ship.
        - Sailing the ship to another port.
        """

        # Load containers onto the ship
        self.assertTrue(self.ship.load(self.container1), "Container 1 should load successfully.")
        self.assertTrue(self.ship.load(self.container2), "Container 2 should load successfully.")
        self.assertFalse(self.ship.load(self.container3), "Container 3 should not load due to constraints.")
        self.assertTrue(self.ship.load(self.container4), "Container 4 should load successfully.")

        # Refuel the ship based on container weights and fuel consumption
        fuel_cost = 1000 * 50 + 4000 * 3 + 3000 * 2.5 + 4000 * 5
        self.ship.re_fuel(fuel_cost)

        # Attempt to sail the ship to port2
        self.assertTrue(self.ship.sail_to(self.port2), "Ship should sail to port2 successfully.")

        # Unload containers from the ship
        self.assertTrue(self.ship.unload(self.container1), "Container 1 should unload successfully.")
        self.assertTrue(self.ship.unload(self.container2), "Container 2 should unload successfully.")
        self.assertFalse(self.ship.unload(self.container3), "Container 3 should not unload because it wasn't loaded.")
        self.assertTrue(self.ship.unload(self.container4), "Container 4 should unload successfully.")


if __name__ == "__main__":
    unittest.main()
