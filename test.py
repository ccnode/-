size = 2
page = 3

print("select q_name,is_success,_date from goods_query_lo limit "+str((page-1)*size)+","+str(size))