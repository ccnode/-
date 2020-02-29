from flask import Flask,render_template,jsonify,Blueprint

from api.routes.goods import goods

app = Flask(__name__)

#添加其他蓝图到主体
app.register_blueprint(goods)


# 首页跳转
@app.route("/")
def index():
    return render_template("index.html")



#关键词分析
@app.route("/keyword")
def k_analyze():
    return render_template("keyword/directory.html")
# @app.route("/hai")
# def hai():
#     res = db.query("select * from user_info")
#     data = {
#         "data": res,
#         "msg" : "查询成功！",
#         "status" : "200"
#     }
#     return jsonify(data)


if __name__ == "__main__":
    # debug=True
     app.run(
      host='127.0.0.1',
      port= 5035,
      debug=True
    )