from pyppeteer import launch
import asyncio

import time
from api.tools.dbtools import DB

class keyword_info():
    async def screen_size(self):
        """使用tkinter获取屏幕大小"""
        import tkinter
        tk = tkinter.Tk()
        width = tk.winfo_screenwidth()
        height = tk.winfo_screenheight()
        tk.quit()
        return width, height

    # 初始化参数
    def __init__(self,url,num):
        self.url = url
        self.num = num
        self.launch_kwargs = {
            # 控制是否为无头模式
            "headless": False,
            # chrome启动命令行参数
            "dumpio": True,
            "autoClose": False,
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
    # 启动协程
    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.geturl())

    # 启动浏览器
    async def geturl(self):
        print("正在启动~")
        width, height = await self.screen_size()
        t1 = time.time()
        # 启动浏览器
        self.browser = await launch(self.launch_kwargs)
        self.page = await self.browser.newPage()
        # 设置网页可视区域大小
        await self.page.setViewport({
            "width": width,
            "height": height
        })
        # 输入网址并打开
        await self.page.goto(self.url)
        print("加载页面~{}".format(time.time() - t1))
        # 调用主体方法
        for i in range(2):
            try:
                await self.main()
            except Exception as e:
                print("发生错误：{}----正在重试{}".format(e, i + 1))
    # 主体方法
    async def main(self):
        # 创建数据库实例
        db = DB(dbname="mitucat", loop=self.loop)

        # 调用爬取商品信息方法
        sql = await g.parser(self.page,self.url,self.num)
        print(sql)

        # 插入商品信息获取id
        goods_id = (await db.commits(sql))[0][0]

        # 调用爬取评论方法
        comSql = await c.parser(self.page, self.num, goods_id)
        await db.commit(comSql)

        # 关闭页面
        # await self.page.close()
        await self.browser.close()
        return

if __name__ == '__main__':
    try:
        spider = keyword_info(url="https://item.jd.com/1026553130.html", num=30)
        print(spider.start())
        print("success")
    except Exception as e:
        print(e)

# https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&psort=3