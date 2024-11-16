import unittest
from Classes.containers import BasicContainer, HeavyContainer, create_container
from Classes.item import Small
from Classes.port import Port


class Test(unittest.TestCase):
    
    def setUp(self):
        self.basic_container = BasicContainer(1500, 10)
        self.item1 = Small(13, 7)
        self.port = Port(coordinates=(12, 12))
    
    def test_load_item(self):
        result = self.basic_container.load_item(self.item1)
        self.assertTrue(result)
        self.assertIn(self.item1, self.basic_container.items_in_the_container)
        
    def test_load_item_again(self):
        self.basic_container.load_item(self.item1)
        result = self.basic_container.load_item(self.item1)
        self.assertFalse(result)
        self.assertEqual(len(self.basic_container.items_in_the_container), 1)
        
    def test_unload(self):
        self.basic_container.load_item(self.item1)
        result = self.basic_container.unload_item(self.item1, self.port)
        self.assertTrue(result)
        self.assertEqual(len(self.basic_container.items_in_the_container), 0)
        
    def test_unload_non_existent_item(self):
        result = self.basic_container.unload_item(self.item1, self.port)
        self.assertFalse(result)
        
    def test_load_limit(self):
        for _ in range(10):
            item = Small(10, 1)
            result = self.basic_container.load_item(item)
            self.assertTrue(result)
        item_11 = Small(10, 1)
        result = self.basic_container.load_item(item_11)
        self.assertFalse(result)

    def test_create_heavy_container(self):
        heavy_container = create_container(3500, 20, "heavy")
        self.assertIsInstance(heavy_container, HeavyContainer)
        self.assertEqual(heavy_container.weight, 3500)
        self.assertEqual(heavy_container.max_item, 20)
        
    def test_create_heavy_basic_container(self):
        with self.assertRaises(ValueError):
            create_container(3200, 20, 'basic')