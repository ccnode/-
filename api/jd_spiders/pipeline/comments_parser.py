from lxml import etree
import time
import asyncio

# 解析商品页面
async def parser(page,num,goods_id):
    # 点击评价数跳转
    await page.hover("li[data-anchor='#comment']")
    await asyncio.sleep(0.3)
    await page.click("li[data-anchor='#comment']")
    await page.waitFor(1000)
    await asyncio.sleep(1.5)
    # 点击时间排序
    await page.hover("span[class='J-current-sortType']")
    # await page.waitFor(300)
    await page.click("li[data-sorttype='6']")
    await page.waitFor(500)
    print("开始爬取评论。。。")
    sql = await getData(page,num,goods_id)
    return sql

async def getData(page,num,goods_id):
    data = ""
    count = 0
    while True:
        # 获取评论的全部标签
        el = await page.querySelector("div[id='comment-0']")
        text = await page.evaluate('(element) => element.innerHTML', el)
        html = etree.HTML(text)
        # 获取数据
        com_user_names = html.xpath("//div[@class='user-info']/img/@alt")
        stars = html.xpath("//div[@class='comment-column J-comment-column']/div[1]/@class")
        contents = html.xpath("//p[@class='comment-con']/text()")
        com_dates = html.xpath("//div[@class='order-info']/span[last()]/text()")
        # 解析并编写sql
        for i in range(len(com_user_names)):
            com_user_name = com_user_names[i]
            # 取星级最后一个字符
            star = (stars[i])[-1]
            content = (contents[i]).strip()
            com_date = com_dates[i]
            if count == num - 1:
                data += "({},'{}','{}',{},'{}');".format(goods_id, com_user_name, content, star, com_date)
                count += 1
                break
            else:
                data += "({},'{}','{}',{},'{}'),".format(goods_id, com_user_name, content, star, com_date)
            # 计数器+1
            count += 1
        print("已爬取：{}条评论".format(count))
        if count == num:
            break
        # 翻页
        await asyncio.sleep(1)
        await page.hover("a[class='ui-pager-next']")
        await page.waitFor(300)
        await page.click("a[class='ui-pager-next']")
    sql = "insert into comments_info(goods_id,com_user_name,content,star,com_date) values" + data
    return sql