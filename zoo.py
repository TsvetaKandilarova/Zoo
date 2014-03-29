from animals import Animal
import sqlite3


class Zoo():
    """docstring for Zoo"""
    def __init__(self, animals, name, capacity, budget):
        self.__animals = animals
        self.__name = name
        self.__capacity = capacity
        self.__budget = budget
        self.__size = len(animals)




