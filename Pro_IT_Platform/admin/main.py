import reflex as rx
from .state import AuthState
from .verify import auth_form
from .admin import main_content

def main():
    return rx.container(
        rx.cond(
            AuthState.is_verified,  # Проверяем, верифицирован ли пользователь
            main_content(),  # Основное окно
            auth_form(),  # Форма для ввода кода
        ),
    )