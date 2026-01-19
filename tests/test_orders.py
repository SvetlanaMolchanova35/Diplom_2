import allure
from api.orders_methods import Order
from api.user_methods import User
from helpers.generation import generate_body_order
from helpers.messages import Message


@allure.feature("Создание заказа")
class TestCreateOrder:
    """
    Класс содержит набор тестов для проверки функциональности создания заказов.
    """
    
    @allure.story("Успешное создание заказа с авторизацией и с ингредиентами")
    @allure.title("Тест на создание заказа с авторизацией и с ингредиентами")
    def test_create_order_successful(self, login_in):
        """
        Тест проверяет успешное создание заказа с авторизованным пользователем
        """
        # Получение токена авторизации
        with allure.step("Получение токена авторизации"):
            login_response = login_in
            access_token = login_response.json().get('accessToken')
            allure.attach(
                f"Полученный токен: {access_token}",
                name="AccessToken",
                attachment_type=allure.attachment_type.TEXT
            )
            
        # Генерация тела заказа
        with allure.step("Генерация тела заказа"):
            body_order = generate_body_order()
            allure.attach(
                str(body_order),
                name="Тело заказа",
                attachment_type=allure.attachment_type.JSON
            )
            
        # Создание заказа
        with allure.step("Создание заказа"):
            order_response = Order.create_order(access_token, body_order)
            allure.attach(
                str(order_response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            
        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert order_response.status_code == 200, (
                f"Неверный статус код: {order_response.status_code}"
            )
            assert order_response.json().get('success') is True, (
                "Флаг успеха отсутствует в ответе"
            )
            assert 'order' in order_response.json(), "В ответе отсутствует order"

    @allure.story("Успешное создание заказа без авторизации")
    @allure.title("Тест на создание заказа без авторизации")
    def test_create_order_without_authorization_successful(
        self, create_and_delete_user
    ):
        """
        Тест проверяет возможность создания заказа без авторизации.
        Ожидаемый результат: заказ должен создаваться без токена авторизации.
        """
        # Получение данных пользователя
        with allure.step("Получение данных пользователя"):
            data_user = create_and_delete_user
            email = data_user.get('email', '')
            password = data_user.get('password', '')
            
        # Авторизация пользователя
        with allure.step("Авторизация пользователя"):
            User.login_user(
                data_user.get('email', email),
                data_user.get('password', password)
            )
            
        # Создание заказа без токена
        with allure.step("Создание заказа без токена"):
            access_token = None
            body_order = generate_body_order()
            order_response = Order.create_order(access_token, body_order)
            allure.attach(
                str(order_response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            
        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert order_response.status_code == 200, (
                f"Неверный статус код: {order_response.status_code}"
            )
            response_json = order_response.json()
            assert response_json.get('success') is True, (
                "Успех не возвращен в ответе"
            )
            assert 'order' in response_json, "В ответе отсутствует поле order"
            assert isinstance(response_json.get('order'), dict), (
                "В ответе API отсутствует подтверждение успешного выполнения"
            )

    @allure.story("Ошибка при создании заказа с авторизацией без ингредиентов")
    @allure.title("Тест на создание заказа с авторизацией без ингредиентов")
    def test_create_order_without_ingredient_error(self, login_in):
        """
        Тест проверяет обработку ошибки при попытке создания заказа
        без ингредиентов с авторизацией.
        """
        # Получение токена авторизации
        with allure.step("Получение токена авторизации"):
            login_response = login_in
            access_token = login_response.json().get('accessToken')
            allure.attach(
                f"Полученный токен: {access_token}",
                name="AccessToken",
                attachment_type=allure.attachment_type.TEXT
            )

        # Подготовка данных для запроса
        with allure.step("Подготовка данных для запроса"):
            body_order = None
            allure.attach(
                str(body_order),
                name="Тело запроса (пустое)",
                attachment_type=allure.attachment_type.JSON
            )

        # Создание заказа
        with allure.step("Создание заказа"):
            order_response = Order.create_order(access_token, body_order)
            allure.attach(
                str(order_response.json()),
                name="Ответ сервера при ошибке",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            response_json = order_response.json()
            assert order_response.status_code == 400, (
                f"Неверный статус код: {order_response.status_code}"
            )
            assert response_json.get('message') == Message.WITHOUT_INGREDIENT, (
                f"Неверное сообщение об ошибке: {response_json.get('message')}"
            )
            assert response_json.get('success') is False, (
                "Поле success должно принимать значение False при ошибке"
            )

    @allure.story(
        "Ошибка при создании заказа с авторизацией "
        "с неверным хешем ингредиентов"
    )
    @allure.title(
        "Тест на создание заказа с авторизацией "
        "с неверным хешем ингредиентов"
    )
    def test_create_order_incorrect_ingredient_error(self, login_in):
        """
        Тест проверяет обработку ошибки при попытке создания заказа
        с некорректными ID ингредиентов. Ожидается, что сервер вернет
        ошибку 500 при передаче невалидных идентификаторов ингредиентов.
        """
        # Получение токена авторизации
        with allure.step("Получение токена авторизации"):
            login_response = login_in
            access_token = login_response.json().get('accessToken')
            allure.attach(
                f"Полученный токен: {access_token}",
                name="AccessToken",
                attachment_type=allure.attachment_type.TEXT
            )

        # Подготовка данных заказа с некорректными ID
        with allure.step("Подготовка данных заказа"):
            body_order = {
                "ingredients": [
                    "abcdefghijklmnopqrst1",
                    "zyxwvutsrqponmlkjih1"
                ]
            }
            allure.attach(
                str(body_order),
                name="Тело запроса",
                attachment_type=allure.attachment_type.JSON
            )

        # Создание заказа
        with allure.step("Создание заказа"):
            order_response = Order.create_order(access_token, body_order)
            allure.attach(
                str(order_response.content),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.TEXT
            )

        # Проверка результата
        with allure.step("Проверка результатов"):
            assert order_response.status_code == 500, (
                f"Неверный статус код: {order_response.status_code}"
            )


@allure.feature("Получение заказов конкретного пользователя")
class TestGetOrder:
    """
    Класс содержит тесты для проверки функциональности получения заказов
    конкретного пользователя. Включает проверку как успешных сценариев,
    так и обработки ошибок.
    """

    @allure.story(
        "Успешное получение заказов конкретного пользователя с авторизацией"
    )
    @allure.title(
        "Тест на получение заказов конкретного пользователя с авторизацией"
    )
    def test_get_order_successful(self, login_in):
        """
        Тест проверяет возможность получения списка заказов
        авторизованным пользователем.
        """
        # Получение токена авторизации
        with allure.step("Получение токена авторизации"):
            login_response = login_in
            access_token = login_response.json().get('accessToken')
            assert access_token, "Токен авторизации не получен"
            allure.attach(
                f"Полученный токен: {access_token}",
                name="AccessToken",
                attachment_type=allure.attachment_type.TEXT
            )

        # Создание тестового заказа
        with allure.step("Создание тестового заказа"):
            body_order = generate_body_order()
            allure.attach(
                str(body_order),
                name="Тело тестового заказа",
                attachment_type=allure.attachment_type.JSON
            )
            create_response = Order.create_order(access_token, body_order)
            assert create_response.status_code == 200, (
                "Ошибка при создании тестового заказа"
            )
            allure.attach(
                str(create_response.json()),
                name="Ответ создания заказа",
                attachment_type=allure.attachment_type.JSON
            )

        # Получение списка заказов
        with allure.step("Получение списка заказов"):
            get_order_response = Order.get_order(access_token)
            allure.attach(
                str(get_order_response.json()),
                name="Ответ получения заказов",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert get_order_response.status_code == 200, (
                f"Неверный статус код: {get_order_response.status_code}"
            )
            response_json = get_order_response.json()
            assert response_json.get('success') is True, (
                "Операция не отмечена как успешная"
            )
            assert 'orders' in response_json, (
                "В ответе отсутствует список заказов"
            )

    @allure.story("Ошибка при попытке получения заказов без авторизации")
    @allure.title("Тест на получение заказов без авторизации")
    def test_get_order_without_authorization_error(self, login_in):
        """
        Тест проверяет обработку попытки получения заказов без авторизации.
        """
        # Получение токена и создание заказа для валидации
        with allure.step("Получение токена авторизации"):
            login_response = login_in
            access_token = login_response.json().get('accessToken')
            assert access_token, "Токен авторизации не получен"
            allure.attach(
                f"Полученный токен: {access_token}",
                name="AccessToken",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Создание тестового заказа"):
            body_order = generate_body_order()
            allure.attach(
                str(body_order),
                name="Тело тестового заказа",
                attachment_type=allure.attachment_type.JSON
            )
            create_response = Order.create_order(access_token, body_order)
            allure.attach(
                str(create_response.json()),
                name="Ответ создания заказа",
                attachment_type=allure.attachment_type.JSON
            )

        # Попытка получения заказов без токена
        with allure.step("Попытка получения заказов без авторизации"):
            access_token = None
            get_order_response = Order.get_order(access_token)
            allure.attach(
                str(get_order_response.json()),
                name="Ответ сервера при ошибке",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert get_order_response.status_code == 401, (
                f"Неверный статус код: {get_order_response.status_code}"
            )
            response_json = get_order_response.json()
            assert response_json.get('success') is False, (
                "Успех должен быть False при ошибке"
            )
            assert response_json.get('message') == Message.WITHOUT_AUTHORIZATION, (
                "Неверное сообщение об ошибке"
            )