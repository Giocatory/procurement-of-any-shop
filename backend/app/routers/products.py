from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..database import get_db
from ..models import ProductDB, Product, PaginatedResponse

router = APIRouter()

@router.get("/products/", response_model=PaginatedResponse)
async def get_products(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=100),
    category_id: int = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    
    # Базовый запрос с загрузкой категорий
    query = db.query(ProductDB).options(joinedload(ProductDB.category))
    
    # Фильтр по категории
    if category_id:
        query = query.filter(ProductDB.category_id == category_id)
    
    # Получаем товары и общее количество
    total = query.count()
    products = query.offset(skip).limit(page_size).all()
    
    # Рассчитываем общее количество страниц
    pages = (total + page_size - 1) // page_size
    
    return PaginatedResponse(
        items=products,
        total=total,
        page=page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductDB).options(joinedload(ProductDB.category)).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product