document.addEventListener('DOMContentLoaded', async () => {
    const logoutButton = document.getElementById('logout-button');
    const returnButton = document.getElementById('return-button');
    const loadingMessage = document.getElementById('loading-message');
    const ordersTable = document.getElementById('orders-table');
    const ordersTableBody = document.getElementById('orders-table-body');

    // Logout button functionality
    logoutButton.addEventListener('click', async () => {
        const response = await fetch('/logout', { method: 'GET' });
        const result = await response.json();
        alert(result.message);
        window.location.href = '/'; // Redirect to login page
    });

    // Return button functionality
    returnButton.addEventListener('click', () => {
        window.location.href = '/welcome'; // Redirect to welcome page
    });

    // Function to load product image
    function loadProductImage(imgElement, productName) {
        const formats = ['jpg', 'png', 'jpeg', 'gif'];
        let formatIndex = 0;

        function tryNextFormat() {
            if (formatIndex < formats.length) {
                imgElement.src = `/static/img/${productName
                    .replace(/\s+/g, '_')                       // replace space to _
                    .replace(/[^a-zA-Z0-9\u4e00-\u9fa5_]/g, '') // remove non alpha/number/chinese/underscore characters
                }.${formats[formatIndex]}`;
                formatIndex++;
            } else {
                imgElement.src = '/static/img/default.jpg'; // Fallback image
            }
        }

        imgElement.onerror = tryNextFormat;
        tryNextFormat(); // Start trying the first format
    }

    // Load user's order history
    try {
        const response = await fetch('/user/orders', { method: 'GET' });
        if (!response.ok) {
            throw new Error('Failed to fetch order history');
        }

        const result = await response.json();
        if (!result.success) {
            throw new Error(result.message || 'Failed to fetch order history');
        }

        // Populate order table
        result.orders.forEach(order => {
            const row = document.createElement('tr');

            const orderIdCell = document.createElement('td');
            orderIdCell.textContent = order.id;
            row.appendChild(orderIdCell);

            const productIdCell = document.createElement('td');
            productIdCell.textContent = order.product_id;
            row.appendChild(productIdCell);

            const productNameCell = document.createElement('td');
            productNameCell.textContent = order.product_name || 'Unknown';
            row.appendChild(productNameCell);

            // const productPriceCell = document.createElement('td');
            // productPriceCell.textContent = order.product_price;
            // row.appendChild(productPriceCell);

            const productImageCell = document.createElement('td');
            const productImg = document.createElement('img');
            loadProductImage(productImg, order.product_name || 'Unknown');
            productImageCell.appendChild(productImg);
            row.appendChild(productImageCell);

            const quantityCell = document.createElement('td');
            quantityCell.textContent = order.quantity;
            row.appendChild(quantityCell);

            const orderDateCell = document.createElement('td');
            orderDateCell.textContent = new Date(order.order_date).toLocaleString();
            row.appendChild(orderDateCell);

            ordersTableBody.appendChild(row);
        });

        loadingMessage.style.display = 'none';
        ordersTable.style.display = 'table';
    } catch (error) {
        loadingMessage.textContent = `Error loading orders: ${error.message}`;
    }
});
