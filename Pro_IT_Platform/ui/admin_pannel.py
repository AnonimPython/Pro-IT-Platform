import reflex as rx
from ..ui.colors import *
from ..ui.admin_links import admin_links
from ..admin.state import AuthState


def admin_pannel():
    return rx.vstack(
        rx.heading("Pro-IT", font_size="30px"),
        rx.text(AuthState.current_user_name, font_size="25px"),
        rx.text(AuthState.current_user_role,color=ADMIN_YELLOW),
        #* links
        admin_links(),
        rx.button(
            "Выйти",
            on_click=AuthState.logout,
            color="red",
            background_color="#ff00001a",
            _hover={"background_color": "#a60000","color":"#400101",},  
            width="100%",
            transition="0.3s",
        ), 
        rx.separator(size="4", background=ADMIN_YELLOW, margin_top="20px"),
        width="20%",
        padding="10px",
        margin_top="10px",
        margin_right="20px",
    )