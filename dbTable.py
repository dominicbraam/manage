from dataConnect import cursor
from dataConnect import db
import uInput
import menu

def getIDName(tableName):
    if tableName == "tasks_list":
        idName="tlid"
    elif tableName == "main_tasks":
        idName="taskID"
    elif tableName == "subtasks_2021":
        idName="subtaskID"
    return idName

def getParentIDName(tableName):
    if tableName=="tasks_list":
        idName_parent=None
    elif tableName=="main_tasks":
        idName_parent="tlID"
    elif tableName=="subtasks_2021":
        idName_parent="taskID"
    return idName_parent

def getColumnName(tableName):
    if tableName=="tasks_list":
        columnName="listname"
    elif tableName=="main_tasks":
        columnName="task"
    elif tableName=="subtasks_2021":
        columnName="subtask"
    return columnName

def resetPriKey(tableName):
    idName = getIDName(tableName)
    cursor.execute("SET @count = 0")
    cursor.execute("UPDATE {tableName} SET {idName} = @count:= @count + 1".format(tableName=tableName,idName=idName))
    cursor.execute("ALTER TABLE {tableName} AUTO_INCREMENT = 1".format(tableName=tableName))

def isEmpty(tableName,itemID_parent):
    idName_parent = getParentIDName(tableName)
    if itemID_parent==None:
        cursor.execute("SELECT COUNT(*) FROM {tableName}".format(tableName=tableName))
    else:
        cursor.execute("SELECT COUNT(*) FROM {tableName} WHERE {idName_parent} = \"{itemID_parent}\"".format(tableName=tableName,idName_parent=idName_parent,itemID_parent=itemID_parent))
    results = cursor.fetchone()
    if results is None or results[0]==0:
        return True
    else:
        return False

def getItemID(tableName,itemID_parent,selectNum):
    idName_parent = getParentIDName(tableName)
    cursor.execute("SELECT * FROM {tableName} WHERE {idName_parent} = \"{itemID_parent}\"".format(tableName=tableName,idName_parent=idName_parent,itemID_parent=itemID_parent))
    selectNum = int(selectNum)
    count = 1
    for x in cursor:
        if count == selectNum:
            return x[0]
        else:
            count+=1
    return 0

def getItemName(tableName,itemID):
    idName = getIDName(tableName)
    columnName = getColumnName(tableName)
#    if tableName=="tasks_list":
#        cursor.execute("SELECT {columnName} FROM {tableName}".format(columnName=columnName,tableName=tableName))
#    else:
    cursor.execute("SELECT {columnName} FROM {tableName} WHERE {idName} = \"{itemID}\"".format(columnName=columnName,tableName=tableName,idName=idName,itemID=itemID))
    name = cursor.fetchone()[0]
    return name

def showNames(tableName,itemID):
    idName_parent = getParentIDName(tableName)
    if itemID==None:
        cursor.execute("SELECT * FROM {tableName}".format(tableName=tableName))
    else:
        cursor.execute("SELECT * FROM {tableName} WHERE {idName_parent} = \"{itemID}\"".format(tableName=tableName,idName_parent=idName_parent,itemID=itemID))
    count = 1
    for x in cursor:
        print(count,":",x[1])
        count+=1
    menu.back()

def itemExists(tableName,itemID,itemID_parent):
    idName = getIDName(tableName)
    idName_parent = getParentIDName(tableName)
    if itemID_parent==None:
        cursor.execute("SELECT COUNT(*) FROM {tableName} WHERE {idName} = \"{itemID}\"".format(tableName=tableName,idName=idName,itemID=itemID))
    else:
        cursor.execute("SELECT COUNT(*) FROM {tableName} WHERE {idName} = \"{itemID}\" AND {idName_parent} = \"{itemID_parent}\"".format(tableName=tableName,idName=idName,itemID=itemID,idName_parent=idName_parent,itemID_parent=itemID_parent))
    results = cursor.fetchone()
    if results is None:
        return False
    else:
        return True

