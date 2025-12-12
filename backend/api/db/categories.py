def get_all_categories(db_conn):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM categories")
    return cursor.fetchall()


def get_category_by_id(db_conn, category_id: int):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM categories WHERE id=%s", (category_id,))
    return cursor.fetchone()


def create_category(db_conn, name: str, slug: str):
    db, cursor = db_conn
    cursor.execute(
        "INSERT INTO categories (name, slug) VALUES (%s, %s)",
        (name, slug)
    )
    db.commit()
    return cursor.lastrowid
