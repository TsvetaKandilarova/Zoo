import sqlite3


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

    def update_weight(self, period):
        self.conn = sqlite3.connect('animals.db')
        cursor = self.conn.cursor()
        query = "SELECT weight_age_ratio FROM animals WHERE \
        species = ?"
        result = cursor.execute(query, (self.__species, )).fetchall()[0][0]
        new_weight = self.get_weight() + result * period
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
        new_age = self.get_age() + period
        self.__age = new_age

    def eat(self):
        pass

    def die(self):
        pass
