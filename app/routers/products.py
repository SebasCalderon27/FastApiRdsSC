from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models import Product, ProductCreate, ProductRead, ProductUpdate, User

router = APIRouter(prefix="/products", tags=["Productos"])

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    owner = session.get(User, product.user_id)
    if not owner:
        raise HTTPException(status_code=400, detail="El user_id especificado no existe")
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductRead])
def read_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@router.get("/{product_id}", response_model=ProductRead)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_data: ProductUpdate, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    product_dict = product_data.model_dump(exclude_unset=True)
    for key, value in product_dict.items():
        setattr(db_product, key, value)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(product)
    session.commit()
    return {"message": "Producto eliminado correctamente"}