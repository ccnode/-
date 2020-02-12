from tools.mysqltools import DB

db = DB(dbname="mitucat")


print(db.query("select * from user_info"))

