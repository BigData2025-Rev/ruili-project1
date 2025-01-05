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
