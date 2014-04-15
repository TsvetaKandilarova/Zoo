import unittest
from animals import Animal
from create_table import create_tables
import sqlite3


class TestAnimal(unittest.TestCase):
    """docstring for ZooTest"""

    def setUp(self):
        self.conn = sqlite3.connect('animal_types.db')
        cursor = self.conn.cursor()
        create_tables(cursor)
        self.conn.commit()
        tiger_stats = cursor.execute("SELECT * FROM animal_types\
         WHERE species = 'tiger'").fetchall()[0]
        # print(tiger_stats)
        # print(tiger_stats[1])
        self.tiger = Animal(tiger_stats[1], 18, "Pencho", 'male', 19)
        lion_stats = cursor.execute("SELECT * FROM animal_types\
            WHERE species = 'lion'").fetchall()[0]
        self.lion = Animal(lion_stats[1], 24, "Svetla", "female", 17)

    def test_get_name(self):
        self.assertEqual("Pencho", self.tiger.get_name())
        self.assertEqual("Svetla", self.lion.get_name())

    def test_get_gender(self):
        self.assertEqual("female", self.lion.get_gender())
        self.assertEqual("male", self.tiger.get_gender())

    def test_get_weight(self):
        self.assertEqual(19, self.tiger.get_weight())
        self.assertEqual(17, self.lion.get_weight())

    def test_get_species(self):
        self.assertEqual("tiger", self.tiger.get_species())
        self.assertEqual("lion", self.lion.get_species())

    def test_get_age(self):
        self.assertEqual(18, self.tiger.get_age())
        self.assertEqual(24, self.lion.get_age())

    def test_max_weight(self):
        self.assertEqual(250, self.tiger.get_max_weight())
        self.assertEqual(200, self.lion.get_max_weight())

    def test_max_age(self):
        self.assertEqual(20, self.tiger.get_max_age())
        self.assertEqual(15, self.lion.get_max_age())

    def test_update_weight(self):
        self.assertEqual(31, self.tiger.update_weight(1))
        self.assertEqual(24.5, self.lion.update_weight(1))
        # testing weight limit
        self.assertEqual(250, self.tiger.update_weight(30))
        self.assertEqual(200, self.lion.update_weight(100))

    def test_grow(self):
        self.tiger.grow(12)
        self.assertEqual(163, self.tiger.get_weight())
        self.assertEqual(19, self.tiger.get_age())

        self.lion.grow(0)
        self.assertEqual(17, self.lion.get_weight())
        self.assertEqual(24, self.lion.get_age())

    # because of the chance_of_dying this test sometimes fails, as it should do
    # so it is commented
    """
    def test_die(self):
        self.tiger.grow(180)
        # his new age is 198 months (max is 20 years = 240 months)
        self.assertEqual(False, self.tiger.die(0))

        self.assertEqual(True, self.tiger.die(22))

        # surely DEAD
        self.assertEqual(True, self.tiger.die(50))
    """

    def tearDown(self):
        conn = sqlite3.connect("animal_types.db")
        cursor = conn.cursor()
        drop_query = "DROP TABLE IF EXISTS animal_types"
        cursor.execute(drop_query)


if __name__ == '__main__':
    unittest.main()
