from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

Base = declarative_base()

# Модель для категорий
class CategoryDB(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связь с товарами
    products = relationship("ProductDB", back_populates="category")

# Обновленная модель товаров
class ProductDB(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(200))
    category_id = Column(Integer, ForeignKey("categories.id"))
    in_stock = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связь с категорией
    category = relationship("CategoryDB", back_populates="products")

# Pydantic модели для категорий
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Обновленные Pydantic модели для товаров
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    in_stock: bool = True

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    category: Optional[Category] = None
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: list[Product]
    total: int
    page: int
    pages: int
    has_next: bool
    has_prev: bool

# Модель для статистики по категориям
class CategoryStats(BaseModel):
    category_id: int
    category_name: str
    product_count: int