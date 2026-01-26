from database.db_connection import db

if db.connect():
    print("DB OK")
else:
    print("DB FAIL")
