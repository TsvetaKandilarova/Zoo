import unittest
from subprocess import call
from animals import Animal
from create_table import create_tables
import interface
import sqlite3


class TestInterface(unittest.TestCase):
    """docstring for TestInterface"""
    # I should create a dummy zoo table too
    def setUp(self):
        self.conn = sqlite3.connect('test_interface.db')
        cursor = self.conn.cursor()
        create_tables(cursor)
        self.conn.commit()
        # Animal(self, species, age, name, gender, weight)
        tiger_stats = cursor.execute("SELECT * FROM animal_types\
         WHERE species = 'tiger'").fetchall()[0]
        self.tiger = Animal(tiger_stats[1], 18, "Pencho", 'male', 19)
        lion_stats = cursor.execute("SELECT * FROM animal_types\
            WHERE species = 'lion'").fetchall()[0]
        self.lion = Animal(lion_stats[1], 24, "Svetla", "female", 17)

    # <name> : <species>, <age>, <weight>
    def test_see_animals(self):
        pass
        # line1 = "Pencho : tiger, 18, 19"
        # line2 = "Svetla : lion, 24, 17"
        # animals_listed = [line1, line2]
        # result = "\n".join(animals_listed)
        # self.assertEqual(result, interface.see_animals('test_interface.db'))

    def tearDown(self):
        self.conn.close()
        call('rm test_interface.db', shell=True)


if __name__ == '__main__':
    unittest.main()
