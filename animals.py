import sqlite3
from random import randint


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

    def update_weight(self, period):
        self.conn = sqlite3.connect('animals.db')
        cursor = self.conn.cursor()
        query = "SELECT weight_age_ratio FROM animals WHERE \
        species = ?"
        result = cursor.execute(query, (self.__species, )).fetchall()[0][0]
        self.__weight = self.__weight + result * period / 30

        return self.__weight

    def get_species(self):
        return self.__species

    def get_age(self):
        return self.__age

    def grow(self):
        pass

    def eat(self):
        pass

    def die(self):
        pass
