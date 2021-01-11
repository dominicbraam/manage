import menu

promptNew = "[NEW]"
promptForTaskList = "Enter task list: "
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

def getTaskList():
    userInput = input(promptForTaskList)
    if len(userInput) > 50:
        print("Task list name too long. Try again.")
        return getTaskList()
    else:
        return userInput

def getTask():
    userInput = input("Task: ")
    if len(userInput) > 100:
        print("Task name too long. Try again.")
        return getTask()
    else:
        return userInput

def getSubtask():
    userInput = input("Subask: ")
    if len(userInput) > 100:
        print("Subtask name too long. Try again.")
        return getSubtask()
    else:
        return userInput

def getDuration():
    try:
        userInput = int(input("Duration (mins): "))
    except ValueError:
        print("Not an integer. Try again.")
        return getDuration()
    if userInput < 0 or userInput > 32000:
        print("Yeah right. You did not spend that much time on that. Try again.")
        return getDuration()
    else:
        return userInput

def getStatus():
    choiceStatus=True
    while choiceStatus: 
        menu.chooseStatus()
        choice=input(promptForChoice)
        if choice=='1':
            status="Up Next"
            choiceStatus=None
        elif choice=='2':
            status="In Progress"
            choiceStatus=None
        elif choice=='3':
            status="Completed"
            choiceStatus=None
        elif choice=='4':
            status="Recurring"
            choiceStatus=None
        else:
            print(errorNoOption)
    return status
