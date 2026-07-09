const token = localStorage.getItem("token");
if (!token){
    window.location.href = "login.html";
}
async function loadTasks(params) {
    const response = await fetch("http://127.0.0.1:8000/student/me/tasks", {
        headers: {"Authorization": "Bearer " + token}
    });
    const data = await response.json();
    console.log(data);
    const list = document.getElementById("tasks-list");
    for (const task of data){
        const li = document.createElement("li");
        
        const title = document.createElement("h2");
        title.textContent = task.name;
        li.appendChild(title);

        const text = document.createElement("p");
        text.textContent = "Текст задания: " + task.text;
        li.appendChild(text);
        
        if (task.task_media != null){
            const task_media_link = document.createElement("a");
            task_media_link.href = task.task_media;
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

        if (task.answer_media != null){
            const link_answer_media = document.createElement("a");
            link_answer_media.href = task.answer_media;
            link_answer_media.textContent = "Мой ответ";
            li.appendChild(link_answer_media);
        }

        list.appendChild(li);
    }
}
loadTasks();
