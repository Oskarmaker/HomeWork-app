|№|endpoint путь|HTTP-метод|Входные данные|Выходные данные|Назначение|
|-|-|-|-|-----|---|
|1|/|GET|-|-|Базовый endpoint для переадресовки. Для выбора за кого входить(преподаватеьль или ученик)|
|2|/student/entry|POST|[login, password]|Сообщение об успешном входе или сообщение с ошибкой с HTTP кодом и JWT-токен|endpoint для входа в учетную запись для учеников|
|3|/teacher/entry|POST|[login, password]|Сообщение об успешном входе или сообщение с ошибкой с HTTP кодом и JWT-токен|endpoint для входа в учетную запись для преподавателей|
|4|/student/me/tasks|GET|-|Список задач для данного ученика([object Task (str: name, str: text, int: number, str: media_url, datetime: deadline, boolean: complete, int: rating)])|endpoint для отправки всех заданий для данного ученика|
|5|/student/me/tasks/{number}|GET|-|Данные о задаче с данным номером для данного ученика(object Task (str: name, str: text, int: number, str: media_url, datetime: deadline, boolean: complete, int: rating))|endpoint для отправки данных об определенном задании|
|6|/student/me/tasks/{number}/load|POST|Файл с данными для загрузки|Сообщение об успешной загрузке или сообщение об ошибке с HTTP кодом|endpoint для загрузки отвнта на задание студентом|
|7|/student/me/tasks/{number}/send|POST|-|Сообщение об успешной отправке или сообщение об ошибке с HTTP кодом|endpoint для отправки уведомления преподавателю что ученик выполнил задание|
|8|/teacher/me/students|GET|-|Список учеников с информацией о них(object Student(str: FIO, str: class_name, int: num_tasks, int: num_comp_tasks))|endpoint для отправки данных об учениках|
|9|/teacher/me/students/{student_login}/tasks|GET|-|Данные о заданиях учеников([object Task (str: name, str: text, int: number, str: media_url, datetime: deadline, boolean: complete, int: rating)])|endpoint для получения данных о заданиях|
|10|/teacher/me/students/{student_login}/tasks/{number_task}|GET|-|Данные о конкретном задании для конкретного ученика(object Task (str: name, str: text, int: number, str: media_url, datetime: deadline, boolean: complete, int: rating))|endpoint для получения данных о заданиях заданных данному ученику|
|11|/teacher/me/students/{student_login}/tasks/{number_task}/rating|POST|Оценка(2,3,4,5) с коментарием|Сообщение об успешном проставлении оценки или сообщение об ошибке с HTTP кодом|endpoint для проставления оценки за задание|
|12|/teacher/me/tasks|POST|Название задания, текст задания, кому оно назначено, до какого числа|Сообщение об успешном создании задния или сообщение об ошибке с HTTP кодом|endpoint для создания задания преподавателем|
|13|/teacher/me/tasks/{number}|PATCH|Изменения для задания(название задания, текст, дедлайн, кому назначено)|Сообщение об изменении задания или сообщение об ошибке с HTTP кодом|endpoint для исправления заданий|
|14|/teacher/me/tasks/{number}|DELETE|-|Сообщение об удалении или сообщение об ошибке с HTTP кодом|endpoint для удаления задания|