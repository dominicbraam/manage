def main():
    print("Main Menu:")
    print("1: Show task lists.")
    print("2: Open task list.")
    print("3: Create task list.")
    print("4: Rename task list.")
    print("5: Delete task list.")

def mainEmpty():
    print("Main Menu:")
    print("No data exists...")
    print("1: Create")

def openTasks(taskList):
    print("Menu - " + taskList)
    print("1: Show tasks.")
    print("2: Open task.")
    print("3: Create task.")
    print("4: Rename task.")
    print("5: Delete task.")
    print("0: back")

def openTasksNone(taskList):
    print("Menu - " + taskList)
    print("No tasks exist...")
    print("1: Create task.")
    print("0: back")

def openSubtasks(task):
    print("Menu - " + task)
    print("1: Show subtasks.")
    print("3: Create subtask.")
    print("5: Delete subtask.")
    print("0: back")

def openSubtasksNone(task):
    print("Menu - " + task)
    print("No subtasks exist...")
    print("1: Create subtask.")
    print("0: back")

def chooseStatus():
    print("1: Up Next")
    print("2: In Progress")
    print("3: Completed")
    print("4: Recurring")
