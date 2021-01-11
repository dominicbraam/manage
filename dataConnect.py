import mysql.connector
from mysql.connector import errorcode

try:
    db = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="01000100",
        database="manage_tasks"
    )
    cursor = db.cursor(buffered=True)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

