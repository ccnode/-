from collections import Counter

a = ["1","2","2","1"]

#统计列表中重复次数最多的前N个元素
N = 3

print(Counter(a).most_common(N))



#输出是[(4, 4), (1, 3), (3, 2)]