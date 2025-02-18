import reflex as rx
from .state import AuthState
from .verify import auth_form
from .admin import main_content
from ..ui.colors import *


def main():
    return rx.box(
        rx.cond(
            AuthState.is_verified,  #* if user is verified
            main_content(),  #* main content
            rx.container(auth_form()),  #* form to enter google auth code
        ),
        width="100%",
        height="100vh",
        background_color=ADMIN_BACKGROUND_COLOR,
        padding_top="2%",
    )