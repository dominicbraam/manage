from dataConnect import cursor
from dataConnect import db
import uInput
import menu
import datetime

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
    count = 0
    for x in cursor:
        if count == selectNum:
            return x[0]
        else:
            count+=1
    return 0

def getItemIDByName(tableName,itemID_parent,name):
    idName_parent = getParentIDName(tableName)
    idName = getIDName(tableName)
    columnName = getColumnName(tableName)
    cursor.execute("SELECT {idName} FROM {tableName} WHERE {idName_parent} = \"{itemID_parent}\" AND {columnName} = \"{name}\"".format(idName=idName,tableName=tableName,idName_parent=idName_parent,itemID_parent=itemID_parent,name=name,columnName=columnName))
    result = cursor.fetchone()
    return result[0]

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
    idName = getIDName(tableName)
    idName_parent = getParentIDName(tableName)
    if itemID_parent==None:
        cursor.execute("SELECT {idName}, {columnName} FROM {tableName}".format(idName=idName,columnName=columnName,tableName=tableName))
    else:
        cursor.execute("SELECT * FROM {tableName} WHERE {idName_parent} = \"{itemID_parent}\"".format(idName=idName,columnName=columnName,idName_parent=idName_parent,tableName=tableName,itemID_parent=itemID_parent))
    items = cursor.fetchall()
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

def createItem(tableName,itemID_parent,allowDup):
    print(uInput.promptNew)
    item = uInput.getName(tableName)

    if itemExistsByName(tableName,itemID_parent,item) and allowDup==False:
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
            date = uInput.getDate(0)
            status = uInput.getStatus()
            duedate = uInput.getDue()
            cursor.execute("INSERT INTO {tableName} ({idName_parent},{columnName},duration,timestamp,status,duedate) VALUES (\"{itemID_parent}\",\"{item}\",{duration},\"{date}\",\"{status}\",\"{duedate}\")".format(tableName=tableName,idName_parent=idName_parent,columnName=columnName,itemID_parent=itemID_parent,item=item,duration=duration,date=date,status=status,duedate=duedate))
        db.commit()
        print("Item successfully created.")
    menu.back()

def deleteItem(tableName,itemID_parent,itemNum):
    if itemNum == -1:
        return
    elif tableName=="tasks_list" and itemNum == 0:
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
    if itemNum == -1:
        return
    elif tableName=="tasks_list" and itemNum == 0:
        return
    if itemID_parent==None:
        itemID=itemNum
    else:
        itemID=getItemID(tableName,itemID_parent,itemNum)
    oldName = getItemName(tableName,itemID)
    idName = getIDName(tableName)
    idName_parent = getParentIDName(tableName)
    columnName = getColumnName(tableName)

    print(uInput.promptNew)
    newItemName = uInput.getName(tableName)

    if tableName == "subtasks_2021":
        cursor.execute("UPDATE {tableName} SET {columnName} = \"{newItemName}\" WHERE {idName_parent} = \"{itemID_parent}\" AND {columnName} = \"{oldName}\"".format(tableName=tableName,columnName=columnName,newItemName=newItemName,oldName=oldName,idName_parent=idName_parent,itemID_parent=itemID_parent))
        db.commit()
    elif itemExistsByName(tableName,itemID_parent,newItemName):
        print(uInput.promptTaskExists)
    else:
        cursor.execute("UPDATE {tableName} SET {columnName} = \"{newItemName}\" WHERE {idName} = \"{itemID}\"".format(tableName=tableName,columnName=columnName,newItemName=newItemName,idName=idName,itemID=itemID))
        db.commit()

def updateItem(tableName,columnName,itemUpdate,idName,itemID):
    cursor.execute("UPDATE {tableName} SET {columnName} = \"{itemUpdate}\" WHERE {idName} = \"{itemID}\"".format(tableName=tableName,columnName=columnName,itemUpdate=itemUpdate,idName=idName,itemID=itemID))
    db.commit()

def modifySubtask(tableName,itemID_parent,itemNum):
    if itemNum == -1:
        return
    itemID = getItemID(tableName,itemID_parent,itemNum)
    idName = getIDName(tableName)
    itemName = getItemName(tableName,itemID)

    modifySubtask_menu_exit = False
    while not modifySubtask_menu_exit:
        modify_menu = menu.modifySubtask(itemName)
        menu_sel = modify_menu.show()

        if menu_sel == 0:
            print(uInput.promptNew)
            renameItem(tableName,itemID_parent,itemNum)
        elif menu_sel == 1:
            print(uInput.promptNew)
            duration = uInput.getDuration()
            updateItem(tableName,"duration",duration,idName,itemID)
        elif menu_sel == 2:
            print(uInput.promptNew)
            date = uInput.getDate(0) 
            updateItem(tableName,"timestamp",date,idName,itemID)
        elif menu_sel == 3:
            print(uInput.promptNew)
            status = uInput.getStatus()
            updateItem(tableName,"status",status,idName,itemID)
        elif menu_sel == 4:
            print(uInput.promptNew)
            duedate = uInput.getDue()
            updateItem(tableName,"duedate",duedate,idName,itemID)
        elif menu_sel == 5:
            modifySubtask_menu_exit = True

def addLogWithRef(tableName,itemID_parent,index):
    if index == -1:
        return
    idName_parent = getParentIDName(tableName)
    columnName = getColumnName(tableName)
    
    item = getItemName(tableName,index)
    duration = uInput.getDuration()
    date = uInput.getDate(0)
    status = uInput.getStatus()
    duedate = uInput.getDue()
    cursor.execute("INSERT INTO {tableName} ({idName_parent},{columnName},duration,timestamp,status,duedate) VALUES (\"{itemID_parent}\",\"{item}\",{duration},\"{date}\",\"{status}\",\"{duedate}\")".format(tableName=tableName,idName_parent=idName_parent,columnName=columnName,itemID_parent=itemID_parent,item=item,duration=duration,date=date,status=status,duedate=duedate))
    db.commit()
    print("Item successfully created.")
    menu.back()

def hasDue(date):
    noDue = datetime.datetime(1,1,1)
    if date==noDue:
        return False
    else:
        return True
