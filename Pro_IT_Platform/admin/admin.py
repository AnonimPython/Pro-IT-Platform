import reflex as rx
from .state import AuthState
from ..ui.colors import *

# rx.button("Выйти", on_click=AuthState.logout), 

def main_content():
    return rx.container(
        #* header
        rx.hstack(
            rx.heading("Pro-IT"),
            rx.spacer(),
            rx.button("Выйти", on_click=AuthState.logout),
        ),
        rx.hstack(
            rx.text("Приветствую EVG")    
        ),
        background_color=GRAY_LAVANDER,
        border_radius="10px",
    )