from flask import Flask, render_template, request, redirect, session ,get_flashed_messages

from controller.regis_controller import register_user
from controller.login_controller import login_user
from database.mysqlconnection import connect_db
from controller.home_controller import homepage
from controller.logout_controller import logout_user
import controller
from model.task_model import TaskModel
from utils.auth import login_required
from controller.task_controller import task_page, add_task, delete_task, update_task ,toggle_status


app = Flask(__name__, static_folder="view/static", template_folder="view/templates")
app.secret_key = "supersecretkey"  # Cần thiết để dùng session

task_model = TaskModel()
task_model.create_database()
task_model.create_table()
# Khởi tạo database & bảng khi chạy

#Login logout main code
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/regis", methods=["GET", "POST"])
def regis():
    if request.method == "POST":
        return register_user()
    return render_template("regis.html")  # Gọi logic đăng ký từ controller

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return login_user()  # Gọi hàm xử lý đăng nhập
    return render_template("login.html")   # Gọi logic đăng nhập từ controller

@app.route("/logout")
def logout():
    return logout_user()

@app.route("/home")
@login_required # authecation nha
def home():
    return homepage()

#task main code
@app.route("/home/task")
@login_required
def task():
    return task_page()

@app.route("/home/task/add", methods=["POST"])
@login_required
def task_add():
    return add_task()

@app.route("/home/task/update", methods=["POST"])
@login_required
def task_update():
    return update_task()

@app.route("/home/task/delete/<int:task_id>", methods=["POST"])
@login_required
def task_delete(task_id):
    return delete_task(task_id)

@app.route("/home/task/toggle", methods=["POST"])
def task_toggle():
    return toggle_status()



if __name__ == "__main__":
    from os import getenv
    port = int(getenv("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
