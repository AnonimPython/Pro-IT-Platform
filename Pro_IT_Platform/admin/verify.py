import reflex as rx
from .state import AuthState

def auth_form():
    return rx.container(
        rx.text("Google Authenticator", size="6", weight="bold"),
        rx.form.root(
            rx.vstack(
                rx.input(
                    placeholder="Введите код из Google Authenticator",
                    value=AuthState.code,
                    on_change=AuthState.set_code,
                ),
                rx.button("Отправить", type="submit"),
            ),
            on_submit=AuthState.verify_and_redirect,
        ),
    )