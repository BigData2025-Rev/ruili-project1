document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('users-table');

    // Fetch all users when "Check All Users" button is clicked
    document.getElementById('check-users-button').addEventListener('click', async () => {
        document.getElementById('users-table').style.display = 'table-row-group';
        tableBody.innerHTML = ''; // Clear existing rows
        try {
            const response = await fetch('/users');
            const result = await response.json();

            if (result.success) {
                result.users.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.user_id}</td>
                        <td>${user.username}</td>
                        <td>${user.role}</td>
                        <td>
                            <button class="delete-user-button" data-id="${user.user_id}">Delete User</button>
                            <button class="update-role-button" data-id="${user.user_id}">Update to Admin</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });

                // Attach event listeners for delete and update buttons
                document.querySelectorAll('.delete-user-button').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const userId = e.target.getAttribute('data-id');
                        const response = await fetch('/user', {
                            method: 'DELETE',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ user_id: userId }),
                        });
                        const result = await response.json();
                        alert(result.success ? 'User deleted successfully.' : `Failed to delete user: ${result.message}`);
                        if (result.success) e.target.closest('tr').remove();
                    });
                });

                document.querySelectorAll('.update-role-button').forEach(button => {
                    button.addEventListener('click', async (e) => {
                        const userId = e.target.getAttribute('data-id');
                        const response = await fetch('/user/role', {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ user_id: userId, role: 'admin' }),
                        });
                        const result = await response.json();
                        alert(result.success ? 'User role updated to admin.' : `Failed to update role: ${result.message}`);
                    });
                });
            } else {
                alert(result.message);
            }
        } catch (error) {
            alert('Failed to fetch users.');
        }
    });


    const productsTable = document.getElementById('products-table');
    const productsTableBody = document.getElementById('products-table-body');
    
    // Check All Products
    document.getElementById('check-products-button').addEventListener('click', async () => {
        productsTableBody.innerHTML = ''; // Clear existing rows
        try {
            const response = await fetch('/products');
            const result = await response.json();

            if (result.success) {
                productsTable.style.display = 'table'; // Show table

                result.products.forEach(product => {
                    const row = document.createElement('tr');

                    // Product ID
                    const idCell = document.createElement('td');
                    idCell.textContent = product.id;
                    row.appendChild(idCell);

                    // Product Name
                    const nameCell = document.createElement('td');
                    nameCell.textContent = product.name;
                    row.appendChild(nameCell);

                    // Inventory
                    const inventoryCell = document.createElement('td');
                    const inventoryInput = document.createElement('input');
                    inventoryInput.type = 'number';
                    inventoryInput.value = product.inventory;
                    inventoryInput.min = 0;
                    inventoryInput.style.width = '60px';
                    inventoryCell.appendChild(inventoryInput);
                    const updateInventoryButton = document.createElement('button');
                    updateInventoryButton.textContent = 'Update';
                    updateInventoryButton.addEventListener('click', async () => {
                        const newInventory = parseInt(inventoryInput.value);
                        if (isNaN(newInventory) || newInventory < 0) {
                            alert('Invalid inventory value');
                            return;
                        }
                        const updateResponse = await fetch('/product/inventory', {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ product_id: product.id, change_amount: newInventory - product.inventory })
                        });
                        const updateResult = await updateResponse.json();
                        if (updateResponse.ok && updateResult.success) {
                            product.inventory = newInventory;
                            alert('Inventory updated successfully');
                        } else {
                            alert(`Failed to update inventory: ${updateResult.message}`);
                        }
                    });
                    inventoryCell.appendChild(updateInventoryButton);
                    row.appendChild(inventoryCell);

                    // Price
                    const priceCell = document.createElement('td');
                    const priceInput = document.createElement('input');
                    priceInput.type = 'number';
                    priceInput.value = product.price;
                    priceInput.min = 0;
                    priceInput.step = 0.01;
                    priceInput.style.width = '60px';
                    priceCell.appendChild(priceInput);
                    const updatePriceButton = document.createElement('button');
                    updatePriceButton.textContent = 'Update';
                    updatePriceButton.addEventListener('click', async () => {
                        const newPrice = parseFloat(priceInput.value);
                        if (isNaN(newPrice) || newPrice < 0) {
                            alert('Invalid price value');
                            return;
                        }
                        const updateResponse = await fetch('/product/price', {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ product_id: product.id, new_price: newPrice })
                        });
                        const updateResult = await updateResponse.json();
                        if (updateResponse.ok && updateResult.success) {
                            product.price = newPrice;
                            alert('Price updated successfully');
                        } else {
                            alert(`Failed to update price: ${updateResult.message}`);
                        }
                    });
                    priceCell.appendChild(updatePriceButton);
                    row.appendChild(priceCell);

                    // Delete
                    const actionsCell = document.createElement('td');
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.addEventListener('click', async () => {
                        const deleteResponse = await fetch('/product', {
                            method: 'DELETE',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ product_id: product.id })
                        });
                        const deleteResult = await deleteResponse.json();
                        if (deleteResponse.ok && deleteResult.success) {
                            row.remove();
                            alert('Product deleted successfully');
                        } else {
                            alert(`Failed to delete product: ${deleteResult.message}`);
                        }
                    });
                    actionsCell.appendChild(deleteButton);
                    row.appendChild(actionsCell);

                    productsTableBody.appendChild(row);
                });
            } else {
                alert(result.message);
            }
        } catch (error) {
            alert('Failed to fetch products.');
        }
    });

    // function to add new product
    document.getElementById('add-product-form').addEventListener('submit', async (event) => {
        event.preventDefault(); // 阻止默认提交行为
    
        const form = event.target;
        const formData = new FormData(form);
    
        try {
            const response = await fetch('/product', {
                method: 'PUT',
                body: formData,
            });
    
            const result = await response.json();
            if (response.ok && result.success) {
                alert('Product added successfully');
                location.reload(); // 刷新页面
            } else {
                alert(`Failed to add product: ${result.message}`);
            }
        } catch (error) {
            alert(`Error adding product: ${error.message}`);
        }
    }); 

    const ordersTable = document.getElementById('orders-table');
    const ordersTableBody = document.getElementById('orders-table-body');

    // Check All Orders
    document.getElementById('check-orders-button').addEventListener('click', async () => {
        ordersTableBody.innerHTML = ''; // Clear existing rows
        try {
            const response = await fetch('/orders');
            const result = await response.json();

            if (result.success) {
                ordersTable.style.display = 'table'; // Show table

                result.orders.forEach(order => {
                    const row = document.createElement('tr');
                    
                    const orderIdCell = document.createElement('td');
                    orderIdCell.textContent = order.id;
                    row.appendChild(orderIdCell);

                    const userIdCell = document.createElement('td');
                    userIdCell.textContent = order.user_id;
                    row.appendChild(userIdCell);

                    const productIdCell = document.createElement('td');
                    productIdCell.textContent = order.product_id;
                    row.appendChild(productIdCell);

                    const productNameCell = document.createElement('td');
                    productNameCell.textContent = order.product_name || 'Unknown';
                    row.appendChild(productNameCell);

                    const quantityCell = document.createElement('td');
                    quantityCell.textContent = order.quantity;
                    row.appendChild(quantityCell);

                    const orderDateCell = document.createElement('td');
                    orderDateCell.textContent = new Date(order.order_date).toLocaleString();
                    row.appendChild(orderDateCell);

                    ordersTableBody.appendChild(row);
                });
            } else {
                alert(result.message);
            }
        } catch (error) {
            alert('Failed to fetch orders.');
        }
    });

    // Hide Orders
    document.getElementById('hide-orders-button').addEventListener('click', () => {
        ordersTable.style.display = 'none';
    });

    // Hide Users
    document.getElementById('hide-users-button').addEventListener('click', () => {
        document.getElementById('users-table').style.display = 'none';
    });

    // Hide Products
    document.getElementById('hide-products-button').addEventListener('click', () => {
        document.getElementById('products-table').style.display = 'none';
    });

    // Logout functionality
    document.getElementById('logout-button').addEventListener('click', async () => {
        const response = await fetch('/logout', { method: 'GET' });
        const result = await response.json();
        alert(result.message);
        window.location.href = '/';
    });

    // Return to welcome page
    document.getElementById('return-button').addEventListener('click', () => {
        window.location.href = '/welcome';
    });
});
