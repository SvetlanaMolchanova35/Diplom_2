import random
import time
import uuid
from faker import Faker
from helpers.data import ingredients

fake = Faker("ru_RU")


def generate_first_name() -> str:
    """
    Генерирует уникальное имя пользователя.
    Добавляем уникальный идентификатор чтобы избежать дубликатов.
    """
    unique_id = str(uuid.uuid4())[:6]  # Берем первые 6 символов UUID
    return f"User_{unique_id}"


def generate_email() -> str:
    """
    Генерирует уникальный email-адрес.
    Используем timestamp и UUID для гарантированной уникальности.
    """
    timestamp = int(time.time() * 1000)  # Текущее время в миллисекундах
    unique_id = str(uuid.uuid4())[:8]  # Уникальный идентификатор
    return f"test_{timestamp}_{unique_id}@test.com"


def generate_password() -> str:
    """
    Генерирует случайный пароль.
    """
    return fake.password()


def generate_data_user(
    include_first_name: bool = True,
    include_email: bool = True,
    include_password: bool = True
) -> dict:
    """
    Создает словарь с данными пользователя.

    Args:
        include_first_name (bool): Включать ли имя в данные
        include_email (bool): Включать ли email в данные
        include_password (bool): Включать ли пароль в данные

    Returns:
        dict: Словарь с данными пользователя
    """
    data_user = {}

    if include_first_name:
        data_user['name'] = generate_first_name()

    if include_email:
        data_user['email'] = generate_email()

    if include_password:
        data_user['password'] = generate_password()

    return data_user


def generate_body_order() -> dict:
    """
    Генерирует тело запроса для создания заказа.
    """
    # Разделяем ингредиенты на булочки и остальные
    buns = [item for item in ingredients if item['type'] == 'bun']
    others = [item for item in ingredients if item['type'] != 'bun']

    # Проверяем наличие булочек
    if not buns:
        raise ValueError("Нет доступных булочек для заказа")

    # Проверяем наличие дополнительных ингредиентов
    if not others:
        raise ValueError("Нет доступных дополнительных ингредиентов")

    # Выбираем случайную булочку
    bun = random.choice(buns)

    # Определяем максимальное количество доступных ингредиентов
    max_others = min(14, len(others))  # Ограничиваем выборку
    other_count = random.randint(1, max_others)  # Случайное кол-во инг-тов
    selected_others = random.sample(others, other_count)

    # Формируем список ID ингредиентов
    selected_ingredients = [
        bun['_id']
    ] + [item['_id'] for item in selected_others]

    # Создаем тело заказа
    body_order = {"ingredients": selected_ingredients}
    return body_order