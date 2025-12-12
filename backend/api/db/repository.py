


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