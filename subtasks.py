from dataConnect import cursor
from dataConnect import db
import manageDB
import menu
import uInput

def isEmpty(taskID):
    cursor.execute("SELECT COUNT(*) FROM subtasks_2021 WHERE taskID = \"{taskID}\"".format(taskID=taskID))
    if cursor.fetchone()[0]>=1:
        return False
    else:
        return True

def show(taskID):
    if isEmpty(taskID):
        print(uInput.errorNoSubtasksExist)
    else:
        cursor.execute("SELECT * FROM subtasks_2021 WHERE taskID = \"{taskID}\"".format(taskID=taskID))
        for x in cursor:
            print(x)

def getSubtaskID(subtaskNum,taskID):
    cursor.execute("SELECT * FROM subtasks_2021 WHERE taskID = \"{taskID}\"".format(taskID=taskID))
    subtaskNum = int(subtaskNum)
    count = 1
    for x in cursor:
        if count == subtaskNum:
            return x[0]
        else:
            count+=11
    return 0

def subtaskExists(subtaskID,taskID):
    cursor.execute("SELECT COUNT(*) FROM subtasks_2021 WHERE subtaskID = \"{subtaskID}\" AND taskID = \"{taskID}\"".format(subtaskID=subtaskID,taskID=taskID))
    results = cursor.fetchone()
    if results is None or taskID==0:
        return False
    else:
        return True

def create(taskID):
    print(uInput.promptNew)
    subtask = uInput.getSubtask() 
    duration = uInput.getDuration() 
    status = uInput.getStatus()
    cursor.execute("INSERT INTO subtasks_2021 (taskID,subtask,duration,timestamp,status) VALUES (\"{taskID}\",\"{subtask}\",{duration},now(),\"{status}\")".format(taskID=taskID,subtask=subtask,duration=duration,status=status))
    db.commit()
    print(uInput.promptSubtaskCreated)

def delete(subtaskNum,taskID):
    subtaskID = getSubtaskID(subtaskNum,taskID)
    if subtaskExists(subtaskID,taskID):
        cursor.execute("DELETE FROM subtasks_2021 WHERE subtaskID = \"{subtaskID}\"".format(subtaskID=subtaskID))
        manageDB.resetPriKey("subtasks_2021")
        db.commit()
        print(uInput.promptSubtaskDeleted)
    else:
        print(uInput.errorSubtaskNoExist)
