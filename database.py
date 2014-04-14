import sqlite3
from random import randint


class Database():
    """docstring for Database"""
    def __init__(self, db_name="zoo.db"):
        self.name = db_name
        self.an_conn = sqlite3.connect("animals.db")
        self.zoo_conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        c = self.zoo_conn.cursor()
        c.execute('''create table if not exists zoo
            (id integer primary key, species text, age int,
                name text, gender text, weight real)''')
        c.execute('''create table if not exists breeding
            (id int, last_breed int,
                foreign key (id) references zoo(id))''')
        self.zoo_conn.commit()

    def insert_into_breeding_table(self, animal):
        c = self.zoo_conn.cursor()
        id = c.execute("SELECT id from zoo").fetchall()[0]
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
            c.execute("DELETE FROM breeding WHERE id=?", (str(animal_id[0], )))
        self.zoo_conn.commit()

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
