import reflex as rx
from ..ui.colors import *


def main():
    return rx.vstack(
        #* header
        rx.box(
            rx.flex(
                #* logo and title
                rx.hstack(
                    rx.image("/logo.png", width="3em", border_radius="10px"),
                    rx.heading("Pro IT", font_size="2em"),
                    align="center",
                ),
                #* username
                rx.box(
                    rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.text("Никита Сидоров", font_size="30px",color="white"), 
                            variant="soft", 
                            # width="30%",
                            height="auto",
                            background_color=GRAY_LAVANDER,),
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Выход",
                            color="red",
                            _hover={"background_color": "#ff00001a"}
                        ),
                        width="100%"
                    ),
                ),    
                ),
                justify="between",
                align="center",
            ),
            width="100%",
        ),
        
        rx.separator(size="4",background=SEPARATOR_COLOR,margin_top="20px"),   
        #* main content
        rx.box(
            rx.hstack(
                #* left side
                rx.box(
                    rx.text("КУРС"),
                    rx.text("Scratch"),
                ),
                #* right side
                rx.box(rx.text("fewfwe")),
                width="100%",
            ),
            width="100%",
        ),
        padding="20px",
        color="white",
        width="100%",
    )