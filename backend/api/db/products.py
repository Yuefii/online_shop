def get_all_products(db_conn, search_query: str = None, min_price: float = None, max_price: float = None, category_id: int = None):
    db, cursor = db_conn
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if search_query:
        query += " AND (name LIKE %s OR description LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
        
    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)
        
    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)
        
    if category_id is not None:
        query += " AND category_id = %s"
        params.append(category_id)
        
    cursor.execute(query, tuple(params))
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
