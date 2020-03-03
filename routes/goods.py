from flask import render_template,jsonify,Blueprint,request,session,redirect,url_for
from api.tools.front_dbtools import DB
from api.jd_spiders.spider.goods_info import goods_info
import asyncio
import threading
goods = Blueprint('goods',__name__)
db = DB("mitucat")


#商品分析页面跳转
@goods.route("/goods")
def g_analyze():
    if check_login()!=True:
        return redirect(url_for("user.login_page"))
    username = session["username"]
    return render_template("goods/directory.html",username=username)


# 历史记录列表
@goods.route("/g_directory",methods=["GET"])
def g_directory():
    if check_login() != True:
        return redirect(url_for("user.login_page"))
    user_id = session["user_id"]
    page = int(request.args.get('page'))
    size = int(request.args.get('size'))
    if page == None:
        page = 1
    if size == None:
        size = 10
    try :
        # 取出本页数据
        res = db.query("select id,q_name,is_success,q_date from goods_query_log "
                       "where user_id={0} limit {1},{2};".format(user_id,(page-1)*size,size))
        # 算出一共分几页
        totaldata = db.query("select count(*) from goods_query_log where user_id={}".format(user_id))
        totalPage = (totaldata[0][0]+size-1)/size
        totalPage = int(totalPage)
        # 数据合并
    except Exception as e:
        print("sql错误！原因{}".format(e))
        data = {
            "msg" : "查询失败",
            "status" : "500"
        }
        return jsonify(data)
    data = {
        "data": res,
        "totalPage" : totalPage,
        "msg" : "查询成功",
        "status" : "200"
    }
    return jsonify(data)

async def test():
    print("wo")

# 新建商品分析
@goods.route("/goods",methods=["GET","POST"])
def getNewAnalys():
    if request.method == 'POST':
        url = request.form.get('url')
        user_id = session["user_id"]
        # 建立爬虫
        spider = goods_info(url="https://item.jd.com/1026553130.html", num=32, q_id=11)
        try:
            pass
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(spider.start(loop))
            # loop.close()
        except:
            print("Error: 无法启动爬虫")
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(spider.geturl())
        loop.close()
        # threading.Thread(target=spider.start).start()



    return  redirect(url_for('goods.g_analyze'))


# 具体历史记录页面跳转
@goods.route("/g_history/<int:nid>",methods=["GET"])
def g_history(nid):
    if check_login()!=True:
        return redirect(url_for("user.login_page"))

    return str(nid)


# 检验登录
def check_login():
    try:
        session["username"]
        return True
    except:
        print("未登录")
        return False
