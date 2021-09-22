import requests
import json
import logging


from django.conf import settings


def get_token():
    url_get_token = 'https://api.moyklass.com/v1/company/auth/getToken'
    body = {
        'apiKey': settings.MOY_KLASS_API_KEY,
    }
    additional_headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url_get_token, data=json.dumps(body), headers=additional_headers)
    except Exception as err:
        logging.exception('При запросе к url_get_token - ответ не был получен: ' + err)
    if response.status_code != 200:
        logging.exception('Ошибка при получении запроса')
    try:
        access_token = response.json()['accessToken']
        logging.info(f'Получен токен {access_token}')
    except KeyError as err:
        logging.exception('Токен не получен')
    return access_token


def delete_token(token):
    url_delete_token = 'https://api.moyklass.com/v1/company/auth/revokeToken'
    additional_headers = {'x-access-token': token}
    try:
        requests.post(url_delete_token, headers=additional_headers)
    except Exception as err:
        logging.exception('При запросе к delete_token - ответ не был получен: ' + err)
    finally:
        logging.info(f'Удален токен {token}')
