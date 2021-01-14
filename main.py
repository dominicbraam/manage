import dataConnect
from dataConnect import db
import menu
import uInput
import dbTable

def main():

    main_menu_exit = False

    while not main_menu_exit:
        if dbTable.isEmpty("tasks_list",None):
            main_menu = menu.main(0)
            main_sel = main_menu.show()

            if main_sel == 0:
                dbTable.createItem("tasks_list",None)
            elif main_sel == 1:
                main_menu_exit = True
                print("manageDom Closed.")
        else:
            main_menu = menu.main(1)
            main_sel = main_menu.show()

            if main_sel == 0:
                dbTable.showNames("tasks_list",None)
            elif main_sel == 1:
                index = menu.selectItem("tasks_list",None)
                open("main_tasks",index+1,"tasks_list")
            elif main_sel == 2:
                dbTable.createItem("tasks_list",None)
            elif main_sel == 3:
                index = menu.selectItem("tasks_list",None)
                dbTable.renameItem("tasks_list",None,index+1)
            elif main_sel == 4:
                index = menu.selectItem("tasks_list",None)
                dbTable.deleteItem("tasks_list",None,index+1)
            elif main_sel == 5:
                main_menu_exit = True
                db.close()
                dataConnect.mysqlStop()
                print("manageDom Closed.")

def open(tableName,itemID_parent,tableName_parent):
    if itemID_parent == 0:
        return
    menu_exit = False

    while not menu_exit:
        if dbTable.isEmpty(tableName,itemID_parent):
            tasks_menu = menu.tasks(0,tableName_parent,itemID_parent)
            menu_sel = tasks_menu.show()

            if menu_sel == 0:
                dbTable.createItem(tableName,itemID_parent)
            elif menu_sel == 1:
                menu_exit = True

        else:
            tasks_menu = menu.tasks(1,tableName_parent,itemID_parent)
            menu_sel = tasks_menu.show()

            if menu_sel == 0:
                dbTable.showNames(tableName,itemID_parent)
            elif menu_sel == 1:
                itemNum = menu.selectItem(tableName,itemID_parent)
                index = dbTable.getItemID(tableName,itemID_parent,itemNum)
                print(index)
                openSubtasks("subtasks_2021",index,"main_tasks")
            elif menu_sel == 2:
                dbTable.createItem(tableName,itemID_parent)
            elif menu_sel == 3:
                index = menu.selectItem(tableName,itemID_parent)
                dbTable.renameItem(tableName,itemID_parent,index)
            elif menu_sel == 4:
                index = menu.selectItem(tableName,itemID_parent)
                dbTable.deleteItem(tableName,itemID_parent,index)
            elif menu_sel == 5:
                menu_exit = True

def openSubtasks(tableName,itemID_parent,tableName_parent):
    if itemID_parent == 0:
        return
    menu_exit = False

    while not menu_exit:
        if dbTable.isEmpty(tableName,itemID_parent):
            tasks_menu = menu.subtasks(0,tableName_parent,itemID_parent)
            menu_sel = tasks_menu.show()

            if menu_sel == 0:
                dbTable.createItem(tableName,itemID_parent)
            elif menu_sel == 1:
                menu_exit = True

        else:
            tasks_menu = menu.subtasks(1,tableName_parent,itemID_parent)
            menu_sel = tasks_menu.show()

            if menu_sel == 0:
                dbTable.showNames(tableName,itemID_parent)
            elif menu_sel == 1:
                # open subtasks
                print("subtasks")
            elif menu_sel == 2:
                dbTable.createItem(tableName,itemID_parent)
            elif menu_sel == 3:
                index = menu.selectItem(tableName,itemID_parent)
                dbTable.modifySubtask(tableName,itemID_parent,index)
            elif menu_sel == 4:
                index = menu.selectItem(tableName,itemID_parent)
                dbTable.deleteItem(tableName,itemID_parent,index)
            elif menu_sel == 5:
                menu_exit = True

if __name__ == "__main__":
    main()
