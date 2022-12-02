import sqlite3

# Connect to the database
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()

# Create table (if it does not already exist)
cursor.execute("CREATE TABLE IF NOT EXISTS movie (movieId int NOT NULL AUTO_INCREMENT, movieName TEXT, movieStudio TEXT, movieYear YEAR)")
cursor.execute("CREATE TABLE IF NOT EXISTS service (serviceId int NOT NULL AUTO_INCREMENT, serviceName TEXT)")

def get_name(cursor):
    cursor.execute("SELECT name FROM movies")
    results = cursor.fetchall()
    if len(results) == 0:
        print("No movies in database")
        return None
    for i in range(len(results)):
        print(f"{i+1} - {results[i][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Name ID: "))
    return results[choice-1][0]


choice = None
while choice != "5":
    print("1) Display Movies")
    print("2) Display Streaming Locations")
    print("3) Add Movie")
    print("4) Add Streaming Service")
    print("3) Update Employee Pay")
    print("4) Delete Movie")
    print("5) Quit")
    choice = input("> ")
    print()
    if choice == "1":
        # Display Movies
        cursor.execute("SELECT * FROM movie ORDER BY movieYear DESC")
        print("{:>10}  {:>10}  {:>10}".format("movieId", "movieName", "movieStudio", "movieYear"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}  {:>10}".format(record[0], record[1], record[2], record[3], record[4]))
    elif choice == "2":
        # Display streaming services that the movies are on
        cursor.execute("SELECT * FROM service ORDER BY serviceName")
    elif choice == "3":
        # Add New Employee
        try:
            name = input("Name: ")
            title = input("Title: ")
            pay = float(input("Pay: "))
            values = (name, title, pay)
            cursor.execute("INSERT INTO employees VALUES (?,?,?)", values)
            connection.commit()
        except ValueError:
            print("Invalid pay!")
    elif choice == "4":
        # Update Employee Pay
        try:
            name = input("Name: ")
            pay = float(input("Pay: "))
            values = (pay, name) # Make sure order is correct
            cursor.execute("UPDATE employees SET pay = ? WHERE name = ?", values)
            connection.commit()
            if cursor.rowcount == 0:
                print("Invalid name!")
        except ValueError:
            print("Invalid pay!")
    elif choice == "5":
        # Delete employee
        name = get_name(cursor)
        if name == None:
            continue
        values = (name, )
        cursor.execute("DELETE FROM employees WHERE name = ?", values)
        connection.commit()
    print()

# Close the database connection before exiting
connection.close()