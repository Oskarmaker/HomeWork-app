const form = document.getElementById("login-form");
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;
    console.log(login, password);
    const response = await fetch("http://127.0.0.1:8000/student/entry", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({login: login, password: password})
    });
    const data = await response.json();
    if (response.ok){
        localStorage.setItem("token", data.access_token);
        window.location.href = "tasks.html";
    } else {
        alert(data.detail);
    }

    console.log(data);
});