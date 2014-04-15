import sqlite3
from random import randint


# the periods of time are in months
class Animal():
    """docstring for Animal"""
    def __init__(self, species, age, name, gender, weight):
        self.__species = species
        self.__age = age
        self.__name = name
        self.__gender = gender
        self.__weight = weight

    def get_name(self):
        return self.__name

    def get_gender(self):
        return self.__gender

    def get_weight(self):
        return self.__weight

    def get_max_weight(self):
        self.conn = sqlite3.connect('animals.db')
        cursor = self.conn.cursor()
        query = "SELECT average_weight FROM animals WHERE \
        species = ?"
        max_weight = cursor.execute(query, (self.__species, )).fetchall()[0][0]
        return max_weight

    # max_age is in years
    def get_max_age(self):
        self.conn = sqlite3.connect('animals.db')
        cursor = self.conn.cursor()
        query = "SELECT life_expectancy FROM animals WHERE \
        species = ?"
        max_age = cursor.execute(query, (self.__species, )).fetchall()[0][0]
        return max_age

    def update_weight(self, period):
        self.conn = sqlite3.connect('animals.db')
        cursor = self.conn.cursor()
        query = "SELECT weight_age_ratio FROM animals WHERE \
        species = ?"
        result = cursor.execute(query, (self.__species, )).fetchall()
        # print(result)
        new_weight = self.get_weight() + result[0][0] * period
        max_weight = self.get_max_weight()
        if(new_weight > max_weight):
            self.__weight = max_weight
        else:
            self.__weight = new_weight

        return self.__weight

    def get_species(self):
        return self.__species

    def get_age(self):
        return self.__age

    def grow(self, period):
        self.update_weight(period)
        new_age = (self.get_age() * 12 + period) / 12
        self.__age = new_age

    def feed(self, food_weight_ratio):
        return (food_weight_ratio * self.get_weight())

    def die(self, period):
        new_age = self.get_age() * 12 + period
        life_expectancy = self.get_max_age() * 12
        chance_of_dying = new_age * 100 / life_expectancy / 2
        # reducing the chance of dying by 2, because it seems unnatural for a
        # 10-years old tiger to have a 50% chance of dying :?
        if(new_age > life_expectancy):
            self.__age = life_expectancy
            return True
        else:
            self.__age = new_age / 12
            if(chance_of_dying > randint(1, 100)):
                return True
            return False
