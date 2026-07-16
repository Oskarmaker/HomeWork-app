from schemas import TaskResponse


def build_task_response(task, task_student, teacher):
    return TaskResponse(id=task.id, name=task.name, text=task.text, answer_media=task_student.media_url,
                                task_media=task.media_url, deadline=task.deadline, creator=f"{teacher.surname} {teacher.name} {teacher.patronymic or ''}",
                                rating=task_student.rating, comment=task_student.comment, complete=task_student.complete)