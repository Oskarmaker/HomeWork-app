const token = localStorage.getItem("token");
const API_URL = "http://127.0.0.1:8000";
if (!token){
    window.location.href = "login.html";
}
async function uploadAnswer(taskId, fileInput) {
    const file = fileInput.files[0];
    if (!file) {
        alert("Сначала выбери файл");
        return;
    }
    const fd = new FormData();
    fd.append("file", file);
    const response = await fetch(`${API_URL}/student/me/tasks/${taskId}/load`, {
        method: "POST",
        headers: {"Authorization": "Bearer " + token},
        body: fd
    });
    if (response.ok) {
        alert("Ответ загружен");
        loadTasks();
    } else {
        alert("Ошибка загрузки");
    }
}
async function sendTask(taskId) {
    const response = await fetch(`${API_URL}/student/me/tasks/${taskId}/send`, {
        method: "POST",
        headers: {"Authorization": "Bearer " + token}
    });
    if (response.ok) {
        alert("Задание успешно загружено");
        loadTasks();
    } else {
        alert("Ошибка отправки")
    }
}

async function loadTasks(params) {
    const response = await fetch(`${API_URL}/student/me/tasks`, {
        headers: {"Authorization": "Bearer " + token},
        cache: "no-store"
    });
    const data = await response.json();
    console.log(data);
    const list = document.getElementById("tasks-list");
    list.innerHTML = "";
    for (const task of data){
        const li = document.createElement("li");
                
        const title = document.createElement("h2");
        title.textContent = task.name;
        li.appendChild(title);
        li.className = "task-card";

        const text = document.createElement("p");
        text.textContent = "Текст задания: " + task.text;
        li.appendChild(text);
        
        if (task.task_media != null){
            const task_media_link = document.createElement("a");
            task_media_link.href = `${API_URL}/${task.task_media}`;
            task_media_link.textContent = "Открыть задание";
            li.appendChild(task_media_link);
        }

        const deadline = document.createElement("p");
        deadline.textContent = "Дедлайн: " + new Date(task.deadline).toLocaleDateString("ru-RU");
        li.appendChild(deadline);

        const creator = document.createElement("p");
        creator.textContent = "Проверяющий: " + task.creator;
        li.appendChild(creator);

        if (task.rating != null){
            const rating = document.createElement("p");
            rating.textContent = "Оценка: " + task.rating;
            li.appendChild(rating);
        }

        if (task.comment != null){
            const comment = document.createElement("p");
            comment.textContent = "Комментарий: " + task.comment;
            li.appendChild(comment);
        }

        const status = document.createElement("p");
        status.textContent = "Состояние: " + (task.complete ? "Выполнено" : "Не выполнено");
        li.appendChild(status);

        if (!task.complete) {
            const fileInput = document.createElement("input");
            fileInput.type = "file";
            li.appendChild(fileInput);

            const uploadBtn = document.createElement("button");
            uploadBtn.textContent = "Загрузить ответ";
            uploadBtn.addEventListener("click", () => uploadAnswer(task.id, fileInput));
            li.appendChild(uploadBtn)

            const sendButton = document.createElement("button");
            sendButton.textContent = "Отправить задание";
            sendButton.addEventListener("click", () => sendTask(task.id));
            li.appendChild(sendButton);
        }

        if (task.answer_media != null){
            const btn_answer_media = document.createElement("button");
            btn_answer_media.textContent = "Мой ответ";
            btn_answer_media.addEventListener("click", () => downloadAnswer(task.id));
            li.appendChild(btn_answer_media);
        }

        list.appendChild(li);
    }
}
async function downloadAnswer(taskId) {
    const response = await fetch(`${API_URL}/student/me/tasks/${taskId}/file`, {
        headers: { "Authorization": "Bearer " + token}
    });
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    window.open(url);
}
const logoutBtn = document.getElementById("logout");
logoutBtn.addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "login.html";
});
loadTasks();
