document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/user/signin", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&scope=&client_id=&client_secret=`,
        });

        const data = await response.json();

        if (response.ok) {
            // Сохраняем токен в localStorage
            localStorage.setItem("access_token", data.access_token);
            // document.getElementById("message").innerText = "Login successful!";
            console.log(localStorage.getItem("access_token"));
            // Перенаправляем пользователя на защищенную страницу
            window.location.href = "/static/templates/requests.html";
        } else {
            console.error("Ошибка при входе:", data.detail || "Неизвестная ошибка");
            // document.getElementById("message").innerText = data.detail || "Ошибка при входе";
        }
    } catch (error) {
        console.error("Ошибка при отправке запроса:", error);
        // document.getElementById("message").innerText = "Ошибка при отправке запроса";
    }
});

window.addEventListener("load", async () => {
    const token = localStorage.getItem("access_token");
    if (token) {
        // Если токен есть, отправляем его на сервер
        const response = await fetch("/", {
            headers: {
                "Authorization": `Bearer ${token}`,
            },
        });
        if (response.ok) {
            // Если сервер подтвердил аутентификацию, остаемся на странице
            console.log("Authenticated");
        } else {
            // Если токен недействителен, перенаправляем на страницу входа
            window.location.href = "/";
        }
    } else {
        // Если токена нет, перенаправляем на страницу входа
        window.location.href = "/";
    }
});