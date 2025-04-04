import mysql.connector

def connect_db():
    try:
        # B1: Kết nối MySQL chưa chọn DB để tạo DB nếu cần
        conn = mysql.connector.connect(
            host="db4free.net",
            user="voki02",
            password="Quyen02082004@",
            database="Quyen02082004@"
        )
        cursor = conn.cursor()

        # B2: Tạo database nếu chưa có
        cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
        conn.commit()
        conn.close()

        # B3: Kết nối lại với database 'mydatabase'
        conn = mysql.connector.connect(
            host="db4free.net",
            user="voki02",
            password="Quyen02082004@",
            database="Quyen02082004@"
        )

        # B4: Tạo bảng tasks nếu chưa có (sau khi đã vào đúng DB)
        cursor = conn.cursor()
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
""")
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        deadline DATE,
        status BOOLEAN NOT NULL DEFAULT 0,
        user_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
""")

        conn.commit()

        print("✅ Kết nối MySQL thành công và đã kiểm tra bảng 'tasks'.")
        return conn

    except mysql.connector.Error as err:
        print(f"❌ Lỗi kết nối: {err}")
        return None
