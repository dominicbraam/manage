import os
os.system("mysql.server start")

import dataConnect
from dataConnect import db
from dataConnect import cursor
import menu
import uInput
import tasks
import taskList

def main():

    menuSelect = True
    while menuSelect:

        if taskList.isEmpty():
            menu.mainEmpty()
            menuSelect = uInput.getChoice()
            if menuSelect=='1':
                taskList.create()
            elif menuSelect=='exit':
                menuSelect=None
                db.close()
                os.system("mysql.server stop")
            else:
                print(uInput.errorNoOption)

        else:
            menu.main()
            menuSelect = uInput.getChoice()

            if menuSelect=='1':
                taskList.show()
            elif menuSelect=='2':
                taskList.show()
                taskList.open(uInput.getChoice())
            elif menuSelect=='3':
                taskList.create()
            elif menuSelect=='4':
                taskList.show()
                taskList.rename(uInput.getChoice())
            elif menuSelect=='5':
                taskList.show()
                taskList.delete(uInput.getChoice())
            elif menuSelect=='exit':
                menuSelect=None
                db.commit()
                db.close()
                os.system("mysql.server stop")
            else:
                print(uInput.errorNoOption)

if __name__ == "__main__":
    main()
