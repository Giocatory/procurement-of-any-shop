class Marketplace {
    constructor() {
        this.apiBase = '/api/v1';
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupCategoryFilter();
    }
    
    setupEventListeners() {
        // Админ форма для товаров
        const adminForm = document.getElementById('admin-form');
        if (adminForm) {
            adminForm.addEventListener('submit', (e) => this.handleAdminSubmit(e));
        }
        
        // Админ форма для категорий
        const categoryForm = document.getElementById('category-form');
        if (categoryForm) {
            categoryForm.addEventListener('submit', (e) => this.handleCategorySubmit(e));
        }
    }
    
    setupCategoryFilter() {
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', function(e) {
                const categoryId = e.target.value;
                filterProductsByCategory(categoryId);
            });
        }
    }
    
    async handleAdminSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        const productData = {
            name: formData.get('name'),
            description: formData.get('description'),
            price: parseFloat(formData.get('price')),
            image_url: formData.get('image_url'),
            category_id: formData.get('category_id') ? parseInt(formData.get('category_id')) : null,
            in_stock: formData.get('in_stock') === 'on'
        };
        
        try {
            const response = await fetch(`${this.apiBase}/admin/products/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(productData)
            });
            
            if (response.ok) {
                alert('Товар успешно добавлен!');
                e.target.reset();
                // Если мы на вкладке управления товарами, обновляем список
                if (document.getElementById('manage-products').classList.contains('active')) {
                    loadProductsForAdmin();
                }
            } else {
                const error = await response.json();
                alert('Ошибка при добавлении товара: ' + error.detail);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ошибка при добавлении товара');
        }
    }
    
    async handleCategorySubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        const categoryData = {
            name: formData.get('name'),
            description: formData.get('description')
        };
        
        try {
            const response = await fetch('/api/v1/categories/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(categoryData)
            });
            
            if (response.ok) {
                alert('Категория успешно добавлена!');
                e.target.reset();
                loadCategoriesForAdmin();
                
                // Обновляем селект категорий в форме добавления товара
                updateCategorySelect();
            } else {
                const error = await response.json();
                alert('Ошибка при добавлении категории: ' + error.detail);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Ошибка при добавлении категории');
        }
    }
}

// Функции для работы с вкладками
function openTab(tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    const tabBtns = document.getElementsByClassName('tab-btn');
    
    for (let tab of tabContents) {
        tab.classList.remove('active');
    }
    for (let btn of tabBtns) {
        btn.classList.remove('active');
    }
    
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
    
    if (tabName === 'manage-products') {
        loadProductsForAdmin();
    } else if (tabName === 'manage-categories') {
        loadCategoriesForAdmin();
    }
}

// Функции для управления товарами
async function loadProductsForAdmin() {
    try {
        const response = await fetch('/api/v1/products/?page=1&page_size=100');
        const data = await response.json();
        
        const productsList = document.getElementById('products-list');
        if (productsList) {
            productsList.innerHTML = data.items.map(product => `
                <div class="product-item">
                    <div class="product-info">
                        <h4>${product.name}</h4>
                        <p>Цена: ${product.price} ₽ | Категория: ${product.category ? product.category.name : 'Без категории'}</p>
                        <p>${product.in_stock ? '✅ В наличии' : '❌ Нет в наличии'}</p>
                    </div>
                    <div class="product-actions">
                        <button class="btn btn-secondary" onclick="editProduct(${product.id})">Редактировать</button>
                        <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Удалить</button>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function deleteProduct(productId) {
    if (!confirm('Вы уверены, что хотите удалить этот товар?')) return;
    
    try {
        const response = await fetch(`/api/v1/admin/products/${productId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Товар успешно удален!');
            loadProductsForAdmin();
        } else {
            const error = await response.json();
            alert('Ошибка при удалении товара: ' + error.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка при удалении товара');
    }
}

async function editProduct(productId) {
    try {
        // Загружаем данные товара
        const response = await fetch(`/api/v1/products/${productId}`);
        const product = await response.json();
        
        // Загружаем категории для селекта
        const categoriesOptions = await getCategoriesOptions(product.category_id);
        
        // Создаем модальное окно для редактирования
        const modalHtml = `
            <div id="edit-modal" class="modal-overlay">
                <div class="modal-content">
                    <h2>Редактировать товар</h2>
                    <form id="edit-product-form">
                        <input type="hidden" name="id" value="${product.id}">
                        <div class="form-group">
                            <label for="edit-name">Название товара:</label>
                            <input type="text" id="edit-name" name="name" value="${product.name}" required class="form-input">
                        </div>
                        <div class="form-group">
                            <label for="edit-description">Описание:</label>
                            <textarea id="edit-description" name="description" class="form-textarea" rows="4">${product.description || ''}</textarea>
                        </div>
                        <div class="form-row">
                            <div class="form-group">
                                <label for="edit-price">Цена (₽):</label>
                                <input type="number" id="edit-price" name="price" value="${product.price}" step="0.01" required class="form-input">
                            </div>
                            <div class="form-group">
                                <label for="edit-category_id">Категория:</label>
                                <select id="edit-category_id" name="category_id" class="form-select">
                                    <option value="">Без категории</option>
                                    ${categoriesOptions}
                                </select>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="edit-image_url">URL изображения:</label>
                            <input type="url" id="edit-image_url" name="image_url" value="${product.image_url || ''}" class="form-input">
                        </div>
                        <div class="form-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="edit-in_stock" name="in_stock" ${product.in_stock ? 'checked' : ''}>
                                <span class="checkmark"></span>
                                В наличии
                            </label>
                        </div>
                        <div class="modal-actions">
                            <button type="submit" class="btn btn-success">Сохранить</button>
                            <button type="button" onclick="closeEditModal()" class="btn btn-secondary">Отмена</button>
                        </div>
                    </form>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        // Обработчик формы
        document.getElementById('edit-product-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            await updateProduct(productId);
        });
        
    } catch (error) {
        console.error('Error loading product:', error);
        alert('Ошибка при загрузке данных товара');
    }
}

async function getCategoriesOptions(selectedCategoryId) {
    try {
        const response = await fetch('/api/v1/categories/');
        const categories = await response.json();
        
        return categories.map(category => 
            `<option value="${category.id}" ${category.id === selectedCategoryId ? 'selected' : ''}>${category.name}</option>`
        ).join('');
    } catch (error) {
        console.error('Error loading categories:', error);
        return '';
    }
}

function closeEditModal() {
    const modal = document.getElementById('edit-modal');
    if (modal) {
        modal.remove();
    }
}

async function updateProduct(productId) {
    const form = document.getElementById('edit-product-form');
    const formData = new FormData(form);
    
    const productData = {
        name: formData.get('name'),
        description: formData.get('description'),
        price: parseFloat(formData.get('price')),
        image_url: formData.get('image_url'),
        category_id: formData.get('category_id') ? parseInt(formData.get('category_id')) : null,
        in_stock: formData.get('in_stock') === 'on'
    };
    
    try {
        const response = await fetch(`/api/v1/admin/products/${productId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(productData)
        });
        
        if (response.ok) {
            alert('Товар успешно обновлен!');
            closeEditModal();
            loadProductsForAdmin(); // Обновляем список
        } else {
            const error = await response.json();
            alert('Ошибка при обновлении товара: ' + error.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка при обновлении товара');
    }
}

// Функции для управления категориями
async function loadCategoriesForAdmin() {
    try {
        const response = await fetch('/api/v1/categories/');
        const categories = await response.json();
        
        const categoriesList = document.getElementById('categories-list');
        if (categoriesList) {
            categoriesList.innerHTML = categories.map(category => `
                <div class="category-item-admin">
                    <div class="category-info">
                        <h4>${category.name}</h4>
                        <p>${category.description || 'Описание отсутствует'}</p>
                        <small>Создана: ${new Date(category.created_at).toLocaleDateString()}</small>
                    </div>
                    <div class="category-actions">
                        <button class="btn btn-secondary" onclick="editCategory(${category.id})">Редактировать</button>
                        <button class="btn btn-danger" onclick="deleteCategory(${category.id})">Удалить</button>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function deleteCategory(categoryId) {
    if (!confirm('Вы уверены, что хотите удалить эту категорию?')) return;
    
    try {
        const response = await fetch(`/api/v1/categories/${categoryId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Категория успешно удалена!');
            loadCategoriesForAdmin();
            updateCategorySelect(); // Обновляем селект в форме товаров
        } else {
            const error = await response.json();
            alert('Ошибка при удалении категории: ' + error.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка при удалении категории');
    }
}

async function editCategory(categoryId) {
    try {
        // Загружаем данные категории
        const response = await fetch(`/api/v1/categories/`);
        const categories = await response.json();
        const category = categories.find(cat => cat.id === categoryId);
        
        if (!category) {
            alert('Категория не найдена');
            return;
        }
        
        const newName = prompt('Введите новое название категории:', category.name);
        if (!newName) return;
        
        const newDescription = prompt('Введите новое описание категории:', category.description || '');
        
        const responseUpdate = await fetch(`/api/v1/categories/${categoryId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: newName,
                description: newDescription
            })
        });
        
        if (responseUpdate.ok) {
            alert('Категория успешно обновлена!');
            loadCategoriesForAdmin();
            updateCategorySelect(); // Обновляем селект в форме товаров
        } else {
            const error = await responseUpdate.json();
            alert('Ошибка при обновлении категории: ' + error.detail);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Ошибка при обновлении категории');
    }
}

// Обновление селекта категорий в форме добавления товара
async function updateCategorySelect() {
    const categorySelect = document.getElementById('category_id');
    if (!categorySelect) return;
    
    try {
        const response = await fetch('/api/v1/categories/');
        const categories = await response.json();
        
        categorySelect.innerHTML = '<option value="">Без категории</option>' + 
            categories.map(category => 
                `<option value="${category.id}">${category.name}</option>`
            ).join('');
    } catch (error) {
        console.error('Error updating category select:', error);
    }
}

// Функции для главной страницы
function filterByCategory(categoryId) {
    if (categoryId) {
        window.location.href = `/?category_id=${categoryId}`;
    } else {
        window.location.href = '/';
    }
}

function filterProductsByCategory(categoryId) {
    const products = document.querySelectorAll('.product-card');
    
    products.forEach(product => {
        if (!categoryId || product.dataset.category === categoryId) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}

// Корзина (базовая реализация)
function addToCart(productId) {
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');
    cart.push(productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    
    alert('Товар добавлен в корзину!');
}

// Обработка ошибок загрузки изображений
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            this.style.display = 'none';
            const placeholder = document.createElement('div');
            placeholder.className = 'no-image-placeholder';
            placeholder.innerHTML = '<span>🖼️</span><p>Image Not Available</p>';
            this.parentNode.insertBefore(placeholder, this);
        });
    });
});

// Инициализация приложения
const marketplace = new Marketplace();

// Глобальные функции для использования в HTML
window.addToCart = addToCart;
window.loadProductsForAdmin = loadProductsForAdmin;
window.deleteProduct = deleteProduct;
window.editProduct = editProduct;
window.openTab = openTab;
window.loadCategoriesForAdmin = loadCategoriesForAdmin;
window.deleteCategory = deleteCategory;
window.editCategory = editCategory;
window.filterByCategory = filterByCategory;
window.filterProductsByCategory = filterProductsByCategory;
window.closeEditModal = closeEditModal;