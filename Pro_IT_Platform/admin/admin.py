import reflex as rx
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel
from ..admin.get_weather import get_weather
from .state import AuthState

def admin_panel():
    """Компонент админ-панели"""
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                rx.vstack(
                    rx.box(
                        rx.hstack(
                            rx.text("Главная страница", font_size="20px"),
                            rx.input(placeholder="Поиск", width="300px", style=input_style),
                            justify="between",
                            width="100%",
                            align="center", 
                            align_self="center"
                        ),
                        width="100%",
                    ),
                    padding="10px",
                    border_radius="5px",
                    background_color="#1c1e21",
                    width="100%",
                    height="100%",
                ),
                rx.box(get_weather()),
            ),
            width="90%",
            height="90vh",
            border_radius="20px",
            color="white",
            padding="20px",
            background_color=ADMIN_MAIN_CONTENT,
            margin="0 auto",  
        ),
        width="100%",
        height="100vh",
        color="white",
        padding="20px",
        background_color=ADMIN_BACKGROUND_COLOR,
        margin="0 auto",
    )