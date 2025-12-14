from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from seed import seed_data
from deps import get_db
from routers.products import router as products_router
from routers.vending import router as vending_router

app = FastAPI(title="Simple Vending Machine")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://localhost:3000",  # Docker frontend
        "http://127.0.0.1:3000"   # Docker frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    db = next(get_db())
    seed_data(db)

# 🔥 include router
app.include_router(products_router)
app.include_router(vending_router)
