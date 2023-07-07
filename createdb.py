# import mysql.connector

# mydb = mysql.connector.connect(
#     host= 'localhost',
#     user= 'root',
#     passwd = "2004",
# )

# my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE codebase")

# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#     print(db)


### RUN A DB MIGRATION

# flask db init

# flask db migrate -m "DB MESSAGE"

# flask db upgrade
