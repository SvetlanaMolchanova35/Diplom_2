import allure
import requests
from helpers import urls


class Order:
    """
    Класс для работы с заказами в API.

    Содержит методы для создания и получения заказов.
    """

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(access_token: str, body_order: dict) -> requests.Response:
        """
        Создает новый заказ в системе.

        Args:
            access_token (str): Токен авторизации пользователя
            body_order (dict): Тело запроса с данными заказа

        Returns:
            requests.Response: Ответ сервера
        """
        order_headers = {
            'Accept': 'application/json',
            'Authorization': access_token
        }

        # Отправляем POST-запрос на создание заказа
        order_response = requests.post(
            urls.CREATE_ORDER,
            headers=order_headers,
            json=body_order
        )
        return order_response

    @staticmethod
    @allure.step("Получение заказа")
    def get_order(access_token: str) -> requests.Response:
        """
        Получает информацию о заказах пользователя.

        Args:
            access_token (str): Токен авторизации пользователя

        Returns:
            requests.Response: Ответ сервера
        """
        order_headers = {
            'Accept': 'application/json',
            'Authorization': access_token
        }

        # Отправляем GET-запрос для получения заказов
        get_order_response = requests.get(
            urls.GET_USER_ORDER,
            headers=order_headers
        )
        return get_order_response