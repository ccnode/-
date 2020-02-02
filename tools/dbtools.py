import pymysql

class DB():
    def __init__(self,host,username,password,dbname):
        self.host =host
        self.username = username
        self.password = password
        self.dbname = dbname
    def query(self,sql):
         # 1、连接数据库
        db = pymysql.connect(host=self.host,user=self.username,password=self.password,db=self.dbname)
        # 2、获取数据库游标（就是光标）
        cursor = db.cursor()
         # 3、在游标中执行SQL语句,可以执行insert update delete
        cursor.execute(sql)
        # 4、应用
        res = cursor.fetchall()
        # 5、关闭数据库连接
        db.close()
        return res
        
    def commit(self,sql):   
        # 1、连接数据库
        db = pymysql.connect(host=self.host,user=self.username,password=self.password,db=self.dbname)
        # 2、获取数据库游标（就是光标）
        cursor = db.cursor()
        # 3、在游标中执行SQL语句,可以执行insert update delete
        cursor.execute(sql)
        # 4、应用
        db.commit()
        # 5、关闭数据库连接
        db.close()
    

# 测试
# db = DB("127.0.0.1","root","","mitucat")
# print(db.query("select * from user_info"))