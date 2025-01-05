document.addEventListener('DOMContentLoaded', () => {
    const tableBody = document.getElementById('users-table');

    // Fetch all users when "Check All Users" button is clicked
    document.getElementById('check-users-button').addEventListener('click', async () => {
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
