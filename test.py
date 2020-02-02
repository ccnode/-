size = 2
page = 3

print("select q_name,is_success,q_date from goods_query_log limit "+str((page-1)*size)+","+str(size))