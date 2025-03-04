import reflex as rx
from ..ui.colors import *

def error() -> rx.Component:
    return rx.box(
        rx.center(
            rx.vstack(
                rx.heading(
                    "404",
                    color="white",
                    font_size=["5em", "6em", "8em"],
                    background_image=f"linear-gradient(45deg, {BUTTON_BACKGROUND}, {ADMIN_YELLOW})",
                    background_clip="text",
                    font_weight="bold",
                    margin_bottom="1rem",
                ),
                rx.text(
                    "Страница потерялась в цифровых глубинах...",
                    font_size=["1.2em", "1.5em"],
                    color=ADMIN_LIGHT_GRAY,
                    text_align="center",
                ),
                rx.link(
                    rx.button(
                        rx.text("На главную", font_size="1.2em"),
                        size="1",
                        bg=BLOCK_BACKGROUND,
                        color=ADMIN_LIGHT_GRAY,
                        _hover={"transform": "scale(1.05)"},
                        padding_x="2rem",
                        border_radius="8px",
                        border=f"2px solid {ADMIN_BACKGROUND_COLOR}",
                        height="40px",
                        width="200px",
                    ),
                    href="/",
                ),
                spacing="4",
                align="center",
                padding="2rem",
            ),
            height="100vh",
            bg=ADMIN_MAIN_CONTENT,
        ),
        style={
            ".floating": {
                "animation": "floating 3s ease-in-out infinite",
                "@keyframes floating": {
                    "0%": {"transform": "translateY(0px)", "filter": "drop-shadow(0 5px 5px rgba(0,0,0,0.1))"},
                    "50%": {"transform": "translateY(-20px)", "filter": "drop-shadow(0 15px 15px rgba(0,0,0,0.2))"},
                    "100%": {"transform": "translateY(0px)", "filter": "drop-shadow(0 5px 5px rgba(0,0,0,0.1))"}
                }
            }
        }
    )