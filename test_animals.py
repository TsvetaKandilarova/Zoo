import unittest
from subprocess import call
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
        self.lion = (lion_stats[1], 24, "Svetla", "female", 17)

    def test_somthing(self):
        pass

    def tearDown(self):
        self.conn.close()
        call('rm animal_types.db', shell=True)

if __name__ == '__main__':
    unittest.main()
