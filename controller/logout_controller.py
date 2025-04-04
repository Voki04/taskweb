from flask import session, redirect

def logout_user():
    session.pop("user", None)
    return redirect("/")
