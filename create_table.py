import sqlite3


def create_tables(cursor):
    cursor.execute('''CREATE TABLE animal_types (id INTEGER PRIMARY KEY,\
     species text, life_expectancy int, food_type text, gestation\
     int, newborn_weight real, average_weight int, weight_age_ratio \
     real, food_weight_ratio real)''')

    query = "INSERT INTO animal_types(species, life_expectancy, food_type,\
     gestation, newborn_weight, average_weight, weight_age_ratio, \
     food_weight_ratio) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, ("lion", 15, "carnivore", 3, 2.0, 200, 7.5, 0.035))
    cursor.execute(query, ('tiger', 20, "carnivore", 4, 1.0, 250, 12.0, 0.06))


def main():
    conn = sqlite3.connect('animal_types.db')
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()
