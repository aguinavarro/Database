# Agui Navarro
# CS 457 Spring 2022
# Python 3.7.3+

import os
import shutil

from itertools import count
from posixpath import split

loop = True
query = None

storedQuery = None
storedQueryFrom = None

currentDB = None
currentTable = None

currentCommand = None
setVariable = None
getVariable = None

keyIndexList = []

lock1 = False
lock2 = False
lock3 = False

savedMessage = None

# First removes ;
# Then converts line into db or table name
def removeCommand(command):
    input = query.replace(";", "")
    input = input.replace(command, "")
    return input

def removeTable(command, table):
    new = command.replace(table, "")
    return new

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
    tableInput = removeCommand("create table ")
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

def select1(fromVariable, whereOnVariable):
    if ("--Cstruct" in fromVariable):
        return

    fromVariable = fromVariable.strip()
    whereOnVariable = whereOnVariable.strip()

    join = None
    fromSplit = None
    
    if "," in fromVariable:
        fromSplit = fromVariable.split(", ")
        join = "innerjoin"
    elif "inner join" in fromVariable:
        fromSplit = fromVariable.split(" inner join ")
        join = "innerjoin"
    elif "left outer join" in fromVariable:
        fromSplit = fromVariable.split(" left outer join ")
        join = "leftouterjoin"
    else:
        print("Invalid from command")

    whereOnSplit = whereOnVariable.split(" = ")

    #print(f"x{fromSplit}x")
    #print(f"x{whereOnSplit}x")

    tableDict = {}
    for i in range(len(fromSplit)):
        splitElement = fromSplit[i].split()
        tableDict[splitElement[1]] = splitElement[0]

    string1 = None
    string2 = None
    count = 0

    for key in tableDict:
        if (currentDB):
            if checkExistsTable(tableDict[key]):
                f = open(f"{currentDB}/{tableDict[key]}.txt", "r")
                if count == 0:
                    string1 = f.read()
                if count == 1:
                    string2 = f.read()
                f.close()
            else:
                print(f"!Failed to query table {tableDict[key]} because it does not exist.")
        else:
            print("Please choose a database to use.")
        count += 1

    list1 = None
    list2 = None

    for i in range(2):
        if i == 0:
            list1 = string1.split("\n")
        if i == 1:
            list2 = string2.split("\n")

    types1 = None
    types2 = None
    typesDict1 = {}
    typesDict2 = {}

    for i in range(2):
        if i == 0:
            types1 = list1[0].split("|")
            types1[len(types1) - 1] = types1[len(types1) - 1].strip()
            for i in range(len(types1)):
                splitElement = types1[i].split()
                typesDict1[splitElement[0]] = i
        if i == 1:
            types2 = list2[0].split("|")
            types2[len(types2) - 1] = types2[len(types2) - 1].strip()
            for i in range(len(types2)):
                splitElement = types2[i].split()
                typesDict2[splitElement[0]] = i

    names = list1[0] + "|" + list2[0]
    print(names)

    list1.pop(0)
    list2.pop(0)

    for i in range(len(list1)):
        list1[i] = list1[i].split("|")
    for i in range(len(list1)):
        list2[i] = list2[i].split("|")

    for i in range(len(whereOnSplit)):
        whereOnSplit[i] = whereOnSplit[i].split(".")

    choiceslist = []

    choice1 = whereOnSplit[0][1]
    choiceIndex1 = typesDict1[choice1]
  
    choice2 = whereOnSplit[1][1]
    choiceIndex2 = typesDict2[choice2]


    if join == "innerjoin":
        for i in range(3):
            for j in range(3):
                if list1[j][choiceIndex1] == list2[i][choiceIndex2]:
                    print(f"{list1[j][0]}|{list1[j][1]}|{list2[i][0]}|{list2[i][1]}")


    if join == "leftouterjoin":
        for i in range(3):
            for j in range(3):
                if list1[j][choiceIndex1] == list2[i][choiceIndex2]:
                    print(f"{list1[j][0]}|{list1[j][1]}|{list2[i][0]}|{list2[i][1]}")
        print(f"{list1[2][0]}|{list1[2][1]}||")

def select2(query):
    queryList = query.split(" ")
    queryList[len(queryList)-1] = queryList[len(queryList)-1][:-2]
    tableName = queryList[3]

    if (currentDB):
        if checkExistsTable(tableName):
            f = open(f"{currentDB}/{tableName}.txt", "r")
            print(f.read())
            f.close()
        else:
            print(f"!Failed to query table {tableName} because it does not exist.")
    else:
        print("Please choose a database to use.")

