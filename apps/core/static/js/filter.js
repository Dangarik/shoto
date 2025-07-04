
export function initializeFilter() {
    const filters = document.querySelectorAll('.category-filter');
    filters.forEach(filter => {
        filter.addEventListener('change', (event) => {
            filterProducts();
        });
    });
}
function filterProducts() {
    const filters = document.querySelectorAll('.category-filter');
    const activeFilters = Array.from(filters)
        .filter(filter => filter.checked)
        .map(filter => filter.id);
    
    const products = document.querySelectorAll('.product');
    
    products.forEach(product => {
        const productCategories = Array.from(product.classList).filter(className => className.startsWith('category'));
        const isVisible = activeFilters.some(filter => productCategories.includes(filter));
        
        if (isVisible) {
            product.style.display = '';
        } else {
            product.style.display = 'none';
        }
    });
}
