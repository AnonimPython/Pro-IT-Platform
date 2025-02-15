import reflex as rx
from .state import AuthState

def main_content():
    return rx.vstack(
        rx.text("Основное окно", size="6", weight="bold"),
        rx.link("Ссылка 1", href="#"),
        rx.link("Ссылка 2", href="#"),
        rx.link("Ссылка 3", href="#"),
        rx.button("Выйти", on_click=AuthState.logout),  # Кнопка выхода
    )