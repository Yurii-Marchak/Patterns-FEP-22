import unittest
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from port import Port
from ship import ShipFactory

class TestContainers(unittest.TestCase):

    def test_basic_container_consumption(self):
        container = BasicContainer(1, 1000)
        self.assertEqual(container.consumption(), 2500)  # 1000 * 2.5

    def test_heavy_container_consumption(self):
        container = HeavyContainer(2, 2000)
        self.assertEqual(container.consumption(), 6000)  # 2000 * 3.0

    def test_refrigerated_container_consumption(self):
        container = RefrigeratedContainer(3, 1500)
        self.assertEqual(container.consumption(), 7500)  # 1500 * 5.0

    def test_liquid_container_consumption(self):
        container = LiquidContainer(4, 2000)
        self.assertEqual(container.consumption(), 8000)  # 2000 * 4.0

class TestPort(unittest.TestCase):

    def test_load_container(self):
        port = Port(1, (46.48, 30.73))
        container = BasicContainer(1, 1000)
        port.containers.append(container)  # Завантажуємо в порт
        self.assertEqual(len(port.containers), 1)

    def test_unload_container(self):
        port = Port(1, (46.48, 30.73))
        ship = ShipFactory.create_lightweight_ship(101, 500, port)
        container = HeavyContainer(2, 2000)
        ship.add_item(container)  # Додаємо контейнер на корабель
        self.assertEqual(len(ship.containers), 1)  # Корабель має 1 контейнер
        ship.containers.remove(container)  # Розвантажуємо контейнер
        self.assertEqual(len(ship.containers), 0)  # Корабель порожній

if __name__ == "__main__":
    unittest.main()