def getItemsForMenu(tableName,itemID_parent):
    columnName = getColumnName(tableName)
    idName_parent = getParentIDName(tableName)
    if itemID_parent==None:
        cursor.execute("SELECT {columnName} FROM {tableName}".format(columnName=columnName,tableName=tableName))
    else:
        cursor.execute("SELECT {columnName} FROM {tableName} WHERE {idName_parent} = \"{itemID_parent}\"".format(columnName=columnName,idName_parent=idName_parent,tableName=tableName,itemID_parent=itemID_parent))
    count = 0
    items = []
    for x in cursor:
        itemNum = count+1
        items.append("[{itemNum}] {x}".format(itemNum=itemNum,x=x[0]))
        count+=1
    return items

def itemExistsByName(tableName,itemID_parent,name):
    idName_parent = getParentIDName(tableName)
    columnName = getColumnName(tableName)
    if itemID_parent==None:
        cursor.execute("SELECT COUNT(*) FROM {tableName} WHERE {columnName} = \"{name}\"".format(tableName=tableName,columnName=columnName,name=name))
    else:
        cursor.execute("SELECT COUNT(*) FROM {tableName} WHERE {columnName} = \"{name}\" AND {idName_parent} = \"{itemID_parent}\"".format(tableName=tableName,columnName=columnName,name=name,idName_parent=idName_parent,itemID_parent=itemID_parent))
    results = cursor.fetchone()
    if results[0]==1:
        return True
    else:
        return False

def createItem(tableName,itemID_parent):
    print(uInput.promptNew)
    item = uInput.getName(tableName)

    if itemExistsByName(tableName,itemID_parent,item):
        print("Item already exists.")
    else:
        idName_parent = getParentIDName(tableName)
        columnName = getColumnName(tableName)
        if idName_parent==None:
            cursor.execute("INSERT INTO {tableName} ({columnName}) VALUES (\"{item}\")".format(tableName=tableName,columnName=columnName,item=item))
        elif tableName=="main_tasks":
            cursor.execute("INSERT INTO {tableName} ({columnName},{idName_parent}) VALUES (\"{item}\",\"{itemID_parent}\")".format(tableName=tableName,columnName=columnName,idName_parent=idName_parent,item=item,itemID_parent=itemID_parent))
        elif tableName=="subtasks_2021":
            duration = uInput.getDuration()
            status = uInput.getStatus()
            cursor.execute("INSERT INTO subtasks_2021 ({idName_parent},{columnName},duration,timestamp,status) VALUES (\"{itemID_parent}\",\"{item}\",{duration},now(),\"{status}\")".format(idName_parent=idName_parent,columnName=columnName,itemID_parent=itemID_parent,item=item,duration=duration,status=status))
        db.commit()
        print("Item successfully created.")
    menu.back()

def deleteItem(tableName,itemID_parent,itemNum):
    if itemNum == 0:
        return
    if itemID_parent==None:
        itemID = itemNum
    else:
        itemID = getItemID(tableName,itemID_parent,itemNum)
    idName = getIDName(tableName) 
    cursor.execute("DELETE FROM {tableName} WHERE {idName} = \"{itemID}\"".format(tableName=tableName,idName=idName,itemID=itemID))
    if tableName=="tasks_list":
        resetPriKey("subtasks_2021")
        resetPriKey("main_tasks")
        resetPriKey("tasks_list")
    elif tableName=="main_tasks":
        resetPriKey("subtasks_2021")
        resetPriKey("main_tasks")
    elif tableName=="subtasks_2021":
        resetPriKey("subtasks_2021")
    db.commit()
    print("Item successfully deleted.")
    menu.back()

def renameItem(tableName,itemID_parent,itemNum):
    if itemNum == 0:
        return
    if itemID_parent==None:
        itemID=itemNum
    else:
        itemID=getItemID(tableName,itemID_parent,itemNum)
    idName = getIDName(tableName)
    columnName = getColumnName(tableName)

    print(uInput.promptNew)
    newItemName = uInput.getName(tableName)

    if itemExistsByName(tableName,itemID_parent,newItemName):
        print(uInput.promptTaskExists)
    else:
        cursor.execute("UPDATE {tableName} SET {columnName} = \"{newItemName}\" WHERE {idName} = \"{itemID}\"".format(tableName=tableName,columnName=columnName,newItemName=newItemName,idName=idName,itemID=itemID))
        db.commit()
