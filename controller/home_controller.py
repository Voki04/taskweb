from flask import session, redirect, render_template

def homepage():
    if "user" in session:
        return render_template("home.html", username=session["user"])  # Hiển thị trang home nếu đã đăng nhập
    return redirect("/")  # Nếu chưa đăng nhập, chuyển hướng về trang chủ hoặc trang đăng nhập
