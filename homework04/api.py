import requests
import time
from typing import List
import config


def get(url: str, params: dict = {}, timeout: int = 5,
        max_retries: int = 5, backoff_factor: float = 0.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except requests.exceptions.RequestException:
            if i >= max_retries - 1:
                raise
            backoff = backoff_factor * (2 ** i)
            time.sleep(backoff)


def get_friends(user_id: int, fields: str):
    """ Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя,
    список друзей которого нужно получить
    :param fields: список полей, которые нужно получить
    для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = config.VK_CONFIG.get('access_token')
    user_id = user_id
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }
    query = "{domain}/friends.get?access_token=" \
            "{access_token}&user_id={user_id}&" \
            "fields={fields}&v=5.53".format(**query_params)
    response = get(query)
    return response.json()['response']


def messages_get_history(user_id: int, offset: int = 0,
                         count: int = 20) -> list:
    """ Получить историю переписки с указанным пользователем
    :param user_id: идентификатор пользователя,
    с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"
    access_token = config.VK_CONFIG.get('access_token')
    messages_history: list = []
    while count > 200:
        query_params = {
            'domain': domain,
            'access_token': access_token,
            'user_id': user_id,
            'offset': offset,
            'count': 200
        }
        query = "{domain}/messages.getHistory?access_token=" \
                "{access_token}&user_id={user_id}&offset={offset}" \
            "&count={count}&v=5.53".format(**query_params)
        response = get(query)
        messages_history.extend(response.json()['response']['items'])
        count -= 200
        offset += 200
        time.sleep(1/3)
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'offset': offset,
        'count': count
    }
    query = "{domain}/messages.getHistory?access_token" \
            "={access_token}&user_id={user_id}&offset={offset}" \
            "&count={count}&v=5.53".format(**query_params)
    response = get(query)
    messages_history.extend(response.json()['response']['items'])
    return messages_history
