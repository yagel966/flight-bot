
from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

app = FastAPI()

class RouteRequest(BaseModel):
    telegram_id: int
    origin: str
    destination: str
    target_price: int

@app.get("/")
def root():
    return {"status": "בוט טיסות חכמות פעיל"}

@app.post("/subscribe")
def subscribe(route: RouteRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (telegram_id) VALUES (%s) ON CONFLICT (telegram_id) DO NOTHING",
        (route.telegram_id,)
    )

    cursor.execute(
        "SELECT id FROM users WHERE telegram_id = %s",
        (route.telegram_id,)
    )
    user_id = cursor.fetchone()[0]

    cursor.execute(
        "INSERT INTO routes (user_id, origin, destination, target_price) VALUES (%s, %s, %s, %s)",
        (user_id, route.origin.upper(), route.destination.upper(), route.target_price)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "נרשמת בהצלחה",
        "route": f"{route.origin.upper()} -> {route.destination.upper()}",
        "target_price": f"${route.target_price}"
    }

@app.get("/routes/{telegram_id}")
def get_routes(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.origin, r.destination, r.target_price, r.is_active
        FROM routes r
        JOIN users u ON r.user_id = u.id
        WHERE u.telegram_id = %s
        """,
        (telegram_id,)
    )
    routes = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"routes": [
        {
            "origin": r[0],
            "destination": r[1],
            "target_price": r[2],
            "active": r[3]
        } for r in routes
    ]}
