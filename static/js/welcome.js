document.getElementById('logout-button').addEventListener('click', async () => {
    const response = await fetch('/logout', { method: 'GET' });
    const result = await response.json();
    alert(result.message);
    window.location.href = '/'; // 跳转到主页
});

document.getElementById('admin-dashboard-button').addEventListener('click', async () => {
    try {
        const response = await fetch('/admin', { method: 'GET' });
        if (response.ok) {
            window.location.href = '/admin';
        } else {
            const result = await response.json();
            alert(result.message);
        }
    } catch (error) {
        alert('Error accessing admin page.');
    }
});

// Load products on page load
document.addEventListener('DOMContentLoaded', async () => {
    const table = document.getElementById('product-table');
    const tableBody = document.getElementById('product-table-body');
    const loadingMessage = document.getElementById('loading-message');
    
    try {
        const response = await fetch('/products', { method: 'GET' });
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.message || 'Failed to fetch products');
        }

        result.products.forEach(product => {
            const row = document.createElement('tr');

            const idCell = document.createElement('td');
            idCell.textContent = product.id;
            row.appendChild(idCell);

            const imageCell = document.createElement('td');
            const img = document.createElement('img');
            img.src = `/static/img/${product.name}.jpg`;
            img.alt = product.name;
            img.onerror = () => { img.src = '/static/img/default.jpg'; }; // Fallback image
            imageCell.appendChild(img);
            row.appendChild(imageCell);

            const nameCell = document.createElement('td');
            nameCell.textContent = product.name;
            row.appendChild(nameCell);

            const priceCell = document.createElement('td');
            const price = parseFloat(product.price) || 0.0;
            priceCell.textContent = `$${price.toFixed(2)}`;
            row.appendChild(priceCell);

            const inventoryCell = document.createElement('td');
            inventoryCell.textContent = product.inventory;
            row.appendChild(inventoryCell);

            tableBody.appendChild(row);
        });

        loadingMessage.style.display = 'none';
        table.style.display = 'table';
    } catch (error) {
        loadingMessage.textContent = `Error loading products: ${error.message}`;
    }
});
