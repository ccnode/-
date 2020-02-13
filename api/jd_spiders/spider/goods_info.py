from pyppeteer import launch
import asyncio
from api.jd_spiders.pipeline import  goods_parser as p
import time
from api.tools.dbtools import DB
async def main(url,loop):
    launch_kwargs = {
        # 控制是否为无头模式
        "headless": True,
        # chrome启动命令行参数
        "dumpio":True, 
        "autoClose":False,
        "args": [
            # 浏览器代理 配合某些中间人代理使用
            # "--proxy-server=http://127.0.0.1:8008",
            # 最大化窗口
            # "--start-maximized",
            # 隐藏自动脚本
            "--enable-automation",
            # 取消沙盒模式 
            "--no-sandbox",
            # 不显示信息栏 
            "--disable-infobars",
            # log等级设置 在某些不是那么完整的系统里 如果使用默认的日志等级 可能会出现一大堆的warning信息
            "--log-level=3",
            # "–window-size=1366,850",
            # 设置UA
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        ],
        # 用户数据保存目录
        "userDataDir": "",
    }
    t1 = time.time()
    # 启动浏览器
    browser = await launch(launch_kwargs)
    # 打开标签页
    page = await browser.newPage()
    # 输入网址并打开
    await page.goto(url)
    print("跳转{}".format(time.time()-t1))
    # 创建数据库实例
    db = DB(dbname="mitucat",loop=loop)
    # 调用处理页面方法
    await p.parser(browser,page,url,db)
    return

# url = "https://item.jd.com/1026553130.html"
url = "https://item.jd.com/100002432068.html"
loop = asyncio.get_event_loop()
loop.run_until_complete(main(url,loop))
