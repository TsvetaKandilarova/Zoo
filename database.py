import sqlite3
from animals import Animal
from random import randint


class Database():
    """docstring for Database"""
    def __init__(self, db_name="zoo.db"):
        self.name = db_name
        self.an_conn = sqlite3.connect("animals.db")
        self.zoo_conn = sqlite3.connect(db_name)
        self.create_tables()

    def get_name(self):
        return self.name

    def create_tables(self):
        c = self.zoo_conn.cursor()
        c.execute('''create table if not exists zoo
            (id integer primary key, species text, age float,
                name text, gender text, weight real)''')
        c.execute('''create table if not exists breeding
            (id int, last_breed int,
                foreign key (id) references zoo(id))''')
        self.zoo_conn.commit()

    def insert_into_breeding_table(self, animal):
        name = animal.get_name()
        species = animal.get_species()
        c = self.zoo_conn.cursor()
        id = c.execute("SELECT id from zoo WHERE name = ? AND species = ?", (name, species)).fetchall()[0]
        id = id[0]
        c.execute("INSERT INTO breeding VALUES(?, ?)", (id, 0))
        self.zoo_conn.commit()

    def insert_animal(self, animal):
        name = animal.get_name()
        age = animal.get_age()
        species = animal.get_species()
        gender = animal.get_gender()
        weight = animal.get_weight()
        c = self.zoo_conn.cursor()
        list = c.execute("SELECT name FROM zoo WHERE name = ?", (name,)).fetchall()
        if len(list) == 0:
            c.execute("INSERT INTO zoo (species, age, name, gender, weight)\
                VALUES (?, ?, ?, ?, ?)", (species, age, name, gender, weight))
            if gender == 'female':
                self.insert_into_breeding_table(animal)
        self.zoo_conn.commit()

    def remove_animal(self, species, name):
        c = self.zoo_conn.cursor()
        query = "SELECT id FROM zoo WHERE species=? AND name=?"
        animal_id = c.execute(query, (species, name)).fetchone()
        if animal_id is not None:
            c.execute("DELETE FROM zoo WHERE species=? AND name=?\
                ", (species, name))
            c.execute("DELETE FROM breeding WHERE id=?", (str(animal_id[0]), ))
        self.zoo_conn.commit()

    def initial_fill_with_animals(self):
        # Animal(species, age, name, gender, weight)
        lion1 = Animal("lion", 10, "Svetla", "female", 160)
        lion2 = Animal("lion", 6, "Gosho", "male", 190)
        tiger1 = Animal("tiger", 12, "Tsveta", "female", 200)
        tiger2 = Animal("tiger", 10, "Joro", "male", 230)
        red_panda1 = Animal("red panda", 3, "Lubka", "female", 4)
        red_panda2 = Animal("red panda", 4, "Lucho", "male", 4.5)
        hippo1 = Animal("hippo", 22, "Anastasiya", "female", 1200)
        hippo2 = Animal("hippo", 15, "Zlatin", "male", 1300)
        goat1 = Animal("goat", 2, "Veska", "female", 40)
        goat2 = Animal("goat", 4, "Niki", "male", 50)
        self.insert_animal(lion1)
        self.insert_animal(lion2)
        self.insert_animal(tiger1)
        self.insert_animal(tiger2)
        self.insert_animal(red_panda1)
        self.insert_animal(red_panda2)
        self.insert_animal(hippo1)
        self.insert_animal(hippo2)
        self.insert_animal(goat1)
        self.insert_animal(goat2)

    def get_males(self, species):
        c = self.zoo_conn.cursor()
        query = "SELECT name FROM zoo WHERE gender='male' and species=?"
        males = c.execute(query, (species, )).fetchall()
        return males

    def has_a_male_species(self, species):
        males = self.get_males(species)
        return len(males) > 0

    def get_male_name(self, species):
        males = self.get_males(species)
        return males[randint(0, len(males) - 1)][0]

    def get_females(self):
        c = self.zoo_conn.cursor()
        query = "SELECT species, name FROM zoo WHERE gender='female'"
        return c.execute(query).fetchall()

    def get_life_expectancy(self, species):
        c = self.an_conn.cursor()
        query = "SELECT life_expectancy FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_food_type(self, species):
        c = self.an_conn.cursor()
        query = "SELECT food_type FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_gestation(self, species):
        c = self.an_conn.cursor()
        query = "SELECT gestation FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_newborn_weight(self, species):
        c = self.an_conn.cursor()
        query = "SELECT newborn_weight FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_average_weight(self, species):
        c = self.an_conn.cursor()
        query = "SELECT average_weight FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_weight_age_ratio(self, species):
        c = self.an_conn.cursor()
        query = "SELECT weight_age_ratio FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_food_weight_ratio(self, species):
        c = self.an_conn.cursor()
        query = "SELECT food_weight_ratio FROM animals WHERE species = ?"
        return c.execute(query, (species, )).fetchone()[0]

    def get_last_breed(self, species, name):
        c = self.zoo_conn.cursor()
        query = "SELECT last_breed FROM breeding\
        join zoo ON zoo.species=? and zoo.name=? AND breeding.id=zoo.id"
        result = c.execute(query, (species, name)).fetchone()[0]
        return result

    def set_last_breed(self, species, name, last_breed):
        c = self.zoo_conn.cursor()
        query = "SELECT id FROM zoo WHERE species=? AND name=?"
        id = c.execute(query, (species, name)).fetchone()[0]
        update_query = "UPDATE breeding SET last_breed=? WHERE id=?"
        c.execute(update_query, (last_breed, id))

    def set_age(self, species, name, new_age):
        c = self.zoo_conn.cursor()
        update_query = "UPDATE zoo SET age = ? WHERE name = ? AND species = ?"
        c.execute(update_query, (new_age, name, species))

    def set_weight(self, species, name, new_weight):
        c = self.zoo_conn.cursor()
        update_query = "UPDATE zoo SET weight=? WHERE name=? AND species=?"
        c.execute(update_query, (new_weight, name, species))
