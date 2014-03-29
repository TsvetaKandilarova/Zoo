import sqlite3
from random import randint


class Animal():
    """docstring for Animal"""
    def __init__(self, species, age, name, gender, weight):
        self.species = species
        self.age = age
        self.name = name
        self.gender = gender
        self.weight = weight

    def get_species(self):
        return self.species

    def get_age(self):
        return self.age

    def grow(self):
        pass

    def eat(self):
        pass

    def die(self):
        pass
