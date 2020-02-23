import time,datetime
now = datetime.datetime.now()

now_time = int(time.mktime(now.timetuple()))

now = datetime.datetime.fromtimestamp(now_time)
print(now,now_time)