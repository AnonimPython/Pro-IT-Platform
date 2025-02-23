import reflex as rx
from ..ui.colors import *


def cours_card(text:str=None,link:str="#"):
    return rx.link(
        rx.box(
            rx.text(text, font_size="25px", weight="bold"),
            color="white",
            _hover={"color": ADMIN_YELLOW},
        ),
            width="300px",
            height="150px",
            border="YELLOW 1px solid",
            background_color=ADMIN_MAIN_CONTENT,
            border_radius="10px",
            padding="10px",
            display="flex",
            justify_content="center",
            align_items="center",
            transition="0.1s",
            _hover={"border": f"{ADMIN_YELLOW} 2px solid"},
            is_external=True,
            href=link,
    )