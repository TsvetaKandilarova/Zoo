from animals import Animal
from database import Database
import sqlite3
from random import randint

__INCOME_PER_ANIMAL = 60
__MEAT_COST = 4
__GRASS_COST = 2
__BREEDING_PERIOD = 6


class Zoo():
    """docstring for Zoo"""
    def __init__(self, name, capacity, budget):
        self.__animals = []
        self.__name = name
        self.__capacity = capacity
        self.__budget = budget
        self.__database = Database(name + ".db")

    def get_name(self):
        return self.__name

    def get_capacity(self):
        return self.__capacity

    def get_animals(self):
        return self.__animals

    def accommodate_animal(self, species, age, name, gender, weight):
        if self.__capacity <= len(self.__animals):
            return False
        new_animal = Animal(species, age, name, gender, weight)
        self.__animals.append(new_animal)
        self.__database.insert_animal(new_animal)
        return True

    def remove_animal(self, species, name):
        for animal in self.__animals:
            if animal.get_species() == species and animal.get_name() == name:
                self.__animals.remove(animal)
                break

    def move_animal(self, species, name):
        self.remove_animal(species, name)

    def see_animals(self):
        list = []
        for animal in self.__animals:
            list.append(str(animal))
        list = '\n'.join(list)
        return list

    def daily_incomes(self):
        return 60 * len(self.__animals)

    def daily_expenses(self):
        money = 0
        for animal in self.__animals:
            animal_type = self.__database.get_food_type
            (animal.get_species())
            ""
            food_weight_ratio = self.__database.get_food_weight_ratio
            (animal.get_species())
            if animal_type == "carnivore":
                money += __MEAT_COST * animal.feed(food_weight_ratio)
            else:
                money += __GRASS_COST * animal.feed(food_weight_ratio)
        return money

    def random_gender(self):
        gender = randint(0, 1)
        if gender == 0:
            gender = 'male'
        else:
            gender = 'female'
        return gender

    def generate_name(self, species, name, gender):
        name = self.__database.get_male_name(species)
        if gender == 'female':
            return name + 'ka'
        else:
            return name + str(randint(1, 100))

    def born_animal(self, species, name):
        self.__database.set_last_breed(species, name, 0)
        weight = self.__database.get_newborn_weight(species)
        gender = self.random_gender()
        name = self.generate_name(species, name, gender)
        new_animal = Animal(species, 1, name, gender, weight)
        self.__animals.append(new_animal)
        self.database.insert_animal(new_animal)

        if len(self.__animals) > self.__capacity:
            return False
        return True

    def will_it_mate(self, species, name):
        breeding_period =\
            __BREEDING_PERIOD + self.database.get_gestation(species)
        has_male = self.database.has_male(species)
        ready_to_breed =\
            breeding_period <= self.database.get_last_breed(species, name)

        return has_male and ready_to_breed
