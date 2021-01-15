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
