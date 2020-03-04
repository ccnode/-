from flask import Flask,render_template,session,redirect,url_for,request,flash
import os
from routes.goods import goods
from routes.user import user
import re
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

#添加其他蓝图到主体
app.register_blueprint(goods)
app.register_blueprint(user)

def check_login():
    try:
        session["username"]
        return True
    except:
        print("未登录")
        return False

# 首页跳转
@app.route("/")
def index():
    if check_login()!=True:
        # return render_template("user/login.html")
        return redirect(url_for("user.login_page"))
    user_id = session["username"]
    return render_template("index.html",user_id=user_id)
    # return render_template("user/login.html")


#关键词分析
@app.route("/keyword")
def k_analyze():
    if check_login() != True:
        return redirect(url_for("user.login_page"))
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
      port=5013,
      debug=True)