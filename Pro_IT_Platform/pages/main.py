import reflex as rx
from ..ui.colors import *


class State(rx.State):
    selected_module: int = 1

    def select_module(self, module: int):
        """Обработчик выбора модуля."""
        self.selected_module = module


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
        rx.hstack(
            #* left side
            rx.box(
                rx.text("КУРС", font_size="30px"),
                rx.heading("Scratch", font_size="45px"),
                rx.box(
                    rx.text("Модули", font_size="30px"),
                    rx.box(
                        rx.vstack(
                            rx.button("1-Стурктура", 
                                    on_click=lambda: State.select_module(1)),    
                            rx.button("2-база", 
                                    on_click=lambda: State.select_module(2)),    
                            rx.button("3-учеба", 
                                    on_click=lambda: State.select_module(3)),    
                            rx.button("4-перекус", 
                                    on_click=lambda: State.select_module(4)),    
                            rx.button("5-выпивка", 
                                    on_click=lambda: State.select_module(5)),
                            margin_top="20px",    
                        ),    
                    ),
                    margin_top="50px"    
                ),
                width="15%",
            ),
            rx.divider(orientation="vertical", size="4",height="700px",background=SEPARATOR_COLOR),
            #* right side
            rx.box(
                rx.cond(
                    State.selected_module == 1,
                    rx.text("Модуль 1 выбран - Структура"),
                    rx.cond(
                        State.selected_module == 2,
                        rx.text("Модуль 2 выбран - База"),
                        rx.cond(
                            State.selected_module == 3,
                            rx.text("Модуль 3 выбран - Учеба"),
                            rx.cond(
                                State.selected_module == 4,
                                rx.text("Модуль 4 выбран - Перекус"),
                                rx.text("Модуль 5 выбран - Выпивка")
                            )
                        )
                    )
                ),
                width="70%",
            ),
            spacing="4",
            width="100%",
            height="10vh"
        ),
        padding="20px",
        color="white",
        width="100%",
    )