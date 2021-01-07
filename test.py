import os
import mysql.connector
from mysql.connector import errorcode
import show

os.system("mysql.server start")

try:
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="01000100",
        database="manage_tasks"
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

def main():
    
    menuSelect = True

    while  menuSelect:
        show.MainMenu()
        menuSelect = input("Choice: ")

        if menuSelect=='1':
            showTaskLists()
        elif menuSelect=='2':
            createTaskList()
        elif menuSelect=='3':
            deleteTaskList()
        elif menuSelect=='exit':
            menuSelect=None
            db.commit()
            db.close()
            os.system("mysql.server stop")
        else:
            print("Not a valid option.")
# name = input("Enter your name: ")
# age = int(input("Enter your age: "))

# cursor.execute("INSERT INTO test (name,number) VALUES (%s,%s)", (name,age))

def showTaskLists():
    cursor.execute("show tables")
    for (table_name,) in cursor:
        print(table_name)

def showTasks():
    cursor.execute("SELECT * FROM test")
    for x in cursor:
        print(x)

def checkTableExists(tableName):
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{tab}'".format(tab=tableName))
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def createTaskList():
    tableName = input("Enter task list name: ")
    tableName = tableName.lower()
    tableName = tableName.replace(" ","_")
    cursor.execute("CREATE TABLE IF NOT EXISTS {tab} (taskID int PRIMARY KEY NOT NULL AUTO_INCREMENT,task VARCHAR(100),subtask VARCHAR(100),duration SMALLINT)".format(tab=tableName))

def deleteTaskList():
    taskList = input("Enter name of task list to delete")
    if checkTableExists(taskList):
        cursor.execute("DROP TABLE {tab}".format(tab=taskList))
    else:
        print("The list '" + taskList + "' does not exist.")

if __name__ == "__main__":
    main()
