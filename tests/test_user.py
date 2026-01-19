import allure
import pytest

from api.user_methods import User
from helpers import generation
from helpers.messages import Message


@allure.feature("Создание пользователя")
class TestCreateCourier:
    """
    Класс содержит тесты для проверки функциональности создания пользователей.
    Включает проверку успешных сценариев и обработку ошибок при регистрации.
    """

    @allure.story("Успешное создание уникального пользователя")
    @allure.title("Тест на успешное создание пользователя со всеми полями")
    def test_create_user_successful(self):
        """
        Тест проверяет успешное создание нового уникального пользователя
        с заполнением всех обязательных полей.
        """
        # Генерация данных для нового пользователя
        with allure.step("Генерация данных пользователя"):
            data_user = generation.generate_data_user()
            allure.attach(
                str(data_user),
                name="Сгенерированные данные пользователя",
                attachment_type=allure.attachment_type.JSON
            )

        # Регистрация пользователя
        with allure.step("Регистрация нового пользователя"):
            response = User.register_new_user(data_user)
            allure.attach(
                str(response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )
            access_token = response.json().get('accessToken')

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert response.status_code == 200, (
                f"Неверный статус код: {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get('success') is True, (
                "Операция не отмечена как успешная"
            )
            assert 'user' in response_json, "В ответе отсутствует пользователь"
            assert 'accessToken' in response_json, (
                "В ответе отсутствует токен доступа"
            )

        # Очистка после теста
        with allure.step("Удаление пользователя после теста"):
            User.delete_new_user(access_token)

    @allure.story("Ошибка при повторном создании пользователя")
    @allure.title("Тест на создание пользователя с уже существующим логином")
    def test_create_user_repeat_login_error(self, create_and_delete_user):
        """
        Тест проверяет обработку ошибки при попытке создания пользователя
        с уже существующим логином.
        """
        # Получение данных существующего пользователя
        with allure.step("Получение данных существующего пользователя"):
            data_user = create_and_delete_user
            allure.attach(
                str(data_user),
                name="Данные существующего пользователя",
                attachment_type=allure.attachment_type.JSON
            )

        # Попытка повторной регистрации
        with allure.step("Попытка повторной регистрации"):
            response = User.register_new_user(data_user)
            allure.attach(
                str(response.json()),
                name="Ответ сервера при ошибке",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert response.status_code == 403, (
                f"Неверный статус код: {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get('success') is False, (
                "Успех должен быть False при ошибке"
            )
            assert response_json.get('message') == Message.USER_ALREADY_EXISTS, (
                "Неверное сообщение об ошибке"
            )

    @allure.story("Ошибка при создании учетной записи без обязательных полей")
    @allure.title("Тест на создание учетной записи без обязательного поля")
    @pytest.mark.parametrize("data_user", [
        generation.generate_data_user(include_first_name=False),
        generation.generate_data_user(include_email=False),
        generation.generate_data_user(include_password=False),
    ])
    def test_create_user_no_required_field_error(self, data_user):
        """
        Тест проверяет обработку ошибок при отсутствии обязательных полей
        при создании учетной записи.
        """
       # Подготовка данных с отсутствующими полями
        with allure.step("Подготовка данных с отсутствующими полями"):
            allure.attach(
                str(data_user),
                name="Данные пользователя без обязательных полей",
                attachment_type=allure.attachment_type.JSON
            )

        # Попытка создания пользователя
        with allure.step("Попытка создания пользователя"):
            response = User.register_new_user(data_user)
            allure.attach(
                str(response.json()),
                name="Ответ сервера при ошибке",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert response.status_code == 403, (
                f"Неверный статус код: {response.status_code}"
            )
            response_json = response.json()
            assert response_json.get('success') is False, (
                "Успех должен быть False при ошибке"
            )
            assert (
                response_json.get('message') == Message.EMAIL_PASSWORD_NAME_REQUIRED
            ), "Неверное сообщение об ошибке"


@allure.feature("Авторизация пользователя")
class TestLoginUser:
    """
    Класс содержит тесты для проверки функциональности авторизации
    пользователей. Включает проверку как успешных сценариев,
    так и обработку ошибок при входе.
    """

    @allure.story("Успешная авторизация пользователя")
    @allure.title(
        "Тест на авторизацию пользователя при передаче всех обязательных полей"
    )
    def test_login_user_successful(self, create_and_delete_user):
        """
        Тест проверяет успешную авторизацию пользователя с корректными
        учетными данными.
        """
        # Получение данных созданного пользователя
        with allure.step("Получение данных пользователя"):
            data_user = create_and_delete_user
            allure.attach(
                str(data_user),
                name="Исходные данные пользователя",
                attachment_type=allure.attachment_type.JSON
            )

        # Выполнение запроса на авторизацию
        with allure.step("Авторизация пользователя"):
            login_response = User.login_user(
                data_user.get('email', ''),
                data_user.get('password', '')
            )
            allure.attach(
                str(login_response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )

        # Извлечение токена доступа
        access_token = login_response.json().get('accessToken')

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert login_response.status_code == 200, (
                f"Неверный статус код: {login_response.status_code}"
            )
            response_json = login_response.json()
            assert response_json.get('success') is True, (
                "Операция не отмечена как успешная"
            )
            assert 'user' in response_json, (
                "В ответе отсутствует информация о пользователе"
            )
            assert access_token, "Токен доступа не получен"
            allure.attach(
                f"Полученный токен: {access_token}",
                name="AccessToken",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.story("Ошибка при неправильном указании логина или пароля")
    @allure.title("Тест на авторизацию с некорректными данными")
    @pytest.mark.parametrize("error_value", ["email", "password"])
    def test_login_user_invalid_value_error(
        self, create_and_delete_user, error_value
    ):
        """
        Тест проверяет обработку ошибок при неверном вводе email или пароля.
        """
        # Копирование данных пользователя
        with allure.step("Подготовка исходных данных"):
            data_user = create_and_delete_user.copy()
            email = data_user.get('email', '')
            password = data_user.get('password', '')
            allure.attach(
                str(data_user),
                name="Исходные данные пользователя",
                attachment_type=allure.attachment_type.JSON
            )

        # Модификация некорректных данных
        with allure.step("Модификация некорректных данных"):
            if error_value == "email":
                data_user['email'] = 'errorERRORerror666@mail.com'
            elif error_value == "password":
                data_user['password'] = 'errorERRORerror666'
            allure.attach(
                str(data_user),
                name="Модифицированные данные",
                attachment_type=allure.attachment_type.JSON
            )

        # Попытка авторизации с некорректными данными
        with allure.step("Попытка авторизации с некорректными данными"):
            login_response = User.login_user(
                data_user.get('email', email),
                data_user.get('password', password)
            )
            allure.attach(
                str(login_response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )

           # Проверка результатов
            with allure.step("Проверка результатов"):
                assert login_response.status_code == 401, (
                    f"Неверный статус код: {login_response.status_code}"
                )
                response_json = login_response.json()
                assert response_json.get('success') is False, (
                    "Успех должен быть False при ошибке"
                )
                assert response_json.get('message') == Message.EMAIL_PASSWORD_INCORRECT, (
                    "Неверное сообщение об ошибке"
                )
                allure.attach(
                    str(response_json),
                    name="Ответ сервера при ошибке",
                    attachment_type=allure.attachment_type.JSON
                )

@allure.feature("Изменения данных пользователя")
class TestChangeUserData:
    """
    Класс содержит тесты для проверки функциональности изменения данных пользователя.
    Включает проверку как успешных сценариев, так и обработку ошибок при обновлении данных.
    """

    @allure.story("Успешное изменение данных пользователя")
    @allure.title("Тест на изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("value", ["email", "name"])
    def test_change_user_data_successful(
        self, create_and_delete_user, value
    ):
        """
        Тест проверяет успешное изменение данных пользователя (email или имени)
        при наличии корректной авторизации.
        """
        # Получение данных созданного пользователя
        with allure.step("Получение данных пользователя"):
            data_user = create_and_delete_user
            email = data_user.get('email', '')
            password = data_user.get('password', '')

        # Авторизация пользователя
        with allure.step("Авторизация пользователя"):
            login_response = User.login_user(
                data_user.get('email', email),
                data_user.get('password', password)
            )
            access_token = login_response.json().get('accessToken')
            allure.attach(
                f"Токен доступа: {access_token}",
                name="Access Token",
                attachment_type=allure.attachment_type.TEXT
            )

        # Подготовка обновленных данных
        with allure.step("Подготовка обновленных данных"):
            updated_data = data_user.copy()
            if value == "email":
                updated_data['email'] = "newemail123@mail.com"
            elif value == "name":
                updated_data['name'] = "NewUsername123"
            allure.attach(
                str(updated_data),
                name="Обновленные данные",
                attachment_type=allure.attachment_type.JSON
            )

        # Выполнение запроса на изменение данных
        with allure.step("Запрос на изменение данных"):
            change_response = User.change_user_data(
                access_token, updated_data
            )
            allure.attach(
                str(change_response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert change_response.status_code == 200, (
                f"Неверный статус код: {change_response.status_code}"
            )
            response_json = change_response.json()
            assert response_json.get('success') is True, (
                "Операция не отмечена как успешная"
            )
            assert 'user' in response_json, (
                "В ответе отсутствует информация о пользователе"
            )

    @allure.story("Ошибка при изменении данных пользователя")
    @allure.title("Тест на изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("value", ["email", "name"])
    def test_change_user_data_without_authorization_error(
        self, create_and_delete_user, value
    ):
        """
        Тест проверяет обработку ошибки при попытке изменения данных
        без предоставления токена авторизации.
        """
        # Получение данных созданного пользователя
        with allure.step("Получение данных пользователя"):
            data_user = create_and_delete_user
            email = data_user.get('email', '')
            password = data_user.get('password', '')

        # Попытка авторизации (токен будет сброшен)
        with allure.step("Попытка авторизации"):
            User.login_user(
                data_user.get('email', email),
                data_user.get('password', password)
            )
            access_token = None

        # Подготовка обновленных данных
        with allure.step("Подготовка обновленных данных"):
            updated_data = data_user.copy()
            if value == "email":
                updated_data['email'] = "newemail123@mail.com"
            elif value == "name":
                updated_data['name'] = "NewUsername123"
            allure.attach(
                str(updated_data),
                name="Обновленные данные",
                attachment_type=allure.attachment_type.JSON
            )

        # Попытка изменения данных без токена
        with allure.step("Попытка изменения данных без токена"):
            change_response = User.change_user_data(
                access_token, updated_data
            )
            allure.attach(
                str(change_response.json()),
                name="Ответ сервера",
                attachment_type=allure.attachment_type.JSON
            )

        # Проверка результатов
        with allure.step("Проверка результатов"):
            assert change_response.status_code == 401, (
                f"Неверный статус код: {change_response.status_code}"
            )
            response_json = change_response.json()
            assert response_json.get('success') is False, (
                "Успех должен быть False при ошибке"
            )
            assert response_json.get('message') == Message.WITHOUT_AUTHORIZATION, (
                "Неверное сообщение об ошибке"
            )