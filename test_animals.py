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

    def test_somthing(self):
        pass


    def tearDown(self):
        self.conn.close()
        call('rm animal_types.db', shell=True)

if __name__ == '__main__':
    unittest.main()
