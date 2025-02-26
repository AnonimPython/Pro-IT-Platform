import reflex as rx
from ..pages.main import State
from ..ui.colors import *

def task_detail():
    """Page detail of task"""
    return rx.box(
    rx.vstack(
        rx.heading(f"Задание: {State.selected_task}", font_size="2em"),
        rx.heading(f"{State.selected_description}", font_size="2em"),
        rx.button(
            "Назад", 
            margin_top="20px",
            background=GRAY_LAVANDER,
            width="300px",
            font_size="30px",
            color=BLOCK_BACKGROUND,
            height="50px",
            padding="10px",
            border_radius="10px",
            _hover={
                    "background": INPUT_BACKGROUND,
                    "color":"white", 
                },
            transition="0.2s linear",
            on_click=rx.redirect("/")
        ),
        padding="20px",
        align="center", 
        width="100%",
    ),    
    background=BACKGROUND,
    width="100%",
    height="100vh",
    display="flex",
    justify_content="center",
    align_items="center",
)