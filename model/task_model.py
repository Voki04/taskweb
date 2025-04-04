import mysql.connector
from mysql.connector import Error
from datetime import datetime

class TaskModel:
    def __init__(self):
        self.connection = None

    def create_connection(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="123456",
                    database="mydatabase"  # Đảm bảo trùng với tên DB bạn đang dùng
                )
                if self.connection.is_connected():
                    print("✅ Đã kết nối đến MySQL")
            except Error as e:
                print(f"❌ Lỗi kết nối MySQL: {e}")

    def create_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456"
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
            print("✅ Database 'mydatabase' đã được tạo hoặc đã tồn tại.")
            cursor.close()
            conn.close()
        except Error as e:
            print(f"❌ Lỗi tạo database: {e}")

    def create_table(self):
        try:
            self.create_connection()
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    status BOOLEAN NOT NULL DEFAULT 0,
                    user_id INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("✅ Bảng 'tasks' đã được tạo hoặc đã tồn tại.")
            cursor.close()
        except Error as e:
            print(f"❌ Lỗi tạo bảng: {e}")

    def get_tasks(self, user_id):
        try:
            self.create_connection()
            cursor = self.connection.cursor(dictionary=True)

            cursor.execute("""
                SELECT * FROM tasks
                WHERE user_id = %s
                ORDER BY 
                    status ASC,
                    CASE WHEN deadline IS NULL THEN 1 ELSE 0 END,
                    deadline ASC
            """, (user_id,))
            
            tasks = cursor.fetchall()
            
            # Format lại deadline về dạng date object
            for task in tasks:
                if task["deadline"]:
                    task["deadline"] = datetime.strptime(str(task["deadline"]), "%Y-%m-%d").date()

            return tasks
        except Exception as e:
            print(f"❌ Lỗi lấy task: {e}")
            return []
    
    def add_task(self, name, description, deadline, user_id):
        try:
            self.create_connection()
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO tasks (name, description, deadline, user_id) VALUES (%s, %s, %s, %s)",
                (name, description, deadline, user_id)
            )
            self.connection.commit()
            cursor.close()
            print("✅ Task mới đã được thêm.")
        except Exception as e:
            print(f"❌ Lỗi thêm task: {e}")

    def update_task(self, task_id, name=None, status=None):
        try:
            self.create_connection()
            cursor = self.connection.cursor()

            if name is not None and status is not None:
                cursor.execute("UPDATE tasks SET name = %s, status = %s WHERE id = %s", (name, status, task_id))
            elif name is not None:
                cursor.execute("UPDATE tasks SET name = %s WHERE id = %s", (name, task_id))
            elif status is not None:
                cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))

            self.connection.commit()
            cursor.close()
            print("✅ Cập nhật task thành công.")
        except Exception as e:
            print(f"❌ Lỗi cập nhật: {e}")

    def delete_task(self, task_id):
        try:
            self.create_connection()
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.connection.commit()
            cursor.close()
            print("🗑 Task đã bị xoá.")
        except Exception as e:
            print(f"❌ Lỗi xoá task: {e}")