class Message:
    """Класс для хранения сообщений об ошибках системы."""

    USER_ALREADY_EXISTS = 'User already exists'

    EMAIL_PASSWORD_NAME_REQUIRED = (
        'Email, password and name are required fields'
    )

    EMAIL_PASSWORD_INCORRECT = 'email or password are incorrect'

    WITHOUT_AUTHORIZATION = 'You should be authorised'

    WITHOUT_INGREDIENT = 'Ingredient ids must be provided'