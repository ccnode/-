from lxml import etree
import time
# from spiders.jd_spider import goods_item
# 解析网页
async def parser(browser,page):
    print("下载页面。。。")
    text = await page.content()
    html = etree.HTML(text)
    t1 = time.time()

    goods_name = html.xpath("//title/text()")
    goods_price = html.xpath("//span[@class='p-price']/span[2]/text()")
    comments_num = html.xpath("//div[@id='comment-count']/a/text()")
    

    t2 = time.time()
    print("解析耗时：{}".format(t2-t1))
    print(comments_num)
    
    # 关闭浏览器
    # await page.close()
    await browser.close()


# 合并列表
async def mergeList(lists):
    str = ""
    for i in lists:
        # str +=i.replace(" ","").replace("\n","").replace("\r","")
        str +=i.strip()
    return str