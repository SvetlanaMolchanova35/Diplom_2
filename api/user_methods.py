import allure
import pytest
import requests

from helpers import urls


class User:
    """
    Класс для работы с пользовательским API.

    Содержит методы для регистрации, авторизации,
    изменения и удаления пользователей.
    """

    @staticmethod
    @allure.step("Создание нового пользователя")
    def register_new_user(data_user: dict) -> requests.Response:
        """
        Регистрирует нового пользователя в системе.

        Args:
            data_user (dict): Данные пользователя для регистрации

        Returns:
            requests.Response: Ответ сервера
        """
        response = requests.post(urls.CREATE_USER, json=data_user)
        return response

    @staticmethod
    @allure.step("Удаление нового пользователя")
    def delete_new_user(access_token: str):
        """
        Удаляет пользователя из системы.

        Args:
            access_token (str): Токен авторизации пользователя

        Raises:
            pytest.fail: Если удаление прошло неудачно
        """
        delete_headers = {
            'Accept': 'application/json',
            'Authorization': f'{access_token}'
        }

        # Отправляем DELETE-запрос для удаления пользователя
        delete_response = requests.delete(
            urls.DELETE_USER,
            headers=delete_headers
        )

        # Проверяем статус ответа
        if delete_response.status_code != 202:
            pytest.fail(
                f"Ошибка при удалении пользователя: "
                f"{delete_response.status_code} - {delete_response.text}"
            )

    @staticmethod
    @allure.step("Логин пользователя")
    def login_user(login: str, password: str) -> requests.Response:
        """
        Выполняет авторизацию пользователя.

        Args:
            login (str): Email пользователя
            password (str): Пароль пользователя

        Returns:
            requests.Response: Ответ сервера
        """
        login_response = requests.post(
            urls.LOGIN_USER,
            json={'email': login, 'password': password}
        )
        return login_response

    @staticmethod
    @allure.step("Изменить данные пользователя")
    def change_user_data(
        access_token: str,
        updated_data: dict
    ) -> requests.Response:
        """
        Изменяет данные существующего пользователя.

        Args:
            access_token (str): Токен авторизации пользователя
            updated_data (dict): Новые данные пользователя

        Returns:
            requests.Response: Ответ сервера
        """
        change_headers = {
            'Accept': 'application/json',
            'Authorization': f'{access_token}'
        }

        # Отправляем PATCH-запрос для изменения данных
        change_response = requests.patch(
            urls.CHANGE_USER_DATA,
            headers=change_headers,
            json=updated_data
        )
        return change_response