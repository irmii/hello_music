import requests
import logging
from datetime import date, timedelta

from polls.models import Students
from polls.consts import TRIAL_CLASS_ID


def get_users(token):
    url_get_users = 'https://api.moyklass.com/v1/company/users'
    additional_headers = {'x-access-token': token}
    response = requests.get(url_get_users, headers=additional_headers)
    return response.json()['users']


def create_users_instance(users):
    for user in users:
        obj, created = Students.objects.get_or_create(
            foreign_id=user['id'],
            defaults={
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'status_id': user['clientStateId'],
            },
        )
        if created:
            logging.info(f'Создан пользователь {obj.foreign_id}')
        else:
            obj.status_id = user['clientStateId']
            obj.phone = user['phone'],
            obj.save()
            logging.info(f'Пользователь {obj.foreign_id} уже существует в системе, обновим его статус и телефон')


def get_user_lessons(token, user_id):
    payload = {'userId': user_id}
    url_get_user_lessons = 'https://api.moyklass.com/v1/company/lessons/'
    additional_headers = {'x-access-token': token}
    response = requests.get(
        url_get_user_lessons,
        params=payload,
        headers=additional_headers,
    )
    return response.json()['lessons']


def need_to_send_message(lessons, token):
    count_lessons = 0
    last_lesson_was_yesterday = False
    previous_day = date.today() - timedelta(days=1)
    for lesson in lessons:
        lesson_class_id = lesson.get('classId')  # Пробные уроки имеют признак classId = TRIAL_CLASS_ID
        if lesson.get('status') == 1 and lesson_class_id != TRIAL_CLASS_ID:
            if check_visit(token, lesson.get('id')):  # Урок отмечен как проведенный и ученик посетил урок
                count_lessons += 1
            if date.fromisoformat(lesson.get('date')) == previous_day:
                last_lesson_was_yesterday = True
    if count_lessons == 3 and last_lesson_was_yesterday:
        return True, last_lesson_was_yesterday, count_lessons
    return False, last_lesson_was_yesterday, count_lessons


def check_visit(token, lesson_id):
    payload = {'lessonId': lesson_id}
    url_get_user_lesson_records = 'https://api.moyklass.com/v1/company/lessonRecords'
    additional_headers = {'x-access-token': token}
    response = requests.get(
        url_get_user_lesson_records,
        params=payload,
        headers=additional_headers,
    )
    return response.json()['lessonRecords'][0]['visit']
