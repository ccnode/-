import datetime
from api.tools.dbtools import DB
import asyncio
async def start(loop):
    db = DB(dbname="mitucat", loop=loop)
    q_data = await db.query("select * from comments_info where "
                            "goods_id=101 order by com_date asc ")
    for i in q_data:
        date2 = i[5].date()
        print(date2+datetime.timedelta(days=1))
    # date2 = datetime.date()
    # print(date2)


loop = asyncio.get_event_loop()
loop.run_until_complete(start(loop))
loop.close()