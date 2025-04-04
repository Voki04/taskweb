# controller/regis_controller.py
from controller.login_controller import login
from model.task_model import TaskModel
from database.mysqlconnection import connect_db
from flask import request, redirect ,flash

def register(username, password):
    task_model = TaskModel()
    conn = connect_db()

    if conn is None:
        flash("❌ Không thể kết nối đến database!")
        return False

    cursor = conn.cursor()
    try:
        # 🔍 Kiểm tra username đã tồn tại chưa
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("❌ Tên đăng nhập đã tồn tại!")
            return False

        # ✅ Nếu chưa tồn tại, tiến hành đăng ký
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        print("✅ Đăng ký thành công!")
        return True

    except Exception as e:
        print(f"❌ Lỗi đăng ký: {e}")
        flash("❌ Lỗi đăng ký: " + str(e))
        return False

    finally:
        conn.close()

def register_user():
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # Kiểm tra mật khẩu có khớp không
    if password != confirm_password:
        flash("❌ Mật khẩu và xác nhận mật khẩu không trùng khớp!")
        return redirect("/regis")

    if register(username, password):
        flash("✅ Đăng ký thành công!")
        return redirect("/")
    else:
        flash("❌ Đăng ký thất bại!")
        return redirect("/regis")
