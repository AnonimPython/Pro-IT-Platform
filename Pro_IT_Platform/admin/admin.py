import reflex as rx
from .state import AuthState
from ..ui.colors import *
from ..ui.admin_links import admin_links

# rx.button("Выйти", on_click=AuthState.logout), 
def main_content():
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.heading("Pro-IT", font_size="30px"),
                rx.text("EVG PYTHON", font_size="25px"),
                rx.text("Супер-Админ",color=ADMIN_YELLOW),
                #* links
                admin_links(),
                rx.button(
                    "Выйти",
                    on_click=AuthState.logout,
                    color="red",
                    background_color="#ff00001a",
                    _hover={"background_color": "#a60000","color":"520202",},  
                    width="100%",
                ), 
                
                width="20%",
                padding="10px",
                margin_top="10px",
            ),
            rx.vstack(
                rx.text("pewjgoiwejpw"),
                padding="10px",
            ),
        ),
        width="90%",
        border_radius="20px",
        color="white",
        padding="20px",
        background_color=ADMIN_MAIN_CONTENT,
        margin="0 auto",  
    )