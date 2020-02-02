from tools.dbtools import DB
size = 3
page = 1
db = DB("127.0.0.1","root","","mitucat")
# 取出本页数据
# res = db.query("select q_name,is_success,q_date from goods_query_log limit {0},{1};".format((page-1)*size,size))
# 算出一共分几页
totaldata = db.query("select count(*) from goods_query_log")
totalPage = (0+size-1)/size
 # 数据合并
print(int(totalPage))