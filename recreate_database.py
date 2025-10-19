import os
from backend.app.database import engine, SessionLocal
from backend.app.models import Base, CategoryDB, ProductDB


def recreate_database():
    # Удаляем существующие таблицы и создаем заново
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Добавляем тестовые категории
    categories = [
        CategoryDB(name="Электроника",
                   description="Смартфоны, ноутбуки, планшеты и другая электроника"),
        CategoryDB(name="Одежда",
                   description="Мужская, женская и детская одежда"),
        CategoryDB(
            name="Книги", description="Художественная и образовательная литература"),
        CategoryDB(name="Дом и сад",
                   description="Товары для дома и садоводства"),
        CategoryDB(name="Спорт", description="Спортивные товары и инвентарь"),
    ]

    for category in categories:
        db.add(category)

    db.commit()
    print("Категории добавлены!")

    # Добавляем тестовые товары
    products = [
        ProductDB(
            name="iPhone 15",
            description="Новый смартфон от Apple с улучшенной камерой",
            price=99999.99,  # В рублях
            image_url="https://api.2droida.ru/storage/products/2f5e426bf0cf949919df221a875fe5ae/6726/3cb3b081e0aab1f9bf39608139da70f2.jpg",
            category_id=1,
            in_stock=True
        ),
        ProductDB(
            name="MacBook Pro",
            description="Мощный ноутбук для работы и творчества",
            price=199999.99,  # В рублях
            image_url="https://avatars.mds.yandex.net/get-mpic/11695357/2a000001909c25cfb294fb6a3e39991373ff/orig",
            category_id=1,
            in_stock=True
        ),
        ProductDB(
            name="iPhone 15",
            description="Новый смартфон от Apple с улучшенной камерой",
            price=999.99,
            image_url="https://api.2droida.ru/storage/products/2f5e426bf0cf949919df221a875fe5ae/6726/3cb3b081e0aab1f9bf39608139da70f2.jpg",
            category_id=1,  # Электроника
            in_stock=True
        ),
        ProductDB(
            name="MacBook Pro",
            description="Мощный ноутбук для работы и творчества",
            price=1999.99,
            image_url="https://avatars.mds.yandex.net/get-mpic/11695357/2a000001909c25cfb294fb6a3e39991373ff/orig",
            category_id=1,  # Электроника
            in_stock=True
        ),
        ProductDB(
            name="Футболка хлопковая",
            description="Комфортная хлопковая футболка",
            price=29.99,
            image_url="https://images-na.ssl-images-amazon.com/images/I/71Lo3LV4ZQL._AC_UL1500_.jpg",
            category_id=2,  # Одежда
            in_stock=True
        ),
        ProductDB(
            name="JavaScript для начинающих",
            description="Книга по основам программирования на JavaScript",
            price=39.99,
            image_url="https://avatars.mds.yandex.net/i?id=b62c2cf81e5e250a8fb31a7e9539a06e_l-4401150-images-thumbs&n=13",
            category_id=3,  # Книги
            in_stock=False
        )
    ]

    for product in products:
        db.add(product)

    db.commit()
    print("Товары добавлены!")
    print("База данных успешно пересоздана!")


if __name__ == "__main__":
    recreate_database()
