from sqlalchemy.orm import Session
from models import Product, MoneyStock
import random


def seed_data(db: Session):
    # ---------- Products ----------
    if db.query(Product).count() == 0:
        products = [
            # ---------- น้ำดื่ม ----------
            Product(
                name="Mineral Water",
                price=10,
                stock_qty=random.randint(0, 50),
                slot_no="A1",
                image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQs64YWg7D04Zzb_LkkMUKaFwwV4beRHkP0sA&s"
            ),
            Product(
                name="Sparkling Water",
                price=15,
                stock_qty=random.randint(0, 50),
                slot_no="A2",
                image_url="https://crushmag-online.com/wp-content/uploads/2024/03/Sparkling-Water_S.Pellegrino_1x65.jpg"
            ),
            Product(
                name="Green Tea Bottle",
                price=20,
                stock_qty=random.randint(0, 50),
                slot_no="A3",
                image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQdIA9f1qvcuTago5A5IoveaLOf04J-98-26g&s"
            ),
            Product(
                name="Lemon Tea",
                price=20,
                stock_qty=random.randint(0, 50),
                slot_no="A4",
                image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQNIEji--Ii95nudHg4AoMPhIAkYv53O6tTxA&s"
            ),

            # ---------- ขนมซอง ----------
            Product(
                name="Potato Chips",
                price=25,
                stock_qty=random.randint(0, 50),
                slot_no="B1",
                image_url="https://i5.walmartimages.com/seo/Lay-s-Classic-Potato-Chips-15-25-oz-Bag_d9939d0f-6382-4a0d-97c1-d5444345899e_1.c22bb525689793e89a3525a65f5a730c.jpeg"
            ),
            Product(
                name="Corn Snack",
                price=20,
                stock_qty=random.randint(0, 50),
                slot_no="B2",
                image_url="https://siamstore.us/cdn/shop/files/TopUpPaprika1.jpg?v=1751886649"
            ),
            Product(
                name="Chocolate Bar",
                price=30,
                stock_qty=random.randint(0, 50),
                slot_no="B3",
                image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKKqWDRvsoxcGLVj2Qr3Zl00TvYos2e7z_Lw&s"
            ),

            # ---------- ถั่ว / ของทานเล่น ----------
            Product(
                name="Roasted Peanuts",
                price=25,
                stock_qty=random.randint(0, 50),
                slot_no="C1",
                image_url="https://jabsons.com/cdn/shop/files/320g_Nutraja_-_Eco_Brand_SALTED_PEANUT_FRONT.webp?v=1761731132&width=1946"
            ),
            Product(
                name="Mixed Nuts",
                price=35,
                stock_qty=random.randint(0, 50),
                slot_no="C2",
                image_url="https://inwfile.com/s-cm/zbk2zf.jpg"
            ),
            Product(
                name="Almond Pack",
                price=40,
                stock_qty=random.randint(0, 50),
                slot_no="C3",
                image_url="https://www.snackamor.com/cdn/shop/products/Almonds-1.png?v=1666267994"
            ),
        ]
        db.add_all(products)

    # ---------- Money ----------
    if db.query(MoneyStock).count() == 0:
        money = [
            MoneyStock(denom=1, quantity=50, type="coin"),
            MoneyStock(denom=5, quantity=50, type="coin"),
            MoneyStock(denom=10, quantity=50, type="coin"),
            MoneyStock(denom=20, quantity=20, type="banknote"),
            MoneyStock(denom=50, quantity=20, type="banknote"),
            MoneyStock(denom=100, quantity=10, type="banknote"),
        ]
        db.add_all(money)

    db.commit()
