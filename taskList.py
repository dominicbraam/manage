from dataConnect import cursor
from dataConnect import db
import manageDB
import menu
import tasks
import uInput

def isEmpty():
    cursor.execute("SELECT COUNT(*) FROM tasks_list")
    if cursor.fetchone()[0]>=1:
        return False
    else:
        return True 

def show():
    if isEmpty():
        print(uInput.errorNoListsExist)
    else:
        cursor.execute("SELECT * FROM tasks_list")
        for x in cursor:
            print(x[0],":",x[1])

def getListName(tlID):
    cursor.execute("SELECT listname FROM tasks_list WHERE tlid = \"{tlID}\"".format(tlID=tlID))
    name = cursor.fetchone()[0]
    return name

def taskListExists(tlID):
    cursor.execute("SELECT COUNT(listname) FROM tasks_list WHERE tlid = \"{tlID}\"".format(tlID=tlID))
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def taskListExistsByName(listname):
    cursor.execute("SELECT COUNT(*) FROM tasks_list WHERE listname = \"{listname}\"".format(listname=listname))
    if cursor.fetchone()[0]==1:
        return True
    else:
        return False

def create():
    print(uInput.promptNew)
    taskList = uInput.getTaskList() 
    if taskListExistsByName(taskList):
        print(uInput.promptListExists)
    else:
        cursor.execute("INSERT INTO tasks_list (listname) VALUES (\"{tlID}\")".format(tlID=taskList))
        db.commit()
        print(uInput.promptListCreated)

def delete(tlID):
    if taskListExists(tlID):
        cursor.execute("DELETE FROM tasks_list WHERE tlid = \"{tlID}\"".format(tlID=tlID))
        manageDB.resetPriKey("subtasks_2021")
        manageDB.resetPriKey("main_tasks")
        manageDB.resetPriKey("tasks_list")
        db.commit()
        print(uInput.promptListDeleted)
    else:
        print(uInput.errorListNoExist)

def rename(tlID):
    if not taskListExists(tlID):
        print(uInput.errorListNoExist)
    else:
        print(uInput.promptNew)
        newListName = uInput.getTaskList()
        cursor.execute("UPDATE tasks_list SET listname = \"{newListName}\" WHERE tlid = \"{tlID}\"".format(newListName=newListName,tlID=tlID))
        db.commit()

def open(tlID):
    if not taskListExists(tlID):
        print(uInput.errorListNoExist)
        return
    
    listName = getListName(tlID)
    menuSelect = True
    while menuSelect:

        if tasks.isEmpty(tlID):
            menu.openTasksNone(listName)
            menuSelect = input(uInput.promptForChoice)
            if menuSelect=='1':
                tasks.create(tlID)
            elif menuSelect=='0':
                menuSelect=None
            else:
                print(uInput.errorNoOption)
        else:
            menu.openTasks(listName)
            menuSelect = input(uInput.promptForChoice)
            if menuSelect=='1':
                tasks.show(tlID)
            elif menuSelect=='2':
                tasks.show(tlID)
                tasks.open(uInput.getChoice(),tlID)
            elif menuSelect=='3':
                tasks.create(tlID)
            elif menuSelect=='4':
                tasks.show(tlID)
                tasks.rename(uInput.getChoice(),tlID)
            elif menuSelect=='5':
                tasks.show(tlID)
                tasks.delete(uInput.getChoice(),tlID)
            elif menuSelect=='0':
                menuSelect=None
            else:
                print(uInput.errorNoOption)
