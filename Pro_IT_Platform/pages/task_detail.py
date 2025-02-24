import reflex as rx
from ..pages.main import State
from ..ui.colors import *

def task_detail():
    """Page detail of task"""
    return rx.box(
    rx.vstack(
        rx.heading(f"Задание: {State.selected_task}", font_size="2em"),
        rx.heading(f"{State.selected_description}", font_size="2em"),
        rx.button("Назад", on_click=rx.redirect("/")),
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