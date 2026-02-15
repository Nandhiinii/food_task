from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import menu, order, order_item
from app.routes import menu as menu_router
from app.routes import orders as order_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
Base.metadata.create_all(bind=engine)

app.include_router(menu_router.router)
app.include_router(order_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Order Management API Running"}
