from database import Database
from animals import Animal
import unittest
from subprocess import call


class DatabaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_zoo.db")
        self.a = Animal("lion", 24, "Svetla", "female", 150)
        self.db.insert_animal(self.a)
        self.c = self.db.zoo_conn.cursor()

    def test_insert_animal(self):
        animal_from_db = self.c.execute('''SELECT * FROM zoo''').fetchall()[0]
        self.assertEqual((1, "lion", 24, "Svetla", "female", 150),
            animal_from_db)
        last_breed_from_db = self.c.execute('''SELECT id, last_breed
                        FROM breeding''').fetchall()[0]
        self.assertEqual((1, 0), last_breed_from_db)

    def test_insert_second_animal(self):
        self.a2 = Animal("tiger", 24, "Tsveta", "female", 120)
        self.db.insert_animal(self.a2)
        animal_from_db = self.c.execute('''SELECT * FROM zoo''').fetchall()[1]
        self.assertEqual((2, "tiger", 24, "Tsveta", "female", 120),
            animal_from_db)
        last_breed_from_db = self.c.execute('''SELECT id, last_breed
                        FROM breeding''').fetchall()[1]
        self.assertEqual((2, 0), last_breed_from_db)

    def test_remove_animal(self):
        breed_from_db = self.c.execute("SELECT * from breeding").fetchall()
        self.assertEqual(1, len(breed_from_db))

        self.db.remove_animal("lion", "Svetla")

        animal_from_db = self.c.execute("SELECT * FROM zoo").fetchall()
        self.assertEqual(0, len(animal_from_db))

        breed_from_db = self.c.execute("SELECT * from breeding").fetchall()
        self.assertEqual(0, len(breed_from_db))

    def test_get_males_with_no_males(self):
        self.assertEqual(0, len(self.db.get_males("lion")))

    def test_get_males_with_one_male(self):
        a2 = Animal("lion", 24, "Pencho", "male", 150)
        self.db.insert_animal(a2)
        self.assertEqual([("Pencho", )], self.db.get_males("lion"))

    def test_has_a_male_species(self):
        self.assertFalse(self.db.has_a_male_species("lion"))

    def test_get_females(self):
        self.assertEqual([("lion", "Svetla")], self.db.get_females())

    def test_get_life_expectancy(self):
        self.assertEqual(15, self.db.get_life_expectancy("lion"))

    def test_get_food_type(self):
        self.assertEqual("carnivore", self.db.get_food_type("lion"))

    def test_get_gestation(self):
        self.assertEqual(3, self.db.get_gestation("lion"))

    def test_get_newborn_weight(self):
        self.assertEqual(2.0, self.db.get_newborn_weight("lion"))

    def test_get_average_weight(self):
        self.assertEqual(200, self.db.get_average_weight("lion"))

    def test_get_weight_age_ratio(self):
        self.assertEqual(7.5, self.db.get_weight_age_ratio("lion"))

    def test_get_food_weight_ration(self):
        self.assertEqual(0.035, self.db.get_food_weight_ratio("lion"))

    def test_get_last_breed(self):
        self.assertEqual(0, self.db.get_last_breed("lion", "Svetla"))

    def test_set_last_breed(self):
        self.db.set_last_breed("lion", "Svetla", 3)
        result = self.db.get_last_breed("lion", "Svetla")
        self.assertEqual(result, 3)

    def test_set_age(self):
        self.db.set_age("lion", "Svetla", 30)
        query = "SELECT age FROM zoo WHERE species = ? AND name = ?"
        result = self.c.execute(query, ("lion", "Svetla")).fetchall()
        self.assertEqual(30, result[0][0])

    def test_set_weight(self):
        self.db.set_weight("lion", "Svetla", 195)
        query = "SELECT weight FROM zoo WHERE species = ? AND name = ?"
        result = self.c.execute(query, ("lion", "Svetla")).fetchall()
        self.assertEqual(195, result[0][0])

    def tearDown(self):
        call("rm {}".format(self.db.name), shell=True)


if __name__ == '__main__':
    unittest.main()
