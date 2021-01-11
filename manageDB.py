from dataConnect import cursor
from dataConnect import db

def resetPriKey(table):
    if table == "tasks_list":
        id="tlid"
    elif table == "main_tasks":
        id="taskID"
    elif table == "subtasks_2021":
        id="subtaskID"
    cursor.execute("SET @count = 0")
    cursor.execute("UPDATE {table} SET {id} = @count:= @count + 1".format(table=table,id=id))
    cursor.execute("ALTER TABLE {table} AUTO_INCREMENT = 1".format(table=table))
