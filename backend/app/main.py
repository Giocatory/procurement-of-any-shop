from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables, get_db
from .routers import products, admin, categories
from sqlalchemy.orm import Session
import os
from sqlalchemy.orm import joinedload

app = FastAPI(title="Marketplace")

# Создаем таблицы
create_tables()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры API
app.include_router(products.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")

# Получаем абсолютные пути
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))  # backend/app -> backend -> project_root
static_dir = os.path.join(project_root, "static")
templates_dir = os.path.join(current_dir, "templates")

print(f"Current dir: {current_dir}")
print(f"Project root: {project_root}")
print(f"Static dir: {static_dir}")
print(f"Templates dir: {templates_dir}")

# Проверяем и создаем директории если нужно
os.makedirs(static_dir, exist_ok=True)
os.makedirs(os.path.join(static_dir, "css"), exist_ok=True)
os.makedirs(os.path.join(static_dir, "js"), exist_ok=True)
os.makedirs(os.path.join(static_dir, "images"), exist_ok=True)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# HTML маршруты
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    from .routers.products import get_products
    from .routers.categories import get_categories_stats
    
    # Получаем параметры из запроса
    page = int(request.query_params.get("page", 1))
    category_id = request.query_params.get("category_id")
    
    # Получаем товары - 2 на страницу
    products_response = await get_products(request, page, 2, category_id, db)
    
    # Получаем статистику по категориям
    categories_stats = await get_categories_stats(db)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products_response.items,
        "pagination": {
            "page": products_response.page,
            "pages": products_response.pages,
            "has_next": products_response.has_next,
            "has_prev": products_response.has_prev  # ИСПРАВЛЕНО: было response.has_prev
        },
        "categories_stats": categories_stats,
        "current_category_id": category_id
    })

@app.get("/product/{product_id}")
async def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    from .routers.products import get_product
    try:
        product = await get_product(product_id, db)
        return templates.TemplateResponse("product.html", {
            "request": request,
            "product": product
        })
    except Exception as e:
        return templates.TemplateResponse("404.html", {
            "request": request,
            "error": str(e)
        }, status_code=404)

@app.get("/admin")
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    from .routers.categories import get_categories
    categories = await get_categories(db)
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "categories": categories
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)