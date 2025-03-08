import reflex as rx
from ..pages.main import MainState
from ..ui.colors import *

def task_detail():
    """Page showing task details."""
    return rx.box(
        rx.vstack(
            rx.heading(
                f"Задание {MainState.selected_task_id}",
                size="1",
            ),
            rx.text(
                MainState.current_task.text,
                font_size="1",
                margin_y="6",
            ),
            rx.button(
                "Назад",
                on_click=rx.redirect("/"),
                background=GRAY_LAVANDER,
                color=BLOCK_BACKGROUND,
                width="300px",
                height="50px",
                font_size="lg",
                padding="10px",
                border_radius="10px",
                _hover={
                    "background": INPUT_BACKGROUND,
                    "color": "white",
                },
                transition="0.2s linear",
            ),
            padding="6",
            align="center",
            max_width="800px",
            width="100%",
        ),
        width="100%",
        min_height="100vh",
        display="flex",
        justify_content="center",
        align_items="center",
        background=BACKGROUND,
    )