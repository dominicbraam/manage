from simple_term_menu import TerminalMenu
import dbTable

class design:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = "\033[1m"
    UNDERLINE = '\033[4m'
    END = "\033[0m"

def main(option):
    # 0 = empty, 1 = has items
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")

    if option == 0:
        main_menu_title =  "{BOLD}Main Menu{END}\nNo data exists...".format(BOLD=design.BOLD,END=design.END)
        main_menu_items = ["[1] Create task list", "[0] Quit"]
    elif option == 1:
        main_menu_title = "Main Menu\n"
        main_menu_items = ["[1] Show task lists", "[2] Open task list", "[3] Create task list", "[4] Rename task list","[5] Delete task list","[0] Quit"]

    main_menu = TerminalMenu(menu_entries=main_menu_items,
                             title=main_menu_title,
                             menu_cursor=main_menu_cursor,
                             menu_cursor_style=main_menu_cursor_style,
                             cycle_cursor=True,
                             clear_screen=True)
    return main_menu

def tasks(option,tableName_parent,itemID_parent):
    itemName_parent = dbTable.getItemName(tableName_parent,itemID_parent)
    # 0 = empty, 1 = has items
    menu_cursor = "> "
    menu_cursor_style = ("fg_red", "bold")

    menu_title = "Tasks Menu\n"
    if option == 0:
        menu_title = "Menu - {itemName_parent}\nNo data exists...\n".format(itemName_parent=itemName_parent)
        menu_items = ["[1] Create task", "[0] Back"]
    elif option == 1:
        menu_title = "Menu - {itemName_parent}\n".format(itemName_parent=itemName_parent)
        menu_items = ["[1] Show tasks", "[2] Open task", "[3] Create task", "[4] Rename task","[5] Delete task","[0] Back"]

    menu = TerminalMenu(menu_entries=menu_items,
                             title=menu_title,
                             menu_cursor=menu_cursor,
                             menu_cursor_style=menu_cursor_style,
                             cycle_cursor=True,
                             clear_screen=True)
    return menu

def subtasks(option,tableName_parent,itemID_parent):
    itemName_parent = dbTable.getItemName(tableName_parent,itemID_parent)
    # 0 = empty, 1 = has items
    menu_cursor = "> "
    menu_cursor_style = ("fg_red", "bold")

    menu_title = "Subtasks Menu\n"
    if option == 0:
        menu_title = "Menu - {itemName_parent}\nNo data exists...\n".format(itemName_parent=itemName_parent)
        menu_items = ["[1] Create subtask", "[0] Back"]
    elif option == 1:
        menu_title = "Menu - {itemName_parent}\n".format(itemName_parent=itemName_parent)
        menu_items = ["[1] Show subtasks", "[2] Add log for...", "[3] Create subtask", "[4] Modify subtask","[5] Delete subtask","[0] Back"]

    menu = TerminalMenu(menu_entries=menu_items,
                             title=menu_title,
                             menu_cursor=menu_cursor,
                             menu_cursor_style=menu_cursor_style,
                             cycle_cursor=True,
                             clear_screen=True)
    return menu


def back():
    back_menu_items = ["[0] back"]

    back_menu = TerminalMenu(menu_entries=back_menu_items)
    back_menu_exit=False
    while not back_menu_exit:
        back_sel = back_menu.show()
        if back_sel==0:
            back_menu_exit=True

    return back_menu

def noDupSubtasks(itemList):
    return list(set(i[1] for i in itemList))

def selectItem(tableName,itemID_parent,dup):
    items = dbTable.getItemsForMenu(tableName,itemID_parent)
    if not dup:
        items = noDupSubtasks(items)

    menu_items = []
    count = 1
    if dup and tableName=="subtasks_2021":
        for x in items:
            menu_items.append("[{count}] {itemName} - {duration} mins - Due: {duedate} - Logged: {timestamp}".format(count=count,itemName=x[1],duration=x[2], duedate=x[6],timestamp=x[3]))
            count+=1
    elif dup:
        for x in items:
            menu_items.append("[{count}] {itemName}".format(count=count,itemName=x[1]))
            count+=1
    
    else:
        for x in items:
            menu_items.append("[{count}] {itemName}".format(count=count,itemName=x))
            count+=1

    menu_items.append("[0] back") 

    menu_title = "Menu\n"
    if tableName == "main_tasks":
        menu_title = "Tasks:\n"
    elif tableName == "subtasks_2021":
        menu_title = "Subtasks:\n"
    elif tableName == "tasks_list":
        menu_title = "Categories:\n"
    selectItem_menu = TerminalMenu(menu_entries=menu_items,
                                   title=menu_title,
                                   cycle_cursor=True,
                                   clear_screen=True)
    menu_sel = selectItem_menu.show()
    if menu_sel == len(items):
        return -1
    elif not dup:
        index = dbTable.getItemIDByName(tableName,itemID_parent,items[menu_sel])
        return index
    else:
        return menu_sel

def getStatus():
    status_items = ["[1] Up Next", "[2] In Progress", "[3] Completed", "[4] Recurring"]
    menu_title = "Status:"
    get_status_menu = TerminalMenu(menu_entries=status_items,
                                   title=menu_title,
                                   cycle_cursor=True)
    return get_status_menu    

def getDate():
    date_menu_items = ["[1] Now", "[2] Custom"]
    menu_title = "Date:"
    date_menu = TerminalMenu(menu_entries=date_menu_items,
                             title=menu_title,
                             cycle_cursor=True)
    return date_menu

def getDue():
    getDue_menu_items = ["[1] No", "[2] Yes"]
    menu_title = "Due Date?"
    getDue_menu = TerminalMenu(menu_entries=getDue_menu_items,
                               title=menu_title,
                               cycle_cursor=True)
    return getDue_menu

def modifySubtask(name):
    modify_items = ["[1] Change name.", "[2] Change duration.", "[3] Change date.", "[4] Change status.", "[5] Change due date.","[0] Back."]
    menu_title = "Modifying {name}...\n".format(name=name)
    modify_menu = TerminalMenu(menu_entries=modify_items,
                               title=menu_title,
                               cycle_cursor=True,
                               clear_screen=True)
    return modify_menu
