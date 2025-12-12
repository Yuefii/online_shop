import mysql.connector
from api.core.config import DB_CONFIG


def get_db():
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor(dictionary=True)
    try:
        yield db, cursor
    finally:
        cursor.close()
        db.close()