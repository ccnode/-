import asyncio
import aiomysql

class DB():
    def __init__(self,dbname,loop,host="127.0.0.1",username="root",password="",port=3306):
        self.host =host
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = port
        self.loop = loop
        # self.loop = asyncio.get_event_loop()
    # 查询   
    async def query(self,sql):
        res = await self.execute(sql, 0)
        return res
        
    #修改，删除，增加
    async def commit(self,sql):
        res = await self.execute(sql, 1)
        return res

    async def execute(self,sql,n):
        conn = await aiomysql.connect(host=self.host, port=self.port,
                                        user=self.username, password=self.password, db=self.dbname,
                                        loop=self.loop)
        cur = await conn.cursor()
        await cur.execute(sql)
        if n==0:
            # 返回查询结果
            r = await cur.fetchall()
            await cur.close()
            conn.close()
            return r
        else:

            await conn.commit()
            await cur.close()
            conn.close()
            return "success"