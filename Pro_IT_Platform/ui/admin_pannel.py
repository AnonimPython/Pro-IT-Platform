import reflex as rx

from ..admin.get_weather import get_weather
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
        rx.box(
            get_weather(),
            width="100%",
            background="linear-gradient(45deg, var(--tomato-9), var(--plum-9))",
            border_radius="15px",
            padding=["1em", "1.5em", "2em"],
            style={
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
            },
            _hover={
                "transform": "scale(1.02)",
                "transition": "all 1s ease-out;",
            },
        ),
        
        rx.box(
            rx.tooltip(
                rx.hstack(
                    rx.icon(tag="info",color="gray"),
                    rx.text("Бета тест",font_size="15px",color="gray"),
                    align="center",
                    align_self="center",
                ),
                content="Данный проект находиться на BETA тестировании, поэтому некоторые функции могут быть недоступны.",
            ),
            
            
        ),
        width="20%",
        padding="10px",
        margin_top="10px",
        margin_right="20px",
    )