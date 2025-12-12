def get_all_products(db_conn):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def get_product_by_id(db_conn, product_id: int):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM products WHERE id=%s", (product_id,))
    return cursor.fetchone()


def create_product(db_conn, name: str, price: float, category_id: int, description: str = None, image_url: str = None, stock: int = 0):
    db, cursor = db_conn
    cursor.execute(
        """
        INSERT INTO products (name, description, price, image_url, stock, category_id) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (name, description, price, image_url, stock, category_id)
    )
    db.commit()
    return cursor.lastrowid