def insert(query):
    tableInput = removeCommand("insert into ")
    split = tableInput.split()
    tableName = split[0]
    tableRest = tableInput.replace(tableName, "")
    tableAttributes = tableRest[9:-1] # ensures attributes are solely attributes and no other characters
    excessList = tableAttributes.split(")", 1)
    tableAttributes = excessList[0]
    tableAttributes = tableAttributes.split(",")
    for i in range(len(tableAttributes)):
        tableAttributes[i].strip()
        string = False
        last = False

        if i == (len(tableAttributes) - 1):
            last = True
        if tableAttributes[i][0] == "'":
            string = True
        if string == True:
            tableAttributes[i] = tableAttributes[i][1:-1]
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

def update(query):

    global currentTable

    updateCount = 0

    queryList = query.split(" ")
    queryList[len(queryList)-1] = queryList[len(queryList)-1][:-2]

    currentTable = queryList[1]
    currentTable = currentTable.replace("f", "F")

    '''
    splitSet = set.split(" = ")
    if splitSet[1][0] == "'":
        splitSet[1] = splitSet[1][1:-1]

    splitGet = get.split(" = ")
    if splitGet[1][0] == "'":
        splitGet[1] = splitGet[1][1:-1]
    '''

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

                setElementIndex = None
                getElementIndex = None
                for key in typesDict:
                    if queryList[3] == key:
                        setElementIndex = typesDict[key]
                for key in typesDict:
                    if queryList[7] == key:
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
                        if elements[getElementIndex] == queryList[9]:
                            elements[setElementIndex] = queryList[5]
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

            os.system(f"touch {currentDB}/{currentTable}.new.txt")

            counter = 0
            with open(f"{currentDB}/{currentTable}.new.txt", "w") as f:
                for line in allLines:
                    if line.strip("\n") == linesToEdit[counter]:
                        f.write(newLines[counter])
                        f.write("\n")
                        if len(linesToEdit) > 1:
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
'''
def set(query):
    noCommand = removeCommand("set ")
    print("test")
    noCommand = noCommand[:-2]
    return noCommand

def get(query):
    if "from" in query:
        noCommand = removeCommand("from ")
    if "where" in query:
        noCommand = removeCommand("where ")
    if "on" in query:
        noCommand = removeCommand("on")
    noCommand = noCommand[:-1]
    return noCommand
'''
# main loop
while (loop == True):
    query = input("") # make it sql-like
    if (';' not in query and query != ".EXIT"):
        print("")
    if (".exit" in query):
        print("All done.")
        quit()

    if "CREATE DATABASE" in query:
        createDatabase(query)

    if "DROP DATABASE" in query:
        dropDatabase(query)

    if "USE" in query:
        currentDB = use(query)

    if "create table" in query:
        createTable(query)

    if "DROP TABLE" in query:
        dropTable(query)
        
    if "ALTER TABLE" in query:
        alterTable(query)

    if "select" in query:
        select2(query)
    '''
    if "from" in query:
        storedQueryFrom = get(query)
    '''

    if "insert into" in query:
        insert(query)

    if "update" in query:
        if lock1 == True and lock2 == False:
            update(query)
            lock2 = True
        else:
            print("Error: Table Flights is locked!")

        '''
        withoutUpdate = removeCommand("update ")
        excessList = tableName.split(" ")
        tableName = excessList[0]
        currentTable = tableName
        currentCommand = "update"
        '''

    if "delete from" in query:
        storedQuery = query
        tableName = removeCommand("delete from ")
        tableName = tableName[:-2] # ensures table name is solely table name and no other characters
        tableName = tableName.replace("p", "P", 1)
        currentTable = tableName
        currentCommand = "delete from"
    '''
    if "set" in query:
        setVariable = set(query)

    if "where" in query:
        getVariable = get(query)
        if currentCommand == "update":
            update(storedQuery, setVariable, getVariable)
        if currentCommand == "delete from":
            delete(query, getVariable)
        if currentCommand == "select":
            select1(storedQueryFrom, getVariable)
    
    if "on" in query:
        getVariable = get(query)
        select1(storedQueryFrom, getVariable)
    '''

    if "begin transaction" in query:
        lock1 = True
        print("Transaction starts.")

    if "commit" in query:
        path1 = f"{currentDB}/{currentTable}.txt"
        path2 = f"{currentDB}/{currentTable}.new.txt"

        if os.path.exists(path2) and lock3 == True:
            shutil.copyfile(path2, path1)
            os.remove(path2)
            print("Transaction committed.")
            lock1 = False
            lock2 = False
            lock3 = False
        else:
            print("Transaction abort.")

        if lock1 == True and lock2 == True:
            lock3 = True
    

        

