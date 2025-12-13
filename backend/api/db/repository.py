


def get_user_by_email(db_conn, email: str):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cursor.fetchone()


def create_user(db_conn, email: str, password: str, full_name: str = None):
    db, cursor = db_conn
    cursor.execute(
        "INSERT INTO users (email, password, full_name) VALUES (%s, %s, %s)", 
        (email, password, full_name)
    )
    db.commit()
    return cursor.lastrowid


def get_all_users(db_conn, search_query: str = None):
    db, cursor = db_conn
    if search_query:
        search_param = f"%{search_query}%"
        cursor.execute(
            "SELECT id, email, full_name, role, is_active, created_at FROM users WHERE email LIKE %s OR full_name LIKE %s", 
            (search_param, search_param)
        )
    else:
        cursor.execute("SELECT id, email, full_name, role, is_active, created_at FROM users")
    return cursor.fetchall()


def update_user_role(db_conn, user_id: int, role: str):
    db, cursor = db_conn
    cursor.execute("UPDATE users SET role = %s WHERE id = %s", (role, user_id))
    db.commit()
    return cursor.rowcount > 0