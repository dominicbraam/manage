from dataConnect import cursor
from dataConnect import db
import manageDB
import menu
import uInput
import subtasks

def isEmpty(tlID):
    cursor.execute("SELECT COUNT(*) FROM main_tasks WHERE tlID = \"{tlID}\"".format(tlID=tlID))
    if cursor.fetchone()[0]>=1:
        return False
    else:
        return True

def show(tlID):
    if isEmpty(tlID):
        print(uInput.errorNoTasksExist)
    else:
        cursor.execute("SELECT * FROM main_tasks WHERE tlID = \"{tlID}\"".format(tlID=tlID))
        count = 1
        for x in cursor:
            print (count,":",x[1])
            count+=1

def taskExists(taskID,tlID):
    cursor.execute("SELECT COUNT(*) from main_tasks WHERE taskID = \"{taskID}\" AND tlID = \"{tlID}\"".format(taskID=taskID,tlID=tlID))
    results = cursor.fetchone()
    if results is None or taskID==0:
        return False
    else:
        return True

def taskExistsByName(taskName,tlID):
    cursor.execute("SELECT COUNT(*) FROM main_tasks WHERE task = \"{taskName}\" AND tlID = \"{tlID}\"".format(taskName=taskName,tlID=tlID))
    if cursor.fetchone()[0]==1:
        return True
    else:
        return False

def getTaskID(taskNum,tlID):
    cursor.execute("SELECT * FROM main_tasks WHERE tlID = \"{tlID}\"".format(tlID=tlID))
    taskNum = int(taskNum)
    count = 1
    for x in cursor:
        if count == taskNum:
            return x[0]
        else:
            count+=1
    return 0

def getTaskName(taskID):
    cursor.execute("SELECT task FROM main_tasks WHERE taskID = \"{taskID}\"".format(taskID=taskID))
    taskName = cursor.fetchone()[0]
    return taskName

def create(tlID):
    print(uInput.promptNew)
    task = uInput.getTask()
    if taskExistsByName(task,tlID):
        print(uInput.promptTaskExists)
    else:
        cursor.execute("INSERT INTO main_tasks (task,tlID) VALUES (\"{task}\",\"{tlID}\")".format(task=task,tlID=tlID))
        db.commit()
        print(uInput.promptTaskCreated)

def delete(taskNum,tlID):
    taskID = getTaskID(taskNum,tlID)
    if taskExists(taskID,tlID):
        cursor.execute("DELETE FROM main_tasks WHERE taskID = \"{taskID}\"".format(taskID=taskID))
        manageDB.resetPriKey("subtasks_2021")
        manageDB.resetPriKey("main_tasks")
        db.commit()
        print(uInput.promptTaskDeleted)
    else:
        print(uInput.errorTaskNoExist)

def rename(taskNum,tlID):
    taskID = getTaskID(taskNum,tlID)
    if not taskExists(taskID,tlID):
        print(uInput.errorTaskNoExist)
    else:
        print(uInput.promptNew)
        newTaskName = uInput.getTask()
        if taskExistsByName(newTaskName,tlID):
            print(uInput.promptTaskExists)
        else:
            cursor.execute("Update main_tasks SET task = \"{newTaskName}\" WHERE taskID = \"{taskID}\"".format(newTaskName=newTaskName,taskID=taskID))
            db.commit()

def open(taskNum,tlID):
    taskID = getTaskID(taskNum,tlID)
    if not taskExists(taskID,tlID):
        print(uInput.errorTaskNoExist)
        return

    taskName = getTaskName(taskID)
    menuSelect = True
    while menuSelect:

        if subtasks.isEmpty(taskID):
            menu.openSubtasksNone(taskName)
            menuSelect = input(uInput.promptForChoice)
            if menuSelect=='1':
                subtasks.create(taskID)
            elif menuSelect=='0':
                menuSelect=None
            else:
                print(uInput.errorNoOption)
        else:
            menu.openSubtasks(taskName)
            menuSelect = input(uInput.promptForChoice)
            if menuSelect=='1':
                subtasks.show(taskID)
            elif menuSelect=='3':
                subtasks.create(taskID)
            elif menuSelect=='5':
                subtasks.show(taskID)
                subtasks.delete(uInput.getChoice(),taskID)
            elif menuSelect=='0':
                menuSelect=None
            else:
                print(uInput.errorNoOption)
