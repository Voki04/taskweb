from flask import session, request, redirect ,flash
from model.task_model import TaskModel
from database.mysqlconnection import connect_db

def login(username, password):
    task_model = TaskModel()
    conn = connect_db()  # Chỉ gọi connect_db() một lần và nhận kết nối
    if conn is None:
        return False  # Trả về False nếu không thể kết nối database

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session["user"] = username
        session["user_id"] = user[0]  # giả sử user[0] là ID, vì SELECT * FROM users
        # Lưu tên người dùng vào session
        print("✅ Đăng nhập thành công!")
        return True
    else:
        print("❌ Sai tài khoản hoặc mật khẩu!")
        return False


def login_user():
    username = request.form["username"]
    password = request.form["password"]
    if login(username, password):
        flash("✅ Đăng nhập thành công!")
        return redirect("/home")
    flash("❌ Sai tài khoản hoặc mật khẩu!")
    return redirect("/login")