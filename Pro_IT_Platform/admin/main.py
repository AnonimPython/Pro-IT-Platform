import reflex as rx
from .state import AuthState
from .auth_page import auth_page 
from .admin import admin_panel
from ..ui.colors import *

def main():
    return rx.box(
        rx.cond(
            AuthState.auth_token == "authenticated",  #* check token LocalStorage 
            admin_panel(), 
            auth_page(),
        ),
        width="100%",
        height="100vh",
        background_color=ADMIN_BACKGROUND_COLOR,
        padding_top="2%",
    )