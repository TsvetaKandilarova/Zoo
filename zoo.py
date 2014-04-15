from animals import Animal
from database import Database
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

    def get_database(self):
        return self.__database

    def accommodate_animal(self, species, age, name, gender, weight):
        if self.__capacity <= len(self.__animals):
            return False
        new_animal = Animal(species, age, name, gender, weight)
        self.__animals.append(new_animal)
        self.__database.insert_animal(new_animal)
        return True

    def see_animals(self):
        list = []
        for animal in self.__animals:
            list.append(str(animal))
        list = '\n'.join(list)
        return list

    def remove_animal(self, species, name):
        for animal in self.__animals:
            if animal.get_species() == species and animal.get_name() == name:
                self.__animals.remove(animal)
                break

    def move_animal(self, species, name):
        self.remove_animal(species, name)

    def daily_incomes(self):
        return 60 * len(self.__animals)

    def daily_expenses(self):
        money = 0
        for animal in self.__animals:
            animal_type = self.__database.get_food_type(animal.get_species())
            food_weight_ratio = self.__database.get_food_weight_ratio(animal.get_species())
            if animal_type == "carnivore":
                money += 4 * animal.feed(food_weight_ratio)
            else:
                money += 2 * animal.feed(food_weight_ratio)
        return money

    def flip_a_coin(self):
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
        gender = self.flip_a_coin()
        name = self.generate_name(species, name, gender)
        new_animal = Animal(species, 1, name, gender, weight)
        self.__animals.append(new_animal)
        self.__database.insert_animal(new_animal)

        if len(self.__animals) > self.__capacity:
            return False
        return True

    def ready_to_give_birth(self, species, name):
        breeding_period =\
            6 + self.database.get_gestation(species)
        if self.database.has_male(species):
            if breeding_period <= self.database.get_last_breed(species, name):
                return True
        return False
