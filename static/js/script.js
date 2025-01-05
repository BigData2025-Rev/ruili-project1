API_BASE_URL = "http://localhost:5000";

document.getElementById("register-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (data.success) {
        alert("Registration successful!");
    } else {
        alert(data.message || "Registration failed.");
    }
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (data.success) {
        localStorage.setItem("token", data.token); // Save token
        window.location.href = "/welcome";         // Redirect to welcome page
    } else {
        alert(data.message || "Login failed.");
    }
});
