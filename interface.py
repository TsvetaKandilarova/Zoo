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


def handle_see_animals_command(zoo):
    output = zoo.see_animals()
    print(output)


# removes an animal from the zoo and returns it to it's natural habitat
def handle_move_to_habitat_command(species, name, zoo):
    db = zoo.get_database()
    db.remove_animal(species, name)
    print(name + " has been moved to habitat.")
    zoo.remove_animal(species, name)


# grow in weight, age, update table, update
def grow_all_animals(time_months, zoo):
    zoo.__animals = zoo.update_animals_from_database()
    db = zoo.get_database()

    for this_animal in zoo.__animals:
        animal = Animal(this_animal[1], this_animal[2], this_animal[3], this_animal[4], this_animal[5])

        species = animal.get_species()
        print(species)
        name = animal.get_name()

        animal.grow(time_months)

        new_age = animal.get_age()
        new_weight = animal.get_weight()

        db.set_age(species, name, new_age)
        db.set_weight(species, name, new_weight)


def check_dead_animals(time_months, zoo):
    zoo.__animals = zoo.update_animals_from_database()
    db = zoo.get_database()
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
    pass


def check_born_animals(time_months):
    pass


def handle_accommodate_command(arguments, zoo):
    species = arguments[1]
    if species == "red":
        species += " " + arguments[2]
        age = arguments[3]
        name = arguments[4]
        gender = arguments[5]
        weight = arguments[6]
    else:
        age = arguments[2]
        name = arguments[3]
        gender = arguments[4]
        weight = arguments[5]

    adding_animal = zoo.accommodate_animal(species, age, name, gender, weight)
    if adding_animal is False:
        print("Not enough space in the zoo")
    else:
        print(name + " has been accommodated in the zoo.")


# period id in months only for now!!!
def handle_simulate_command(interval_of_time, period, zoo):
    if interval_of_time == "months":
        time_months = period
    elif interval_of_time == "weeks":
        time_months = period / 4
    elif interval_of_time == "days":
        time_months = period / 30

    grow_all_animals(time_months, zoo)
    dead_list = check_dead_animals(time_months, zoo)
    check_budget(time_months)
    check_born_animals(time_months)

    zoo.__animals = zoo.update_animals_from_database()
    print(zoo.see_animals())
    print(dead_list)


def run_interface(zoo):
    zoo.__animals = zoo.update_animals_from_database()
    while True:
        command = input("Enter command>")
        arguments = command.split()

        if (arguments[0] not in __commands):
            print(__unknown_command_msg)

        if (arguments[0] == "see_animals"):
            handle_see_animals_command(zoo)

        if (arguments[0] == "accommodate"):
            handle_accommodate_command(arguments, zoo)

        if (arguments[0] == "move_to_habitat"):
            species = arguments[1]
            if species == "red":
                species += " " + arguments[2]
                name = arguments[3]
            else:
                name = arguments[2]

            handle_move_to_habitat_command(species, name, zoo)

        if (arguments[0] == "simulate"):
            interval_of_time = arguments[1]
            period = int(arguments[2])
            handle_simulate_command(interval_of_time, period, zoo)

        if (arguments[0] == "exit"):
            break


def main():
    # Zoo(name, capacity, budget)
    zoo = Zoo("Sofia_zoo", 50, 3000)
    if is_zoo_database("Sofia_zoo.db") is False:
        db = Database("Sofia_zoo.db")
        print("Creating Sofia Zoo")
        db.initial_fill_with_animals()

    run_interface(zoo)


if __name__ == '__main__':
    main()
