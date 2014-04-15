from animals import Animal
import sqlite3


#Global arguments
commands = ["see_animals",
            "accommodate",
            "move_to_habitat",
            "simulate",
            "finish"
            ]


# UNDER DEVELOPMENT
# <name> : <species>, <age>, <weight>
def see_animals(database):
    animals_listed = []
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    query = "SELECT name, species, age, weight FROM zoo"
    # animals_listed = cursor.execute(query, ).fetchall()
    return animals_listed


# adds an animal to the zoo
def accommodate(species, name, age, weight):
    pass


# removes an animal from the zoo and returns it to it's natural habitat
def move_to_habitat(species, name):
    pass


def simulate(interval_of_time, period):
    pass


def run_interface():
    while True:
        command = input("Enter command>")
        arguments = command.split()
        # the database is test_interface.db
        database = "test_interface"

        if (arguments[0] not in commands):
            print("\nUnknown command!\nTry one of the following:\
                \n\nsee_animals\naccommodate\nmove_to_habitat\
                \nsimulate")

        if (arguments[0] == "see_animals"):
            see_animals(database)

        if (arguments[0] == "accommodate"):
            # accommodate(species, name, age, weight)
            pass

        if (arguments[0] == "move_to_habitat"):
            # move_to_habitat(species, name)
            pass

        if (arguments[0] == "simulate"):
            # simulate(interval_of_time, period)
            pass

        if (arguments[0] == "finish"):
            break


def main():
    run_interface()


if __name__ == '__main__':
    main()
