document.getElementById('logout-button').addEventListener('click', async () => {
    const response = await fetch('/logout', { method: 'GET' });
    const result = await response.json();
    alert(result.message);
    window.location.href = '/'; // 跳转到主页
});
