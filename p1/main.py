# Agui Navarro
# CS 457 Spring 2022
# Python 3.7.3+

import os
import prettytable # Please install prettytable for program to work

loop = True
query = None
currentDB = None
currentPrettyTable = None

# First removes ;
# Then converts line into db or table name
def removeCommand(command):
    input = query.replace(";", "")
    input = input.replace(command, "")
    return input

# Checks if directory with db name exists
def checkExistsDB(database):
    if os.path.isdir(database):
        return True
    else:
        return False

# Checks if file with table name exists
def checkExistsTable(table):
    if os.path.isfile(currentDB + "/" + table + ".txt"):
        return True
    else:
        return False

# Create database
def createDatabase(query):
    print(query)
    db = removeCommand("CREATE DATABASE ")
    db = db[:-1] # ensures database name is solely database and no other characters
    if checkExistsDB(db) == False:
        os.system(f"mkdir {db}")
        print(f"Database {db} created.")
    else:
        print(f"!Failed to create database {db} because it already exists.")
    print()

# Delete database
def dropDatabase(query):
    print(query)
    db = removeCommand("DROP DATABASE ")
    db = db[:-1] # ensures database name is solely database and no other characters
    if checkExistsDB(db) == True:
        os.system(f"rm -r {db}")
        print(f"Database {db} deleted.")
    else:
        print(f"!Failed to delete {db} because it does not exist.")
    print()

# Select database to use
def use(query):
    print(query)
    currentDB = removeCommand("USE ")
    currentDB = currentDB[:-1] # ensures database name is solely database and no other characters
    if checkExistsDB(currentDB) == True:
        print(f"Using database {currentDB}")
        print()
        return currentDB
    else:
        print(f"!Failed to use {currentDB} because it does not exist.")
        print()

# Create table
def createTable(query):
    print(query)
    tableInput = removeCommand("CREATE TABLE ")
    split = tableInput.split()
    tableName = split[0]
    tableRest = tableInput.replace(tableName, "")
    tableAttributes = tableRest[2:-2] # ensures attributes are solely attributes and no other characters
    tableAttributes = tableAttributes.split(", ")

    if (currentDB):
        if checkExistsTable(tableName) == False:
            os.system(f"touch {currentDB}/{tableName}.txt")
            fileName = currentDB + "/" + tableName + ".txt"
            f = open(fileName, "w")
            table = prettytable.PrettyTable(["Attributes"]) # creates pretty table
            for i in tableAttributes:
                table.add_row([i]) # adds attribute to pretty table
            f.write(str(table)) # writes in form of string
            f.close()
            print(f"Table {tableName} created.")
            print()
            return table
        else:
            print(f"!Failed to create table {tableName} because it already exists.")
            print()
    else:
        print("Please choose a database to use.")
        print()

def dropTable(query):
    print(query)
    tableName = removeCommand("DROP TABLE ")
    tableName = tableName[:-1] # ensures table name is solely table name and no other characters
    if (currentDB):
        if checkExistsTable(tableName):
            os.system(f"rm {currentDB}/{tableName}.txt")
            print(f"Table {tableName} deleted.")
        else:
            print(f"!Failed to delete {tableName} because it does not exist.")
    else:
        print("Please choose a database to use.")
    print()

def alterTable(query):
    print(query)
    alterInput = removeCommand("ALTER TABLE ")
    split = alterInput.split()
    tableName = split[0]
    alterCommand = split[1]
    alterRest = alterInput.replace(tableName, "")
    alterRest = alterRest.replace(alterCommand, "")
    alterRest = alterRest[2:-1] # ensures attributes are solely attributes and no other characters

    if (currentDB):
        if checkExistsTable(tableName):
            fileName = currentDB + "/" + tableName + ".txt"
            f = open(fileName, "w")
            f.truncate() # removes contents of file
            table = currentPrettyTable
            table.add_row([alterRest]) # new attribute is added to imported prettytable
            f.write(str(table)) # table is written in form of string
            f.close()
            print(f"Table {tableName} modified.")
            print()
            return table
        else:
            print(f"!Failed to modify {tableName} because it does not exist.")
            print()
    else:
        print("Please choose a database to use.")
        print()

def select(query):
    print(query)
    tableName = removeCommand("SELECT * FROM ")
    tableName = tableName[:-1] # ensures table name is solely table name and no other characters
    if (currentDB):
        if checkExistsTable(tableName):
            f = open(f"{currentDB}/{tableName}.txt", "r")
            print(f.read())
            f.close()
        else:
            print(f"!Failed to query table {tableName} because it does not exist.")
    else:
        print("Please choose a database to use.")
    print()

# main loop
while (loop == True):
    query = input("sql> ") # make it sql-like
    if (';' not in query and query != ".EXIT"):
        print("")
    if (".EXIT" in query):
        quit()

    if "CREATE DATABASE" in query:
        createDatabase(query)

    if "DROP DATABASE" in query:
        dropDatabase(query)

    if "USE" in query:
        currentDB = use(query)

    if "CREATE TABLE" in query:
        currentPrettyTable = createTable(query)

    if "DROP TABLE" in query:
        dropTable(query)
        
    if "ALTER TABLE" in query:
        currentPrettyTable = alterTable(query)

    if "SELECT *" in query:
        select(query)




        


