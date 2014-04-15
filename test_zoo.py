import unittest
from subprocess import call
from zoo import Zoo
from animals import Animal
import sqlite3


class TestZoo(unittest.TestCase):
    """docstring for ZooTest"""

    def setUp(self):
        self.zoo = Zoo("Sofia", 2, 3000)

    def test_atributes(self):
        self.assertEqual("Sofia", self.zoo.get_name())
        self.assertEqual(2, self.zoo.get_capacity())
        self.assertEqual([], self.zoo.get_animals())

    def test_accomodate_animal(self):
        self.zoo.accommodate_animal('tiger', 18, "Zyblyo", 'male', 19)
        self.assertEqual(1, len(self.zoo.get_animals()))
        self.assertEqual(True, self.zoo.accommodate_animal('tiger', 18, "Anastasij", 'male', 19))

    def test_remove_animal(self):
        self.zoo.accommodate_animal('tiger', 18, "Zyblyo", 'male', 19)
        self.zoo.remove_animal('tiger', 'Zyblyo')
        self.assertEqual(0, len(self.zoo.get_animals()))

    def test_move_animal(self):
        self.zoo.accommodate_animal('tiger', 18, "Spiridon", 'male', 19)
        self.zoo.move_animal('tiger', 'Spiridon')
        self.assertEqual(0, len(self.zoo.get_animals()))

    def test_daily_incomes(self):
        self.zoo.accommodate_animal('tiger', 18, "Tsveta", 'male', 19)
        self.zoo.accommodate_animal('tiger', 18, "Svetla", 'male', 19)
        self.assertEqual(120, self.zoo.daily_incomes())

    def test_daily_expenses(self):
        self.zoo.accommodate_animal('tiger', 18, "Zyblyo", 'male', 19)
        self.assertEqual(19 * 0.06 * 4, self.zoo.daily_expenses())

    # def test_generate_name(self):
    #     pass

    # def test_born_animal(self):
    #     pass

    def tearDown(self):
        call('rm Sofia.db', shell=True)

if __name__ == '__main__':
    unittest.main()
