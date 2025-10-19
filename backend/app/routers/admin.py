from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import ProductDB, ProductCreate, Product

router = APIRouter(prefix="/admin", tags=["admin"])

# Простая аутентификация
def verify_admin():
    return True

@router.post("/products/", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    if not verify_admin():
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_product = ProductDB(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Загружаем категорию для ответа
    db_product = db.query(ProductDB).options(joinedload(ProductDB.category)).filter(ProductDB.id == db_product.id).first()
    return db_product

@router.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    if not verify_admin():
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db_product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    
    # Загружаем категорию для ответа
    db_product = db.query(ProductDB).options(joinedload(ProductDB.category)).filter(ProductDB.id == db_product.id).first()
    return db_product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    if not verify_admin():
        raise HTTPException(status_code=403, detail="Not authorized")
    
    product = db.query(ProductDB).filter(ProductDB.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}