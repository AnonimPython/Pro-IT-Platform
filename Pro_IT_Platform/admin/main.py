import reflex as rx
from .state import AuthState
from .auth_page import auth_page  # Импортируем auth_page из auth_page.py
from .admin import admin_panel  # Импортируем admin_panel из admin.py
from ..ui.colors import *

def main():
    return rx.box(
        rx.cond(
            AuthState.auth_token == "authenticated",  # Проверяем токен в LocalStorage
            admin_panel(),  # Админ-панель
            auth_page(),  # Страница авторизации
        ),
        width="100%",
        height="100vh",
        background_color=ADMIN_BACKGROUND_COLOR,
        padding_top="2%",
    )