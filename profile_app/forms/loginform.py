from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class LoginUserForm(AuthenticationForm):
    """
    Класс формы авторизации пользователя
    """
    # Переопределение сообщение об ошибки из формы AuthenticationForm
    error_messages = {
        "invalid_login": (
            "Неверные логин или пароль. Попробуйте снова.\n"
            "Обратите внимание, что оба поля чувствительные к регистру."
        ),
    }

    # Переопределение функции из формы AuthenticationForm
    def clean(self):
        # Получаем username и password
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Проверка, что пользователь ввел пароль и логин
        if username is not None and password:
            # Пытаемся авторизовать пользователя по введённым данным. Возвращает None, если данные неверные или не сущ.
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            # Проверка, что пользователь не смог авторизоваться. Тогда выдаем ошибку.
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data