import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.menu import Menu
from app.schemas.menu import MenuResponse

router = APIRouter(prefix="/api/menu", tags=["Menu"])

UPLOAD_DIR = "uploads/menu_images"

# Ensure folder exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=MenuResponse)
def create_menu_item(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save image to disk
    file_path = os.path.join(UPLOAD_DIR, image.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    menu_item = Menu(
        name=name,
        description=description,
        price=price,
        image_url=file_path
    )

    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)

    return menu_item

@router.get("/", response_model=List[MenuResponse])
def get_menu(db: Session = Depends(get_db)):
    return db.query(Menu).all()
