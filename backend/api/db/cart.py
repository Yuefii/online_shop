def get_cart_by_user_id(db_conn, user_id: int):
    db, cursor = db_conn
    
    # 1. Get or Create Cart
    cursor.execute("SELECT * FROM carts WHERE user_id = %s", (user_id,))
    cart = cursor.fetchone()
    
    if not cart:
        cursor.execute("INSERT INTO carts (user_id) VALUES (%s)", (user_id,))
        db.commit()
        cart_id = cursor.lastrowid
        cursor.execute("SELECT * FROM carts WHERE id = %s", (cart_id,))
        cart = cursor.fetchone()
    
    cart_id = cart['id']
    
    # 2. Get Items with Product Details
    query = """
        SELECT ci.id, ci.quantity, ci.cart_id, 
               p.id as product_id, p.name, p.description, p.price, p.image_url, p.stock, p.category_id, p.created_at
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.cart_id = %s
    """
    cursor.execute(query, (cart_id,))
    rows = cursor.fetchall()
    
    items = []
    total_price = 0
    
    for row in rows:
        product = {
            "id": row['product_id'],
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "image_url": row['image_url'],
            "stock": row['stock'],
            "category_id": row['category_id'],
            "created_at": row['created_at']
        }
        item_total = row['price'] * row['quantity']
        total_price += item_total
        
        items.append({
            "id": row['id'],
            "product": product,
            "quantity": row['quantity']
        })
        
    return {
        "id": cart_id,
        "user_id": user_id,
        "items": items,
        "total_price": total_price
    }

def add_to_cart(db_conn, user_id: int, product_id: int, quantity: int):
    db, cursor = db_conn
    
    # Ensure cart exists
    cart = get_cart_by_user_id(db_conn, user_id)
    cart_id = cart['id']
    
    # Check if item exists in cart
    cursor.execute("SELECT * FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
    existing_item = cursor.fetchone()
    
    if existing_item:
        new_quantity = existing_item['quantity'] + quantity
        if new_quantity <= 0:
             cursor.execute("DELETE FROM cart_items WHERE id = %s", (existing_item['id'],))
        else:
             cursor.execute("UPDATE cart_items SET quantity = %s WHERE id = %s", (new_quantity, existing_item['id']))
    else:
        if quantity > 0:
            cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)", (cart_id, product_id, quantity))
            
    db.commit()
    return get_cart_by_user_id(db_conn, user_id)

def remove_from_cart(db_conn, user_id: int, item_id: int):
    db, cursor = db_conn
    # Verify item belongs to user's cart
    cart = get_cart_by_user_id(db_conn, user_id)
    cart_id = cart['id']
    
    cursor.execute("DELETE FROM cart_items WHERE id = %s AND cart_id = %s", (item_id, cart_id))
    db.commit()
    return get_cart_by_user_id(db_conn, user_id)
