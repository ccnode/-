from flask import render_template,jsonify,Blueprint,request
from api.tools.dbtools import DB
goods = Blueprint('goods',__name__)
db = DB("mitucat")

#商品分析页面跳转
@goods.route("/goods")
def g_analyze():
    return render_template("goods/directory.html")

# 历史记录列表
@goods.route("/g_directory",methods=["GET"])
def g_directory():
    page = int(request.args.get('page'))
    size = int(request.args.get('size'))
    if page == None:
        page = 1
    if size == None:
        size = 10
    try :
        # 取出本页数据
        res = db.query("select id,q_name,is_success,q_date from goods_query_log limit {0},{1};".format((page-1)*size,size))
        # 算出一共分几页
        totaldata = db.query("select count(*) from goods_query_log")
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

# 具体历史记录页面跳转
@goods.route("/g_history/<int:nid>",methods=["GET"])
def g_history(nid):
    
    return str(nid)
#测试
# @goods.route("/hai")
# def hai():
#     res = db.query("select * from user_info")
#     data = {
#         "data": res,
#         "msg" : "查询成功！",
#         "status" : "200"
#     }
#     return jsonify(data)

