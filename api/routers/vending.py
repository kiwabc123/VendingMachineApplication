from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from models import Product, MoneyStock, Transaction
from deps import get_db
from session_store import VENDING_SESSION, create_session

router = APIRouter(
    tags=["Vending"]
)

# Pydantic models for requests
class SelectProductRequest(BaseModel):
    product_id: int

class InsertMoneyRequest(BaseModel):
    session_id: str
    denom: int

class ConfirmRequest(BaseModel):
    session_id: str

# POST /select-product
@router.post("/select-product")
def select_product(request: SelectProductRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == request.product_id, Product.stock_qty > 0).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not available")
    
    session_id = create_session(product.id, product.price)
    return {
        "session_id": session_id,
        "product": {
            "id": product.id,
            "name": product.name,
            "price": int(product.price)
        },
        "inserted_amount": 0
    }

# POST /insert-money
@router.post("/insert-money")
def insert_money(request: InsertMoneyRequest, db: Session = Depends(get_db)):
    if request.session_id not in VENDING_SESSION:
        raise HTTPException(status_code=400, detail="INVALID_SESSION")
    
    session = VENDING_SESSION[request.session_id]
    if session.get("confirmed"):
        raise HTTPException(status_code=400, detail="Session already confirmed")
    
    # Check valid denom
    valid_denoms = [1, 5, 10, 20, 50, 100, 500, 1000]
    if request.denom not in valid_denoms:
        raise HTTPException(status_code=400, detail="Invalid denomination")
    
    # Check if machine accepts this denom
    money_stock = db.query(MoneyStock).filter(MoneyStock.denom == request.denom).first()
    if not money_stock:
        raise HTTPException(status_code=400, detail="Denomination not accepted")
    
    session["paid"] += request.denom
    money_stock.quantity += 1  
    
    status = "NOT_ENOUGH"
    if session["paid"] >= session["price"]:
        status = "ENOUGH" if session["paid"] == session["price"] else "EXCESS"
    
    db.commit()
    
    return {
        "inserted_amount": session["paid"],
        "price": session["price"],
        "status": status
    }

# POST /confirm
@router.post("/confirm")
def confirm_purchase(request: ConfirmRequest, db: Session = Depends(get_db)):
    if request.session_id not in VENDING_SESSION:
        raise HTTPException(status_code=400, detail="INVALID_SESSION")
    
    session = VENDING_SESSION[request.session_id]
    if session.get("confirmed"):
        raise HTTPException(status_code=400, detail="Session already confirmed")
    
    product = db.query(Product).filter(Product.id == session["product_id"]).first()
    if not product or product.stock_qty <= 0:
        raise HTTPException(status_code=400, detail="Product out of stock")
    
    if session["paid"] < session["price"]:
        raise HTTPException(status_code=400, detail={
            "error": "NOT_ENOUGH_MONEY",
            "paid": session["paid"],
            "price": session["price"]
        })
    
    change_amount = session["paid"] - session["price"]
    
    # Calculate change
    change_detail = []
    remaining_change = change_amount
    if remaining_change > 0:
        # Get available money stocks sorted by denom descending
        money_stocks = db.query(MoneyStock).order_by(MoneyStock.denom.desc()).all()
        for stock in money_stocks:
            if remaining_change >= stock.denom and stock.quantity > 0:
                qty = min(remaining_change // stock.denom, stock.quantity)
                if qty > 0:
                    change_detail.append({"denom": stock.denom, "qty": qty})
                    remaining_change -= qty * stock.denom
                    stock.quantity -= qty
        if remaining_change > 0:
            raise HTTPException(status_code=400, detail={"error": "INSUFFICIENT_CHANGE"})
    
    # Update product stock
    product.stock_qty -= 1
    
    # Record transaction
    transaction = Transaction(
        product_id=product.id,
        paid_amount=session["paid"],
        change_amount=change_amount
    )
    db.add(transaction)
    db.commit()
    
    session["confirmed"] = True
    
    return {
        "status": "SUCCESS",
        "product": {
            "id": product.id,
            "name": product.name
        },
        "paid": session["paid"],
        "price": session["price"],
        "change": change_amount,
        "change_detail": change_detail,
        "remaining_stock": product.stock_qty
    }

# GET /money-stock
@router.get("/money-stock")
def get_money_stock(db: Session = Depends(get_db)):
    money_stocks = db.query(MoneyStock).order_by(MoneyStock.denom).all()
    return [
        {
            "denom": stock.denom,
            "quantity": stock.quantity,
            "type": stock.type
        }
        for stock in money_stocks
    ]