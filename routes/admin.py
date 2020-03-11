from flask import render_template,jsonify,Blueprint,request,session,redirect,url_for,flash
from api.tools.front_dbtools import DB
from api.data_analysis.goods_analysis import goods_analysis
import time
from api.jd_spiders.crow_goods import crow_goods
import asyncio
import threading
admin = Blueprint('admin',__name__)
db = DB("mitucat")

@admin.route("/rewards")
def rewards():
    return render_template("admin/rewards.html")

# 管理页面
@admin.route("/admin_page")
def admin_page():
    return render_template("admin/admin.html")
# 加载公告编辑
@admin.route("/edit_rewards")
def edit_rewards():
    username = session["username"]
    return render_template("admin/edit_rewards.html",username=username)

# 加载用户管理
@admin.route("/user_manage")
def user_manage():
    username = session["username"]
    return render_template("admin/user_manage.html",username=username)