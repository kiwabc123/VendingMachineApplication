import uuid

# runtime session (ยังไม่ลง DB)
VENDING_SESSION = {}

def create_session(product_id: int, price: int):
    session_id = str(uuid.uuid4())
    VENDING_SESSION[session_id] = {
        "product_id": product_id,
        "price": int(price),
        "paid": 0,
        "confirmed": False
    }
    return session_id
