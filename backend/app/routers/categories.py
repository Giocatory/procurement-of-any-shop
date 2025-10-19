from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..models import CategoryDB, Category, CategoryCreate, CategoryStats

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[Category])
async def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryDB).all()

@router.get("/stats/", response_model=list[CategoryStats])
async def get_categories_stats(db: Session = Depends(get_db)):
    # Получаем статистику по категориям (количество товаров в каждой)
    stats = db.query(
        CategoryDB.id,
        CategoryDB.name,
        func.count(CategoryDB.products).label('product_count')
    ).outerjoin(CategoryDB.products).group_by(CategoryDB.id, CategoryDB.name).all()
    
    return [CategoryStats(
        category_id=stat.id,
        category_name=stat.name,
        product_count=stat.product_count
    ) for stat in stats]

@router.post("/", response_model=Category)
async def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли категория с таким именем
    existing_category = db.query(CategoryDB).filter(CategoryDB.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    db_category = CategoryDB(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Проверяем, не существует ли другой категории с таким именем
    existing_category = db.query(CategoryDB).filter(
        CategoryDB.name == category.name,
        CategoryDB.id != category_id
    ).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Проверяем, есть ли товары в этой категории
    if category.products:
        raise HTTPException(
            status_code=400, 
            detail="Cannot delete category that has products. Please reassign products first."
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}