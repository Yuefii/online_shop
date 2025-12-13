def get_all_categories(db_conn, search_query: str = None, limit: int = None, offset: int = None):
    db, cursor = db_conn
    query = "SELECT * FROM categories WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE %s OR slug LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
    
    if limit is not None:
        query += " LIMIT %s"
        params.append(limit)
        
    if offset is not None:
        query += " OFFSET %s"
        params.append(offset)

    cursor.execute(query, tuple(params))
    return cursor.fetchall()


def count_categories(db_conn, search_query: str = None):
    db, cursor = db_conn
    query = "SELECT COUNT(*) FROM categories WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE %s OR slug LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    cursor.execute(query, tuple(params))
    return cursor.fetchone()['COUNT(*)']


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


def update_category(db_conn, category_id: int, name: str = None, slug: str = None):
    db, cursor = db_conn
    fields = []
    params = []

    if name is not None:
        fields.append("name = %s")
        params.append(name)
    if slug is not None:
        fields.append("slug = %s")
        params.append(slug)
    
    if not fields:
        return 0

    params.append(category_id)
    query = f"UPDATE categories SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, tuple(params))
    db.commit()
    return cursor.rowcount


def delete_category(db_conn, category_id: int):
    db, cursor = db_conn
    cursor.execute("DELETE FROM categories WHERE id=%s", (category_id,))
    db.commit()
    return cursor.rowcount
