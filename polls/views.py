import requests

from django.conf import settings


def get_text_from_template(path):
    with open(path) as file:
        data = file.read()
    return data


def send_message(phone):
    url = settings.SMS_API_URL
    api_key = settings.SMS_API_KEY
    text_message = get_text_from_template('templates/poll_after_third_lesson')
    query_params = {
        'api_key': api_key,
        'text': text_message,
        'to': phone,
    }
    request = requests.get(url, params=query_params, verify=False)
    return request.status_code
