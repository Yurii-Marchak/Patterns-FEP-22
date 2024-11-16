import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from port import Port
from ship import Ship


class TestPort(unittest.TestCase):

    def setUp(self):
        """
        Creates a test port and ships for testing.
        """
        self.port_a = Port(id=1, coordinates=(54.3520, 18.6466))  
        self.port_b = Port(id=2, coordinates=(53.4286, 14.5524))  

        self.ship1 = Ship(id=1, current_port=self.port_a, fuel=100.0, capacity=None, fuel_consumption_per_km=1.0)
        self.ship2 = Ship(id=2, current_port=self.port_a, fuel=200.0, capacity=None, fuel_consumption_per_km=1.5)
        self.ship3 = Ship(id=3, current_port=self.port_b, fuel=300.0, capacity=None, fuel_consumption_per_km=2.0)

    def test_initialization(self):
        """
        Tests the correctness of initializing the fields of the `Port` object.
        """
        self.assertEqual(self.port_a.id, 1)
        self.assertEqual(self.port_a.coordinates, (54.3520, 18.6466))
        self.assertEqual(self.port_a.list_of_containers, [])
        self.assertEqual(self.port_a.current_ships, [])
        self.assertEqual(self.port_a.history_list_of_ships, [])

    def test_incoming_ship(self):
        """
        Tests adding a ship to the port.
        """
        self.port_a.incoming_ship(self.ship1)
        self.assertIn(self.ship1, self.port_a.current_ships)
        self.assertIn(self.ship1, self.port_a.history_list_of_ships)

   
        self.port_a.incoming_ship(self.ship2)
        self.assertIn(self.ship2, self.port_a.current_ships)
        self.assertIn(self.ship2, self.port_a.history_list_of_ships)

    def test_outgoing_ship(self):
        """
        Tests removing a ship from the port.
        """
        self.port_a.incoming_ship(self.ship1)
        self.port_a.incoming_ship(self.ship2)
    
        self.port_a.outgoing_ship(self.ship1)
        self.assertNotIn(self.ship1, self.port_a.current_ships)

        self.assertIn(self.ship1, self.port_a.history_list_of_ships)

    def test_get_distance(self):
        """
        Tests the calculation of the distance between two ports.
        """
        distance = self.port_a.get_distance(self.port_b)
        expected_distance =  287.22  
        self.assertAlmostEqual(distance, expected_distance, delta=1.0)  


if __name__ == "__main__":
    unittest.main()

