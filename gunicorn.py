import multiprocessing
import sys
# 监听端口
bind = "0.0.0.0:8000"
# 并行工作进程数，默认 1
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 1
# 设置守护进程【关闭连接时，程序仍在运行】
# daemon = True
# 工作模式协程
worker_classes = 'gevent'
# 设置最大并发量
worker_connections = 2000
# gunicorn  要切换到的目的工作目录
chdir = '/root/MituCat'
# 超时判断, 单位为 s ， 默认 30
timeout = 30
# 设置访问日志和错误信息日志路径
# accesslog = './logs/acess.log'
# errorlog = './logs/error.log'











