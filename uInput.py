import menu
import re
import datetime
from datetime import datetime, date, time

promptNew = "[NEW]"
promptForTaskList = "Task list: "
promptForTask = "Task: "
promptForSubtask = "Subask: "
promptForChoice = "Choice: "
promptListExists = "List already exists."
promptListCreated = "Task list created successfully."
promptListDeleted = "Task list deleted successfully."
promptTaskExists = "Task already exists."
promptTaskCreated = "Task created successfully."
promptTaskDeleted = "Task deleted successfully."
promptSubtaskCreated = "Subtask created successfully."
promptSubtaskDeleted = "Subtask deleted successfully."
errorListNoExist = "Task list does not exist."
errorNoListsExist = "No task lists exist. Try creating one."
errorTaskNoExist = "Task does not exist."
errorNoTasksExist = "No tasks exist. Try creating one."
errorSubtaskNoExist = "Subtask does not exist."
errorNoSubtasksExist = "No subtasks exist. Try creating a new one."
errorNoOption = "Not a valid option."

def getChoice():
    userInput = input(promptForChoice)
    return userInput

def getInteger(prompt):
    try:
        userInput = int(input(prompt))
        return userInput
    except ValueError:
        print("Not an integer. Try again.")
        return getInteger(prompt)

def getName(tableName):
    if tableName == "tasks_list":
        userInput = input(promptForTaskList)
    elif tableName == "main_tasks":
        userInput = input(promptForTask)
    elif tableName == "subtasks_2021":
        userInput = input(promptForSubtask)
    if not re.search('[a-zA-Z0-9_]',userInput) or userInput[:1]==" ":
        print("Not a valid name. Try again.")
        return getName(tableName)
    else:
        if tableName == "tasks_list" and len(userInput) > 50:
            print("Name too long. Try again.")
            return getName(tableName)
        elif len(userInput) > 100:
            print("Name too long. Try again.")
            return getName(tableName)
        else:
            return userInput

def getDuration():
    userInput = getInteger("Duration (mins): ")
    if userInput < 0 or userInput > 32000:
        print("Yeah right. You did not spend that much time on that. Try again.")
        return getDuration()
    else:
        return userInput

def getStatus():
    status_menu_exit = False
    status=""
    while not status_menu_exit: 
        get_status_menu = menu.getStatus()
        menu_sel = get_status_menu.show()
        if menu_sel==0:
            status="Up Next"
        elif menu_sel==1:
            status="In Progress"
        elif menu_sel==2:
            status="Completed"
        elif menu_sel==3:
            status="Recurring"
        status_menu_exit=True
    return status

def manualDate():
    year = getInteger("Year: ") 
    month = getInteger("Month: ") 
    day = getInteger("Day: ") 
    hour = getInteger("Hour: ") 
    minute = getInteger("Minute: ") 
    date = datetime(year,month,day,hour,minute)
    return date

def getDate(menu_sel):
    # menu_sel for automatic selection outside of func
    getDate_menu_exit = False
    date = datetime.now()
    if menu_sel == 1:
        date.strftime('%Y-%m-%d %H:%M:%S')
        return date
    if menu_sel == 2:
        date = manualDate()
        return date
    while not getDate_menu_exit:
        getDate_menu = menu.getDate()
        menu_sel = getDate_menu.show()
        if menu_sel==0:
            date = datetime.now()
        elif menu_sel==1:
           date = manualDate() 
        getDate_menu_exit = True
    date.strftime('%Y-%m-%d %H:%M:%S')
    return date

def getDue():
    getDue_menu_exit = False
    getDue_menu = menu.getDue()
    menu_sel = getDue_menu.show()
    while not getDue_menu_exit:
        if menu_sel==0:
            due = datetime.min 
            due.strftime('%Y-%m-%d %H:%M:%S')
            return due
        elif menu_sel==1:
            due = manualDate()
            due.strftime('%Y-%m-%d %H:%M:%S')
            return due
