import logging
from celery import chain

from django.apps import apps

from hello_music.celery import app
# from polls.views import send_message
from polls.authentications import get_token, delete_token
from polls.data_collection.moy_klass import (
    get_user_lessons,
    need_to_send_message,
    create_users_instance,
    get_users,
)


@app.task(name='task_get_token')
def task_get_token():
    """Таска по получению токена. """
    logging.info('Получили токен')
    return get_token()


@app.task(name='task_get_users_and_create_instances')
def task_get_users_and_create_instances(token):
    """Таска для получения и обработки пользователей. """
    users = get_users(token)
    create_users_instance(users)
    logging.info('Получили и наполнили таблицу с юзерами')
    return token


@app.task(name='task_check_all_active_users')
def task_check_all_active_users(token):
    student_model = apps.get_model('polls', 'Students')
    for student in student_model.objects.filter(
            status_id__in=[
                '61341',
                '109189',
                '103866',
                '103866',
                '103867',
            ]
    ):
        lessons = get_user_lessons(token, student.foreign_id)
        is_need_to_send_message, is_last_lesson_was_yesterday, passed_lessons = need_to_send_message(lessons)
        logging.info(
            f"""У пользователя {student.foreign_id} было {passed_lessons} пройденных занятий
            и последнее было вчера? Да, нет: {is_last_lesson_was_yesterday}""",
        )
        if is_need_to_send_message:
            task_send_message.delay(student.phone)
            logging.info(
                f"""Отправляем пользователю {student.foreign_id} 
                сообщение на телефон {student.phone}"""
            )
    logging.info('Завершили отправку сообщений')
    return token


@app.task(name='task_send_message')
def task_send_message(phone):
    """Таска по отправке сообщения пользователю.
    Args:
        phone: телефон пользователя
    """
    # send_message(phone)
    logging.info(f'Отправлено сообщение с отзывом {phone}')


@app.task(name='task_remove_token')
def task_remove_token(token):
    logging.info('Удалили токен')
    delete_token(token)


@app.task(name='task_chain')
def task_chain():
    """Запуск процедуры заполнения подготовительных данных для распределения."""
    tasks = [
        task_get_token.s(),
        task_get_users_and_create_instances.s(),
        task_check_all_active_users.s(),
        task_remove_token.s(),
    ]
    chain(*tasks).apply_async()
