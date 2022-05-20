# Agui Navarro
# CS 457 Spring 2022
# Python 3.7.3+

import os
from posixpath import split

loop = True
query = None
storedQuery = None
currentDB = None
currentTable = None

currentCommand = None
setVariable = None
getVariable = None

keyIndexList = []

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
    db = removeCommand("CREATE DATABASE ")
    db = db[:-1] # ensures database name is solely database and no other characters
    if checkExistsDB(db) == False:
        os.system(f"mkdir {db}")
        print(f"Database {db} created.")
    else:
        print(f"!Failed to create database {db} because it already exists.")

# Delete database
def dropDatabase(query):
    db = removeCommand("DROP DATABASE ")
    db = db[:-1] # ensures database name is solely database and no other characters
    if checkExistsDB(db) == True:
        os.system(f"rm -r {db}")
        print(f"Database {db} deleted.")
    else:
        print(f"!Failed to delete {db} because it does not exist.")
# Select database to use
def use(query):
    currentDB = removeCommand("USE ")
    currentDB = currentDB[:-1] # ensures database name is solely database and no other characters
    if checkExistsDB(currentDB) == True:
        print(f"Using database {currentDB}")
        return currentDB
    else:
        print(f"!Failed to use {currentDB} because it does not exist.")

# Create table
def createTable(query):
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
            first = True
            for i in tableAttributes:
                if first == True:
                    f.write(f"{i}") # no vertical bar for first element in tableAttributes
                    first = False
                else:
                    f.write(f"|{i}")
            f.close()
            print(f"Table {tableName} created.")
        else:
            print(f"!Failed to create table {tableName} because it already exists.")
    else:
        print("Please choose a database to use.")

def dropTable(query):
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

def alterTable(query):
    alterInput = removeCommand("ALTER TABLE ")
    split = alterInput.split()
    tableName = split[0]
    alterCommand = split[1]
    alterRest = alterInput.replace(tableName, "")
    alterRest = alterRest.replace(alterCommand, "")
    alterRest = alterRest[2:-1] # ensures attributes are solely attributes and no other characters

    if (currentDB):
        if checkExistsTable(tableName):
            f = open(f"{currentDB}/{tableName}.txt", "a")
            f.write(f"|{alterRest}") # table is written in form of string
            f.close()
            print(f"Table {tableName} modified.")
        else:
            print(f"!Failed to modify {tableName} because it does not exist.")
    else:
        print("Please choose a database to use.")

def select(query):
    if "*" in query:
        tableName = removeCommand("select * from ")
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
    else:
        rest = removeCommand("select ")
        splitRest = rest.split(", ")
        splitRest[1] = splitRest[1][:-2]

        if (currentDB):
            if checkExistsTable(currentTable):
                with open(f"{currentDB}/{currentTable}.txt", "r") as f:
                    firstLine = f.readline()
                    types = firstLine.split("|")
                    types[len(types) - 1] = types[len(types) - 1].strip()
                    typesDict = {}
                    for i in range(len(types)):
                        splitElement = types[i].split()
                        typesDict[splitElement[0]] = i
                    
                    keyIndexList = []
                    for key in typesDict:
                        for i in splitRest:
                            if i == key:
                                keyIndexList.append(typesDict[key])
                    return keyIndexList
            else:
                print(f"!Failed to modify {tableName} because it does not exist.")
        else:
            print("Please choose a database to use.")

def selectWhere(query): 
    rest = removeCommand("where ")
    


        

def insert(query):
    tableInput = removeCommand("insert into ")
    split = tableInput.split()
    tableName = split[0]
    tableRest = tableInput.replace(tableName, "")
    tableAttributes = tableRest[8:-2] # ensures attributes are solely attributes and no other characters
    tableAttributes = tableAttributes.split()
    for i in range(len(tableAttributes)):
        tableAttributes[i].strip()
        string = False
        last = False

        if i == (len(tableAttributes) - 1):
            last = True
        if tableAttributes[i][0] == "'":
            string = True

        if string == False and last == False:
            tableAttributes[i] = tableAttributes[i][:-1]
        if string == True:
            tableAttributes[i] = tableAttributes[i][1:-2]
    
    if (currentDB):
        if checkExistsTable(tableName):
            f = open(f"{currentDB}/{tableName}.txt", "a")
            f.write(f"\n")
            first = True
            for i in tableAttributes:
                if first == True:
                    f.write(f"{i}") # no vertical bar for first element in tableAttributes
                    first = False
                else:
                    f.write(f"|{i}")
            f.close()
            print("1 new record inserted.")
        else:
            print(f"!Failed to query table {tableName} because it does not exist.")
    else:
        print("Please choose a database to use.")

