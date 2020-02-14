from pyppeteer import launch
import asyncio
from lxml import etree
# 拦截图片视频资源
async def inject_request(req):
    """
    resourceType:
        document, stylesheet, image, media, font, script, texttrack,
        xhr, fetch, eventsource, websocket, manifest, other
    """
    if req.resourceType in ['media','image']:
        await req.abort()
    else:
        await req.continue_()

async def inject_response(res):
    if res.request.resourceType in ['xhr']:
        print(res.request.url)

def screen_size():
    """使用tkinter获取屏幕大小"""
    import tkinter
    tk = tkinter.Tk()
    width = tk.winfo_screenwidth()
    height = tk.winfo_screenheight()
    tk.quit()
    return width, height

async def main(url,loop):
    launch_kwargs = {
        # 控制是否为无头模式
        "headless": False,
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
    # 启动浏览器
    browser = await launch(launch_kwargs)
    # 打开标签页
    page = await browser.newPage()
    # 不加载图片及视频资源
    # await page.setRequestInterception(True)
    # page.on('request', inject_request)
    # page.on('response', inject_response)
    # 网页大小
    width, height = screen_size()
    # 设置网页可视区域大小
    await page.setViewport({
        "width": width,
        "height": height
    })
    # 输入网址并打开
    await page.goto(url)
    # await page.click("a[class='main-link']")
    await page.waitFor(300)

    await page.click("div[id='comment-count']")
    await page.waitFor(2000)
    await page.hover("div[class='current']")

    await page.click("li[data-sorttype='6']")
    await page.waitFor(2000)
    el = await page.querySelector("div[id='comment-0']")
    text = await page.evaluate('(element) => element.innerHTML', el)
    html = etree.HTML(text)
    print(html)

    # 下一页
    await page.hover("a[class='ui-pager-next']")
    await page.waitFor(300)
    await page.click("a[class='ui-pager-next']")
    # 关闭页面
    # await browser.close()
    return

# url = "https://item.jd.com/1026553130.html"
url = "https://item.jd.com/8137344.html"
loop = asyncio.get_event_loop()
loop.run_until_complete(main(url,loop))