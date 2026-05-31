import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_connection():
    return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
    )

def save_price(route_id, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO prices (route_id, price, currency) VALUES (%s, %s, %s)",
            (route_id, price, "USD")
    )
    conn.commit()
    cursor.close()
    conn.close()

def get_last_price(route_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT price FROM prices WHERE route_id = %s ORDER BY fetched_at DESC LIMIT 1",
            (route_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_active_routes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "SELECT id, origin, destination, target_price FROM routes WHERE is_active = TRUE"
    )
    routes = cursor.fetchall()
    cursor.close()
    conn.close()
    return routes

def save_alert(route_id, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
            "INSERT INTO alerts_sent (route_id, price) VALUES (%s, %s)",
            (route_id, price)
    )
    conn.commit()
    cursor.close()
    conn.close()
