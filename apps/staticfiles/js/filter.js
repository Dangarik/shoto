/*
function filterProducts() {
    const filters = document.querySelectorAll('.category-filter');
    const activeFilters = Array.from(filters)
        .filter(filter => filter.checked)
        .map(filter => filter.id);

    const products = document.querySelectorAll('.product');
    products.forEach(product => {
        const productCategories = Array.from(product.classList).filter(className => className.startsWith('category'));
        const isVisible = activeFilters.some(filter => {
            const filterCategory = document.getElementById(filter).nextElementSibling.textContent.trim(); // отримаємо текст категорії
            return productCategories.includes(`category-${filterCategory}`);
        });

        if (isVisible) {
            product.style.display = '';
        } else {
            product.style.display = 'none';
        }
    });
}

 */