import reflex as rx
# from .state import AuthState
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel
from ..admin.get_weather import get_weather

# rx.button("Выйти", on_click=AuthState.logout), 
def main_content():
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                rx.vstack(
                #* main content | search
                rx.box(
                    rx.hstack(
                        #* search
                        rx.text("Главная страница", font_size="20px"),
                        rx.input(placeholder="Поиск",width="300px",style=input_style),
                        justify="between",
                        width="100%",
                        align="center", align_self="center"
                    ),
                    width="100%",
                ),
                padding="10px",
                border_radius="5px",
                background_color="#1c1e21",
                width="100%",
                height="100%",
            ),
            #* weather
                rx.box(
                    get_weather(),    
                ),
            ),
            
        ),
        width="90%",
        height="90vh",
        border_radius="20px",
        color="white",
        padding="20px",
        background_color=ADMIN_MAIN_CONTENT,
        margin="0 auto",  
    )