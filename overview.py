from dataConnect import cursor
import menu
import dbTable
import datetime
from tabulate import tabulate

def all(tableName,itemID_parent):

    cursor.execute("SELECT taskID, task FROM main_tasks WHERE tlID = \"{itemID_parent}\"".format(itemID_parent=itemID_parent))
    tasks = cursor.fetchall()

    for x in tasks:
        print(menu.design.BOLD + menu.design.UNDERLINE + x[1] + menu.design.END)
        cursor.execute("SELECT DISTINCT subtask FROM subtasks_2021 WHERE taskID = \"{x}\"".format(x=x[0]))
        subtaskNames = [row[0] for row in cursor.fetchall()]
        subtasks =[] 
        inProgress = []
        upNext = []
        completed = []
        storeDuration = []
        for i in subtaskNames:
            duration =0 
            cursor.execute("SELECT subtask, status, duedate, timestamp, duration FROM subtasks_2021 WHERE subtask = \"{i}\" ORDER BY timestamp DESC".format(i=i))
            getSimilar = cursor.fetchall()
            for t in getSimilar:
                duration=t[4] + duration
            item = getSimilar[0]
            if item[1]=="In Progress":
                inProgress.append(item)
            elif item[1]=="Up Next":
                upNext.append(item)
            elif item[1]=="Completed":
                completed.append(item)
            storeDuration.append(duration)

        subtasksFormatted = []
        item = ()
        colour ="" 
        dueDate = datetime.datetime(1,1,1) 

        for a in inProgress:
            subtasks.append(a)
        for b in upNext:
            subtasks.append(b)
        for c in completed:
            subtasks.append(c)

        countY=0
        for y in subtasks:
            itemName = y[0]

            if y[1] == "Up Next":
                colour = menu.design.RED
            elif y[1] == "In Progress":
                colour = menu.design.YELLOW
            elif y[1] == "Completed":
                colour = menu.design.GREEN

            if dbTable.hasDue(y[2]):
                dueDate = y[2]
                dueDate.strftime("%m/%d/%Y")
            else:
                dueDate = None

            formattedDuration = round(storeDuration[countY]/60,2)

            item = (itemName,"[{duration} hrs]".format(duration=formattedDuration),"[{colour}{status}{end}]".format(colour=colour,status=y[1],end=menu.design.END), "Due: {dueDate}".format(dueDate=dueDate))
            subtasksFormatted.append(item)
            countY+=1
            
        print(tabulate(subtasksFormatted, tablefmt='plain'))
        print("\n")
    menu.back()
