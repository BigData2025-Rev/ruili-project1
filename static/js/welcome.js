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

// Load current user information
async function loadCurrentUser() {
    try {
        const usernameResponse = await fetch('/user/username');
        const usernameResult = await usernameResponse.json();
        if (!usernameResult.username) {
            throw new Error('Failed to retrieve username.');
        }
        document.getElementById('current-username').textContent = usernameResult.username;

        const depositResponse = await fetch('/user/deposit');
        const depositResult = await depositResponse.json();
        if (!depositResult.success) {
            throw new Error(depositResult.message || 'Failed to retrieve deposit.');
        }
        document.getElementById('current-deposit').textContent = depositResult.deposit.toFixed(2);
    } catch (error) {
        alert(`Failed to load user information: ${error.message}`);
        console.error(error);
    }
}

// Load user info when page is loaded
loadCurrentUser();

// Add deposit functionality
document.getElementById('add-deposit-button').addEventListener('click', async () => {
    const addDepositInput = document.getElementById('add-deposit-input');
    const amount = parseFloat(addDepositInput.value);

    if (isNaN(amount) || amount <= 0) {
        alert('Please enter a valid positive amount.');
        return;
    }

    try {
        const response = await fetch('/user/adddeposite', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount })
        });

        const result = await response.json();
        if (response.ok && result.success) {
            alert('Deposit updated successfully!');
            await loadCurrentUser(); // Reload user information
            addDepositInput.value = ''; // Clear input field
        } else {
            alert(`Failed to update deposit: ${result.message}`);
        }
    } catch (error) {
        alert('Failed to update deposit.');
        console.error(error);
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
            // 定义支持的图片格式
            const formats = ['jpg', 'png', 'jpeg', 'gif'];
            let formatIndex = 0;
            // 尝试加载不同格式的图片
            function tryNextFormat() {
                if (formatIndex < formats.length) {
                    img.src = `/static/img/${product.name.replace(/\s+/g, '_')}.${formats[formatIndex]}`;
                    formatIndex++;
                } else {
                    // 如果所有格式都失败，则使用默认图片
                    img.src = '/static/img/default.jpg';
                }
            }
            // 当图片加载失败时尝试下一个格式
            img.onerror = tryNextFormat;
            // 开始尝试加载第一种格式
            tryNextFormat();
            img.alt = product.name;
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
            inventoryCell.setAttribute('data-inventory', product.inventory); // 保存库存信息
            row.appendChild(inventoryCell);

            // Category
            const categoryCell = document.createElement('td');
            categoryCell.textContent = product.category || 'N/A'; // show N/A if empty
            row.appendChild(categoryCell);

            // Description
            const descriptionCell = document.createElement('td');
            descriptionCell.textContent = product.description || 'N/A'; // show N/A if empty
            row.appendChild(descriptionCell);

            const purchaseCell = document.createElement('td');
            const quantityInput = document.createElement('input');
            quantityInput.type = 'number';
            quantityInput.min = 1;
            quantityInput.max = product.inventory;
            quantityInput.value = 1;
            quantityInput.style.width = '50px';

            const purchaseButton = document.createElement('button');
            purchaseButton.textContent = 'Buy';
            purchaseButton.addEventListener('click', async () => {
                const quantity = parseInt(quantityInput.value);
                if (isNaN(quantity) || quantity < 1 || quantity > product.inventory) {
                    alert('Invalid quantity');
                    return;
                }
            
                const totalCost = quantity * parseFloat(product.price); // 计算总价格
            
                try {
                    // 更新库存
                    const updateInventoryResponse = await fetch('/product/inventory', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            product_id: product.id,
                            change_amount: -quantity
                        })
                    });
            
                    const updateInventoryResult = await updateInventoryResponse.json();
                    if (!updateInventoryResponse.ok || !updateInventoryResult.success) {
                        throw new Error(updateInventoryResult.message || 'Failed to purchase product');
                    }
            
                    // 更新存款
                    const updateDepositResponse = await fetch('/user/minusdeposite', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ amount: totalCost }) // 扣减总价格
                    });
            
                    const updateDepositResult = await updateDepositResponse.json();
                    if (!updateDepositResponse.ok || !updateDepositResult.success) {
                        throw new Error(updateDepositResult.message || 'Failed to update deposit');
                    }
            
                    // 更新页面显示
                    product.inventory -= quantity;
                    inventoryCell.textContent = product.inventory;
                    quantityInput.max = product.inventory;
            
                    // 重新加载用户信息
                    await loadCurrentUser();
            
                    alert('Purchase successful');
                } catch (error) {
                    alert(`Error processing purchase: ${error.message}`);
                }
            });

            purchaseCell.appendChild(quantityInput);
            purchaseCell.appendChild(purchaseButton);
            row.appendChild(purchaseCell);

            tableBody.appendChild(row);
        });

        loadingMessage.style.display = 'none';
        table.style.display = 'table';
    } catch (error) {
        loadingMessage.textContent = `Error loading products: ${error.message}`;
    }
});
