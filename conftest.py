import pytest
import requests

from helpers import urls
from api.user_methods import User
from helpers import generation


@pytest.fixture
def create_and_delete_user():
    """
    Фиксатура для создания и удаления пользователя.
    Создает пользователя, возвращает его данные и удаляет после использования.

    Возвращает:
        dict: Данные созданного пользователя
    """
    # Генерация данных пользователя
    data_user = generation.generate_data_user()

    # Создание пользователя
    create_response = requests.post(
        urls.CREATE_USER,
        json=data_user
    )

    # Извлечение токена доступа
    user_access_token = create_response.json().get('accessToken')

    # Передача данных пользователя в тест
    yield data_user

    # Очистка: удаление пользователя после теста
    delete_headers = {
        'Accept': 'application/json',
        'Authorization': user_access_token
    }
    requests.delete(
        urls.DELETE_USER,
        headers=delete_headers
    )


@pytest.fixture
def login_in(create_and_delete_user):
    """
    Фиксатура для авторизации пользователя.
    Выполняет вход в систему с использованием созданных учетных данных.

    Возвращает:
        Response: Ответ сервера после авторизации
    """
    # Получение данных пользователя
    data_user = create_and_delete_user

    # Извлечение учетных данных
    email = data_user.get('email', '')
    password = data_user.get('password', '')

    # Выполнение авторизации
    login_response = User.login_user(email, password)

    return login_response