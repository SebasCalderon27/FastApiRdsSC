from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- Entidad Usuario ---
class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="owner")

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None

# --- Entidad Producto ---
class ProductBase(SQLModel):
    title: str
    price: float
    user_id: int = Field(foreign_key="user.id")

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner: Optional[User] = Relationship(back_populates="products")

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

class ProductUpdate(SQLModel):
    title: Optional[str] = None
    price: Optional[float] = None