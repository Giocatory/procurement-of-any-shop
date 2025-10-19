# 🛍️ MarketPlace - Шаблон интернет-магазина на FastAPI

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=for-the-badge&logo=sass&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

Современный, полностью функциональный шаблон интернет-магазина с панелью администратора, построенный на FastAPI с красивым фронтендом и адаптивным дизайном.

## ✨ Особенности

### 🎯 Основной функционал
- **📦 Управление товарами** - Полный CRUD для товаров
- **🏷️ Система категорий** - Гибкая категоризация товаров
- **👨‍💼 Панель администратора** - Интуитивное управление контентом
- **🔍 Поиск и фильтрация** - Умный поиск по товарам и категориям
- **📄 Пагинация** - Оптимизированная загрузка товаров
- **🛒 Корзина покупок** - Базовая реализация корзины

### 🎨 Дизайн и UX
- **⚡ Современный дизайн** - Glass-morphism и градиенты
- **📱 Полная адаптивность** - Mobile-first подход
- **🎭 Плавные анимации** - CSS-анимации и переходы
- **♿ Доступность** - Семантическая верстка
- **🌙 Современные тренды** - Следует последним тенденциям UI/UX

### 🛠 Технические особенности
- **🚀 Высокая производительность** - Асинхронный FastAPI
- **📊 SQLAlchemy ORM** - Надежная работа с базой данных
- **🎯 Type hints** - Полная типизация кода
- **🔧 SCSS препроцессор** - Переменные, миксины, функции
- **⚙️ Модульная архитектура** - Легкая расширяемость

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.8+
- pip (менеджер пакетов Python)
- Node.js (для компиляции SCSS)

### Установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/yourusername/marketplace-template.git
cd marketplace-template
```

2. **Создание виртуального окружения**
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# или
venv\Scripts\activate     # Windows
```

3. **Установка зависимостей**
```bash
pip install -r requirements.txt
```

4. **Установка Sass для компиляции стилей**
```bash
npm install -g sass
```

5. **Инициализация базы данных**
```bash
python recreate_database.py
```

6. **Компиляция SCSS стилей**
```bash
sass scss/main.scss static/css/style.css --watch
```

7. **Запуск сервера**
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

8. **Откройте в браузере**
```
http://localhost:8000
```

## 📁 Структура проекта

```
marketplace-template/
├── backend/                    # Backend на FastAPI
│   ├── app/
│   │   ├── main.py            # Основное приложение
│   │   ├── models.py          # Модели данных
│   │   ├── database.py        # Настройки базы данных
│   │   ├── routers/           # API роутеры
│   │   │   ├── products.py    # API товаров
│   │   │   ├── admin.py       # API админки
│   │   │   └── categories.py  # API категорий
│   │   └── templates/         # HTML шаблоны
│   │       ├── base.html
│   │       ├── index.html
│   │       ├── product.html
│   │       └── admin.html
├── static/                    # Статические файлы
│   ├── css/
│   │   └── style.css          # Скомпилированные стили
│   ├── js/
│   │   └── main.js            # Фронтенд логика
│   └── images/                # Изображения
├── scss/                      # Исходные SCSS файлы
│   └── main.scss              # Главный SCSS файл
├── requirements.txt           # Зависимости Python
└── recreate_database.py       # Скрипт инициализации БД
```

## 🎨 Кастомизация

### Цветовая схема

Измените переменные в `scss/main.scss`:

```scss
$primary-color: #6366f1;       // Основной цвет
$secondary-color: #10b981;     // Вторичный цвет
$gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Добавление новых полей товаров

1. Обновите модель в `backend/app/models.py`:
```python
class ProductDB(Base):
    # существующие поля...
    new_field = Column(String(100))  # новое поле
```

2. Обновите Pydantic схемы:
```python
class ProductBase(BaseModel):
    # существующие поля...
    new_field: Optional[str] = None
