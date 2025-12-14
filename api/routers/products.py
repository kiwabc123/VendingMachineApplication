from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from models import Product
from deps import get_db

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# Pydantic models
class ProductCreate(BaseModel):
    name: str
    price: int
    stock_qty: int
    slot_no: str
    image_url: str = None

class ProductUpdate(BaseModel):
    name: str = None
    price: int = None
    stock_qty: int = None
    slot_no: str = None
    image_url: str = None

# GET /products
@router.get("")
def list_products(db: Session = Depends(get_db)):
    products = (
        db.query(Product)
        .filter(Product.stock_qty > 0)
        .all()
    )

    return [
        {
            "id": p.id,
            "slot_no": p.slot_no,
            "name": p.name,
            "price": int(p.price),
            "stock": p.stock_qty,
            "image_url": p.image_url,
        }
        for p in products
    ]

# GET /products/all (including out of stock)
@router.get("/all")
def list_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [
        {
            "id": p.id,
            "slot_no": p.slot_no,
            "name": p.name,
            "price": int(p.price),
            "stock": p.stock_qty,
            "image_url": p.image_url,
        }
        for p in products
    ]

# GET /products/{id}
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product.id,
        "slot_no": product.slot_no,
        "name": product.name,
        "price": int(product.price),
        "stock": product.stock_qty,
        "image_url": product.image_url,
    }

# POST /products
@router.post("")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Check if slot_no already exists
    existing = db.query(Product).filter(Product.slot_no == product.slot_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Slot number already exists")

    new_product = Product(
        name=product.name,
        price=product.price,
        stock_qty=product.stock_qty,
        slot_no=product.slot_no,
        image_url=product.image_url
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "slot_no": new_product.slot_no,
        "name": new_product.name,
        "price": int(new_product.price),
        "stock": new_product.stock_qty,
        "image_url": new_product.image_url,
    }

# PUT /products/{id}
@router.put("/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check slot_no uniqueness if being updated
    if product_update.slot_no and product_update.slot_no != product.slot_no:
        existing = db.query(Product).filter(Product.slot_no == product_update.slot_no).first()
        if existing:
            raise HTTPException(status_code=400, detail="Slot number already exists")

    # Update fields
    for field, value in product_update.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return {
        "id": product.id,
        "slot_no": product.slot_no,
        "name": product.name,
        "price": int(product.price),
        "stock": product.stock_qty,
        "image_url": product.image_url,
    }

# DELETE /products/{id}
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}