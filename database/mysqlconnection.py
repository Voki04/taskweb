import mysql.connector

def connect_db():
    try:
        # Kết nối tới DB được cấp sẵn
        conn = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12771357",
            password="ZGpzfNAyyq",
            database="sql12771357",
            port=3306
        )

        cursor = conn.cursor()

        # Tạo bảng nếu chưa có
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
        print("✅ Đã kết nối đến database và tạo bảng nếu chưa có.")
        return conn

    except mysql.connector.Error as err:
        print(f"❌ Lỗi kết nối: {err}")
        return None
