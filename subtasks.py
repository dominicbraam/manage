from dataConnect import cursor
from dataConnect import db
import dbTable
import menu
import uInput

def show(taskID):
    if dbTable.isEmpty("subtasks_2021",taskID):
        print(uInput.errorNoSubtasksExist)
    else:
        cursor.execute("SELECT * FROM subtasks_2021 WHERE taskID = \"{taskID}\"".format(taskID=taskID))
        for x in cursor:
            print(x)

def modify(subtaskNum,taskID):
    subtaskID = dbTable.getItemID("subtasks_2021",taskID,subtaskNum)
    if dbTable.itemExists("subtasks_2021",subtaskID,taskID):
        subtaskName = dbTable.getItemName("subtasks_2021",subtaskID)
        menuSelect = True
        while menuSelect:
            menu.modifySubtask(subtaskName)
            menuSelect = input(uInput.promptForChoice)
            if menuSelect=='1':
                newName = uInput.getSubtask()
                cursor.execute("UPDATE subtasks_2021 SET subtask = \"{newName}\" WHERE subtaskID = \"{subtaskID}\"".format(newName=newName,subtaskID=subtaskID))
            elif menuSelect=='2':
                newDuration = uInput.getDuration()
                cursor.execute("UPDATE subtasks_2021 SET duration = \"{newDuration}\" WHERE subtaskID = \"{subtaskID}\"".format(newDuration=newDuration,subtaskID=subtaskID))
            elif menuSelect=='3':
                newStatus = uInput.getStatus()
                cursor.execute("UPDATE subtasks_2021 SET status = \"{newStatus}\" WHERE subtaskID = \"{subtaskID}\"".format(newStatus=newStatus,subtaskID=subtaskID))
            elif menuSelect=='0':
                menuSelect=None
            else:
                print(uInput.errorNoOption)
    else:
        print("else runs")
