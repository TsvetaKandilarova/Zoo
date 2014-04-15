from animals import Animal
from zoo import Zoo
from database import Database
import sqlite3


#Global arguments
__commands = ["see_animals",
              "accommodate",
              "move_to_habitat",
              "simulate",
              "exit"
              ]
# Zoo(name, capacity, budget)
__zoo = Zoo("Sofia_zoo", 50, 3000)
__unknown_command_msg = """
Unknown command!

Try one of the following:
    - see_animals
    - accommodate <species> <age> <name> <gender> <weight>
    - move_to_habitat <species> <name>
    - simulate
    - exit
"""


""" if there are already animals in the zoo table -> we should update
the zoo_class on loading the application"""
# def update_zoo_class(self, zoo_class):
#     db = Database("Sofia_zoo.db")


def is_zoo_database(database_name):
    zoo_conn = sqlite3.connect(database_name)
    cursor = zoo_conn.cursor()
    animals_from_db = cursor.execute('''SELECT * FROM zoo''').fetchall()
    if animals_from_db == []:
        return False
    else:
        return True


def fill_with_animals(database):
    db = database
    # Animal(species, age, name, gender, weight)
    lion1 = Animal("lion", 10, "Svetla", "female", 160)
    lion2 = Animal("lion", 6, "Gosho", "male", 190)
    tiger1 = Animal("tiger", 12, "Tsveta", "female", 200)
    tiger2 = Animal("tiger", 10, "Joro", "male", 230)
    red_panda1 = Animal("red_panda", 3, "Lubka", "female", 4)
    red_panda2 = Animal("red_panda", 4, "Lucho", "male", 4.5)
    hippo1 = Animal("hippo", 22, "Anastasiya", "female", 1200)
    hippo2 = Animal("hippo", 15, "Zlatin", "male", 1300)
    goat1 = Animal("goat", 2, "Veska", "female", 40)
    goat2 = Animal("goat", 4, "Niki", "male", 50)
    db.insert_animal(lion1)
    db.insert_animal(lion2)
    db.insert_animal(tiger1)
    db.insert_animal(tiger2)
    db.insert_animal(red_panda1)
    db.insert_animal(red_panda2)
    db.insert_animal(hippo1)
    db.insert_animal(hippo2)
    db.insert_animal(goat1)
    db.insert_animal(goat2)


def update_from_database(database_name):
    zoo = __zoo
    zoo.__animals = []
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    animals_from_db = cursor.execute('''SELECT * FROM zoo''').fetchall()
    for animal in animals_from_db:
        zoo.__animals.append(animal)
    return zoo


# <name> : <species>, <age>, <weight>
def see_animals():
    zoo = __zoo
    formated_list = []

    # animal_objects look like this: (id, species, age, name, gender, weight)
    for animal in zoo.__animals:
        animal_string = animal[3] + "\t   -   " + animal[1] + ", age: " + str(animal[2]) + " years, weight: " + str(animal[5]) + " kg"
        formated_list.append(animal_string)
    output_string = '\n'.join(formated_list)
    return output_string


# removes an animal from the zoo and returns it to it's natural habitat
def move_to_habitat(species, name):
    db = __zoo.get_database()
    print(db.name)
    db.remove_animal(species, name)
    __zoo.remove_animal(species, name)


# grow in weight, age, update table, update
def grow_all_animals(time_months):
    __zoo = update_from_database("Sofia_zoo.db")
    zoo = __zoo
    db = __zoo.get_database()

    for this_animal in zoo.__animals:
        animal = Animal(this_animal[1], this_animal[2], this_animal[3], this_animal[4], this_animal[5])
        animal.grow(time_months)

        species = animal.get_species()
        name = animal.get_name()
        new_age = animal.get_age()
        new_weight = animal.get_weight()

        db.set_age(species, name, new_age)
        db.set_weight(species, name, new_weight)


def check_dead_animals(time_months):
    __zoo = update_from_database("Sofia_zoo.db")
    zoo = __zoo
    db = __zoo.get_database()
    dead_list = []

    for this_animal in zoo.__animals:
        animal = Animal(this_animal[1], this_animal[2], this_animal[3], this_animal[4], this_animal[5])
        if animal.die(0) is True:
            dead_list.append(animal)

            species = animal.get_species()
            name = animal.get_name()
            db.remove_animal(species, name)
    return dead_list


def check_budget(time_months):
    # __zoo = update_from_database("Sofia_zoo.db")
    # return __zoo
    pass


def check_born_animals(time_months):
    # __zoo = update_from_database("Sofia_zoo.db")
    # return __zoo
    pass


# period id in months only for now!!!
def simulate(interval_of_time, period):
    if interval_of_time == "months":
        time_months = period
    elif interval_of_time == "weeks":
        time_months = period / 4
    elif interval_of_time == "days":
        time_months = period / 30

    grow_all_animals(time_months)
    dead_list = check_dead_animals(time_months)
    check_budget(time_months)
    check_born_animals(time_months)

    __zoo = update_from_database("Sofia_zoo.db")
    print(see_animals())
    print(dead_list)


def run_interface():
    __zoo = update_from_database("Sofia_zoo.db")
    while True:
        command = input("Enter command>")
        arguments = command.split()

        if (arguments[0] not in __commands):
            print(__unknown_command_msg)

        if (arguments[0] == "see_animals"):
            print(see_animals())

        if (arguments[0] == "accommodate"):
            species = arguments[1]
            age = arguments[2]
            name = arguments[3]
            gender = arguments[4]
            weight = arguments[5]
            adding_animal = __zoo.accommodate_animal(species, age, name, gender, weight)
            if adding_animal is False:
                print("Not enough space in the zoo")
            else:
                print(name + " has been accommodated in the zoo.")
                __zoo = update_from_database("Sofia_zoo.db")

        if (arguments[0] == "move_to_habitat"):
            species = arguments[1]
            name = arguments[2]
            move_to_habitat(species, name)
            print(name + " has been moved to habitat.")
            __zoo = update_from_database("Sofia_zoo.db")

        # gives an error in simulate !!!
        if (arguments[0] == "simulate"):
            # interval_of_time = arguments[1]
            # period = int(arguments[2])
            # simulate(interval_of_time, period)
            pass

        if (arguments[0] == "exit"):
            break


def main():
    if is_zoo_database("Sofia_zoo.db") is False:
        db = Database("Sofia_zoo.db")
        print("Creating Sofia Zoo")
        fill_with_animals(db)

    run_interface()


if __name__ == '__main__':
    main()
