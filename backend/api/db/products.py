def get_all_products(db_conn, search_query: str = None, min_price: float = None, max_price: float = None, category_id: int = None):
    db, cursor = db_conn
    
    query = """
        SELECT p.*, c.name as category_name 
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE 1=1
    """
    params = []
    
    if search_query:
        query += " AND (p.name LIKE %s OR p.description LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])
        
    if min_price is not None:
        query += " AND p.price >= %s"
        params.append(min_price)
        
    if max_price is not None:
        query += " AND p.price <= %s"
        params.append(max_price)
        
    if category_id is not None:
        query += " AND p.category_id = %s"
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


def update_product(db_conn, product_id: int, name: str = None, price: float = None, category_id: int = None, description: str = None, image_url: str = None, stock: int = None):
    db, cursor = db_conn
    
    fields = []
    params = []
    
    if name is not None:
        fields.append("name = %s")
        params.append(name)
    if price is not None:
        fields.append("price = %s")
        params.append(price)
    if category_id is not None:
        fields.append("category_id = %s")
        params.append(category_id)
    if description is not None:
        fields.append("description = %s")
        params.append(description)
    if image_url is not None:
        fields.append("image_url = %s")
        params.append(image_url)
    if stock is not None:
        fields.append("stock = %s")
        params.append(stock)
        
    if not fields:
        return
        
    params.append(product_id)
    query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s"
    
    cursor.execute(query, tuple(params))
    db.commit()
    return cursor.rowcount


def delete_product(db_conn, product_id: int):
    db, cursor = db_conn
    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    db.commit()
    return cursor.rowcount