```

3. Обновите формы в шаблонах

### Расширение функционала

- **Аутентификация пользователей** - Добавьте JWT токены
- **Платежная система** - Интегрируйте Stripe/YooMoney
- **Отзывы и рейтинги** - Добавьте систему оценок
- **Мультиязычность** - Поддержка нескольких языков
- **Система скидок** - Купоны и акции

## 🔧 API Endpoints

### Товары
- `GET /api/v1/products/` - Список товаров с пагинацией
- `GET /api/v1/products/{id}` - Детали товара
- `POST /api/v1/admin/products/` - Создать товар (админ)
- `PUT /api/v1/admin/products/{id}` - Обновить товар (админ)
- `DELETE /api/v1/admin/products/{id}` - Удалить товар (админ)

### Категории
- `GET /api/v1/categories/` - Список категорий
- `GET /api/v1/categories/stats/` - Статистика по категориям
- `POST /api/v1/categories/` - Создать категорию (админ)
- `PUT /api/v1/categories/{id}` - Обновить категорию (админ)
- `DELETE /api/v1/categories/{id}` - Удалить категорию (админ)

## 🎯 Использование

### Для разработчиков

1. **Создание нового типа товара**
```python
# В backend/app/models.py
class DigitalProductDB(ProductDB):
    __tablename__ = "digital_products"
    id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    download_url = Column(String(200))
    file_size = Column(String(50))
```

2. **Добавление нового фильтра**
```javascript
// В static/js/main.js
class Marketplace {
    addPriceFilter(minPrice, maxPrice) {
        // Реализация фильтра по цене
    }
}
```

3. **Кастомизация стилей**
```scss
// В scss/main.scss
@mixin custom-product-card {
    @include card-style(lg);
    border-left: 4px solid $secondary-color;
    
    &:hover {
        transform: rotate(-1deg);
    }
}
```

### Для владельцев бизнеса

1. **Добавление товаров** через панель администратора
2. **Управление категориями** для организации каталога
3. **Настройка дизайна** через SCSS переменные
4. **Расширение функционала** по мере роста бизнеса

## 🚀 Производительность

### Оптимизации

- **Асинхронные запросы** - FastAPI + async/await
- **Ленивая загрузка** - Пагинация и бесконечный скролл
- **Кэширование** - Готовность к интеграции Redis
- **Оптимизированные изображения** - Adaptive images
- **Минификация CSS/JS** - Готовность к продакшену

### Мониторинг

```python
# Добавьте в main.py для мониторинга
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

## 🔒 Безопасность

### Встроенные меры безопасности

- **Валидация данных** - Pydantic схемы
- **SQL injection protection** - SQLAlchemy ORM
- **XSS protection** - Jinja2 autoescaping
- **CORS настройки** - Защита межсайтовых запросов

### Рекомендации для продакшена

1. **Настройка HTTPS**
2. **Добавление аутентификации**
3. **Настройка брандмауэра**
4. **Регулярное обновление зависимостей**

## 📈 Масштабирование

### Вертикальное масштабирование
- Миграция на PostgreSQL
- Добавление Redis для кэширования
- Настройка кластеризации

### Горизонтальное масштабирование
- Docker контейнеризация
- Балансировщик нагрузки
- Репликация базы данных

## 🌐 Развертывание

### Локальная разработка
```bash
uvicorn backend.app.main:app --reload
```

### Продакшен с Docker
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### Развертывание на облачных платформах

**Heroku**
```bash
heroku create your-shop-name
git push heroku main
```

**DigitalOcean App Platform**
- Автоматическое развертывание из GitHub
- Встроенный SSL и CDN

**AWS Elastic Beanstalk**
```bash
eb init -p python-3.11 marketplace-app
eb create marketplace-env
```

### Процесс разработки

1. Форкните репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Стандарты кода

- **Python** - PEP 8, black formatter
- **JavaScript** - ESLint, Prettier
- **SCSS** - BEM methodology
- **Коммиты** - Conventional Commits

## 🚀 Быстрый старт за 5 минут

```bash
# 1. Клонировать репозиторий
git clone https://github.com/yourusername/marketplace-template.git shop
cd shop

# 2. Установить зависимости
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Запустить
python recreate_database.py
uvicorn backend.app.main:app --reload
```

**Ваш магазин запущен!** 🎉 Откройте http://localhost:8000 и начните продавать!
