import sqlite3

# Connect to the database
connection = sqlite3.connect('movies.db')
cursor = connection.cursor()

# Create table (if it does not already exist)
cursor.execute("CREATE TABLE IF NOT EXISTS service (serviceId INTEGER PRIMARY KEY AUTOINCREMENT, serviceName TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS movie (movieId INTEGER PRIMARY KEY AUTOINCREMENT, movieName TEXT, movieStudio TEXT, movieYear YEAR, serviceId INTEGER)")

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
while choice != "8":
    print("1) Display Movies")
    print("2) Display Streaming Locations")
    print("3) Add Streaming Service")
    print("4) Add Movie")
    print("5) Display Where To Watch Movies")
    print("6) Delete Movie")
    print("7) Modify Movie Name")
    print("8) Quit")
    choice = input("> ")
    print()
    if choice == "1":
        # Display Movies
        cursor.execute("SELECT movieId, movieName, movieStudio, movieYear FROM movie")
        print("{:>10}  {:>10}  {:>10} {:>10}".format("movieId", "movieName", "movieStudio", "movieYear"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}  {:>10} {:>10}".format(record[0], record[1], record[2], record[3]))
    elif choice == "2":
        # Display streaming services that the movies are on
        cursor.execute("SELECT * FROM service ORDER BY serviceName")
        print("{:>10}  {:>10}".format("serviceId", "serviceName"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}".format(record[0], record[1]))
    elif choice == "3":
        # Add New Service
        try:
            serviceId = None            
            serviceName = input("serviceName: ")
            values = (serviceId, serviceName)
            cursor.execute("INSERT INTO service VALUES (?, ?)", values)
            connection.commit()
        except ValueError:
            print("Invalid name!")
    elif choice == "4": 
        # Add New Movie
        movieId = None
        movieName = input("movieName: ")
        movieStudio = input("movieStudio: ")
        movieYear = (input("movieYear: "))
        serviceId = (input("Service Id: "))
        values = (movieId, movieName, movieStudio, movieYear, serviceId)
        cursor.execute("INSERT INTO movie VALUES (?,?,?,?,?)", values)
        connection.commit()
    elif choice == "5": 
        # Perform Join to view which movies are on which services
        cursor.execute("SELECT movieName, serviceName FROM movie INNER JOIN service ON movie.serviceId=service.serviceId")
        print("{:>10}  {:>10}".format("movieName", "serviceName"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}".format(record[0], record[1]))
    elif choice == "6":
        # Delete movie
        movieName = get_name(cursor)
        if movieName == None:
            continue
        values = (movieName, )
        cursor.execute("DELETE FROM movie WHERE movieName = ?", values)
        connection.commit()       
    elif choice == "7":
        # Update Movie Name
        try:
            movieName = input("Name: ")
            movieId = (input("MovieId: "))
            values = (movieName, movieId) # Make sure order is correct
            cursor.execute("UPDATE movie SET movieName = ? WHERE movieId = ?", values)
            connection.commit()
            if cursor.rowcount == 0:
                print("Invalid name!")
        except ValueError:
            print("Invalid id!")

    print()

# Close the database connection before exiting
connection.close()