def update(query, set, get):

    updateCount = 0

    splitSet = set.split(" = ")
    if splitSet[1][0] == "'":
        splitSet[1] = splitSet[1][1:-1]

    splitGet = get.split(" = ")
    if splitGet[1][0] == "'":
        splitGet[1] = splitGet[1][1:-1]

    if (currentDB):
        if checkExistsTable(currentTable):
            with open(f"{currentDB}/{currentTable}.txt", "r") as f:
                firstLine = f.readline()
                types = firstLine.split("|")
                print(types)
                types[len(types) - 1] = types[len(types) - 1].strip()
                print(types)
                typesDict = {}
                for i in range(len(types)):
                    splitElement = types[i].split()
                    typesDict[splitElement[0]] = i

                print(typesDict)

                setElementIndex = None
                getElementIndex = None
                for key in typesDict:
                    if splitSet[0] == key:
                        setElementIndex = typesDict[key]
                for key in typesDict:
                    if splitGet[0] == key:
                        getElementIndex = typesDict[key]

                EOF = False
                changedElements = None
                linesToEdit = []
                newLines = []
                while (EOF == False):
                    line = f.readline()
                    line = line.strip()
                    if not line:
                        EOF = True
                    else:
                        elements = line.split("|")
                        elements[len(elements) - 1] = elements[len(elements) - 1].strip()
                        if elements[getElementIndex] == splitGet[1]:
                            elements[setElementIndex] = splitSet[1]
                            changedElements = elements
                            linesToEdit.append(line)

                            first = True
                            temp = ""
                            for i in changedElements:
                                if first == True:
                                    temp += i
                                    first = False
                                else:
                                    temp += "|"
                                    temp += i
                            newLines.append(temp)

            with open(f"{currentDB}/{currentTable}.txt", "r") as f:
                allLines = f.readlines()

            counter = 0
            with open(f"{currentDB}/{currentTable}.txt", "w") as f:
                for line in allLines:
                    if line.strip("\n") == linesToEdit[counter]:
                        f.write(newLines[counter])
                        f.write("\n")
                        counter += 1
                        updateCount += 1
                    else:
                        f.write(line)
            if updateCount == 1:
                print(f"{updateCount} record modified.")
            if updateCount > 1:
                print(f"{updateCount} records modified.")
        else:
            print(f"!Failed to query table {currentTable} because it does not exist.")
    else:
        print("Please choose a database to use.")

def delete(query, get):

    operator = None
    deleteCount = 0

    if get.find("=") != -1:
        operator = "="
        splitGet = get.split(" = ")
        if splitGet[1][0] == "'":
            splitGet[1] = splitGet[1][1:-1]

    if get.find(">") != -1:
        operator = ">"
        splitGet = get.split(" > ")


    if (currentDB):
        if checkExistsTable(currentTable):
            with open(f"{currentDB}/{currentTable}.txt", "r") as f:
                firstLine = f.readline()
                types = firstLine.split("|")
                types[len(types) - 1] = types[len(types) - 1].strip()
                typesDict = {}
                for i in range(len(types)):
                    splitElement = types[i].split()
                    typesDict[splitElement[0]] = i

                getElementIndex = None
                for key in typesDict:
                    if splitGet[0] == key:
                        getElementIndex = typesDict[key]

                EOF = False
                linesToEdit = []
                while (EOF == False):
                    line = f.readline()
                    line = line.strip()
                    if not line:
                        EOF = True
                    else:
                        elements = line.split("|")
                        elements[len(elements) - 1] = elements[len(elements) - 1].strip()

                        if elements[getElementIndex] == splitGet[1]:
                            linesToEdit.append(line)
                        if operator == ">":
                            left = float(elements[getElementIndex])
                            right = float(splitGet[1])
                            if left > right:
                                linesToEdit.append(line)
                            
            with open(f"{currentDB}/{currentTable}.txt", "r") as f:
                allLines = f.readlines()

            counter = 0
            with open(f"{currentDB}/{currentTable}.txt", "w") as f:
                for line in allLines:
                    line = line[:-1]
                    if line == linesToEdit[counter]:
                        counter += 1
                        deleteCount += 1
                    else: 
                        f.write(line)
                        f.write("\n")
            if deleteCount == 1:
                print(f"{deleteCount} record deleted.")
            if deleteCount > 1:
                print(f"{deleteCount} records deleted.")
        else:
            print(f"!Failed to query table {currentTable} because it does not exist.")
    else:
        print("Please choose a database to use.")

def set(query):
    noCommand = removeCommand("set ")
    noCommand = noCommand[:-2]
    return noCommand

def get(query):
    noCommand = removeCommand("where ")
    noCommand = noCommand[:-1]
    return noCommand

def fromm(query):
    noCommand = removeCommand("from ")
    noCommand = noCommand[:-1]
    noCommand.replace("p", "P", 1)
    return noCommand

# main loop
while (loop == True):
    query = input("") # make it sql-like
    if (';' not in query and query != ".EXIT"):
        print("")
    if (".exit" in query):
        quit()

    if "CREATE DATABASE" in query:
        createDatabase(query)

    if "DROP DATABASE" in query:
        dropDatabase(query)

    if "USE" in query:
        currentDB = use(query)

    if "CREATE TABLE" in query:
        createTable(query)

    if "DROP TABLE" in query:
        dropTable(query)
        
    if "ALTER TABLE" in query:
        alterTable(query)

    if "select" in query:
        keyIndexList = select(query)
    
    if "insert into" in query:
        insert(query)

    if "update" in query:
        storedQuery = query
        tableName = removeCommand("update ")
        tableName = tableName[:-2] # ensures table name is solely table name and no other characters
        currentTable = tableName
        currentCommand = "update"

    if "delete from" in query:
        storedQuery = query
        tableName = removeCommand("delete from ")
        tableName = tableName[:-2] # ensures table name is solely table name and no other characters
        tableName = tableName.replace("p", "P", 1)
        currentTable = tableName
        currentCommand = "delete from"

    if "set" in query:
        setVariable = set(query)

    if "where" in query:
        getVariable = get(query)
        if currentCommand == "update":
            update(storedQuery, setVariable, getVariable)
        if currentCommand == "delete from":
            delete(query, getVariable)
            currentCommand = ""
        else:
            selectWhere(query)



    
    if "from" in query:
        fromVariable = fromm(query)
        




        


