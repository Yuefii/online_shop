from api.db.cart import get_cart_by_user_id

def create_order(db_conn, user_id: int, shipping_address: str):
    db, cursor = db_conn
    
    # 1. Get User's Cart
    cart = get_cart_by_user_id(db_conn, user_id)
    cart_items = cart['items']
    
    if not cart_items:
        raise ValueError("Cart is empty")
        
    total_price = cart['total_price']
    
    # 2. Create Order
    cursor.execute(
        "INSERT INTO orders (user_id, total_price, status, shipping_address) VALUES (%s, %s, %s, %s)",
        (user_id, total_price, 'pending', shipping_address)
    )
    order_id = cursor.lastrowid
    
    # 3. Create Order Items (Copy from Cart)
    for item in cart_items:
        product = item['product']
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
            (order_id, product['id'], item['quantity'], product['price'])
        )
        
    # 4. Clear Cart
    cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart['id'],))
    
    db.commit()
    return get_order_by_id(db_conn, order_id)

def get_orders_by_user(db_conn, user_id: int):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    orders = cursor.fetchall()
    
    # Fetch items for all orders (naive N+1 constraint for now, optimization later if needed)
    result = []
    for order in orders:
        order['items'] = get_order_items(db_conn, order['id'])
        result.append(order)
        
    return result

def get_order_by_id(db_conn, order_id: int):
    db, cursor = db_conn
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    if order:
         order['items'] = get_order_items(db_conn, order_id)
    return order

def get_order_items(db_conn, order_id: int):
    db, cursor = db_conn
    # Join with products to get current name (or snapshot if we stored it, but we only have ID)
    # Ideally order_items should have snapshot data, but for now we pull from products.
    # If product deleted, name comes up null or need left join.
    query = """
        SELECT oi.*, p.name as product_name
        FROM order_items oi
        LEFT JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
    """
    cursor.execute(query, (order_id,))
    return cursor.fetchall()

def get_all_orders(db_conn, search_query: str = None):
    db, cursor = db_conn
    
    if search_query:
        # Check if query is a number (for ID search)
        if search_query.isdigit():
            # Search by ID or Status
             cursor.execute(
                "SELECT * FROM orders WHERE id = %s OR status LIKE %s ORDER BY created_at DESC", 
                (int(search_query), f"%{search_query}%")
            )
        else:
             cursor.execute(
                "SELECT * FROM orders WHERE status LIKE %s ORDER BY created_at DESC", 
                (f"%{search_query}%",)
            )
    else:
        cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    
    orders = cursor.fetchall()
    # Populate items? For admin listing usually summary is enough, but user might expand. 
    # Let's keep it consistent.
    result = []
    for order in orders:
        order['items'] = get_order_items(db_conn, order['id'])
        result.append(order)
    return result

def update_order_status(db_conn, order_id: int, status: str):
    db, cursor = db_conn
    cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (status, order_id))
    db.commit()
    if cursor.rowcount == 0:
        return None
    return get_order_by_id(db_conn, order_id)


def get_order_stats(db_conn):
    db, cursor = db_conn
    cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status IN ('pending', 'processing')")
    result = cursor.fetchone()
    return {"pending_count": result['count'] if result else 0}
