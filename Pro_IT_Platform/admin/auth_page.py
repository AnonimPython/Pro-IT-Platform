import reflex as rx
from .state import AuthState 
from ..ui.colors import *

def auth_page():
    """Страница авторизации"""
    return rx.center(
        rx.vstack(
            rx.text("Введите код из Google Authenticator", 
                   size="6", 
                   weight="bold",
                   text_align="center",
                   color="white"
            ),
            rx.cond(
                ~AuthState.show_login_field,
                rx.vstack(
                    rx.input(
                        placeholder="6-значный код",
                        value=AuthState.code,
                        on_change=AuthState.set_code,
                        style=input_style,
                    ),
                    rx.button(
                        "Проверить код",
                        on_click=AuthState.verify_code,
                        width="300px",
                        background=BLOCK_BACKGROUND,
                        transition="0.3s",
                        _hover={"background": BORDER_INPUT}
                    ),
                    align_items="center", # Добавлено
                ),
                rx.vstack(
                    rx.input(
                        placeholder="Логин",
                        value=AuthState.login,
                        on_change=AuthState.set_login,
                        style=input_style,
                    ),
                    rx.button(
                        "Войти",
                        on_click=AuthState.verify_login,
                        width="300px",
                        background=BLOCK_BACKGROUND,
                        transition="0.3s",
                        _hover={"background": BORDER_INPUT}
                    ),
                    align_items="center", # Добавлено
                ),
            ),
            width="100%",
            align_items="center", # Добавлено
            justify_content="center", # Добавлено
        ),
        height="100vh",
        width="100%",
        color="white",
        padding="20px",
        background_color=ADMIN_BACKGROUND_COLOR,
        margin="0 auto",
        align_items="center", # Добавлено
        justify_content="center", # Добавлено
    )