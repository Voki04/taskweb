from flask import request, redirect, render_template ,session ,flash,jsonify
from model.task_model import TaskModel
from utils.auth import login_required
from datetime import datetime, timedelta

task_model = TaskModel()

@login_required
def task_page():
    user_id = session["user_id"]
    tasks = task_model.get_tasks(user_id)
    now = datetime.now().date()
    return render_template("task.html", tasks=tasks, now=now, timedelta=timedelta)


@login_required
def add_task():
    user_id = session["user_id"]
    name = request.form["name"]
    description = request.form.get("description", "")
    deadline = request.form.get("deadline", None)

    task_model.add_task(name, description, deadline, user_id)
    flash("✅ Đã thêm task mới!")
    return redirect("/home/task")

@login_required
def delete_task(task_id):
    task_model.delete_task(task_id)
    flash("🗑 Task đã bị xoá!")
    return redirect("/home/task")

@login_required
def update_task():
    task_id = request.form["id"]
    name = request.form["name"]
    status = 1 if "status" in request.form else 0
    task_model.update_task(task_id, name, status)
    flash("✏️ Task đã được cập nhật!")
    return redirect("/home/task")

@login_required
def toggle_status():
    task_id = request.form["task_id"]
    status = 1 if request.form["status"] == "true" else 0
    task_model.update_task(task_id, None, status)
    return {"success": True}