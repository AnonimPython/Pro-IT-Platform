import reflex as rx
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel
from ..ui.cours_card import cours_card


def courses() -> rx.Component:
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                #* main content | search
                rx.box(
                    rx.hstack(
                        #* search
                        rx.text("Курсы", font_size="20px"),
                        rx.input(placeholder="Поиск",width="300px",style=input_style),
                        justify="between",
                        width="100%",
                        align="center", align_self="center"
                    ),
                    width="100%",
                ),
                #* cards 
                #? grid style = 3 columns
                rx.box(
                      rx.grid(
                        #* card
                        cours_card(text="Scratch", link="https://drive.google.com/drive/folders/1ON1vlo9BESpLRiH_9ktADKvsuhcOI--l?clckid=3b2980a1"),
                        cours_card(text="Roblox",link="https://drive.google.com/drive/folders/1E87-_MSrNjbnxzJteNkk6kgi2NBMpu-i?clckid=3b2980a1"),
                        cours_card(text="Python 1st",link="https://drive.google.com/drive/folders/16hET92-hcYRydvxd8MEWqnEObbyNUFeZ?clckid=3b2980a1"),
                        cours_card(text="Python 2nd"),
                        cours_card(text="Robotics",link="https://drive.google.com/drive/folders/1lIdyMkBeE69h6JR7H6lAHHtQTBba0fgl?clckid=3b2980a1"),
                        cours_card(text="GDevelop",link="https://drive.google.com/drive/folders/1VGZGwUWFv39hSRJgfqTgCQ1FSCi9_lmf?clckid=3b2980a1"),
                        columns="3",
                        gap="1rem",
                        # spacing_x="2",
                        # spacing_y="2",
                        width="100%",
                    ),
                    width="100%",
                    margin_top="50px",
                ),
                padding="10px",
                border_radius="5px",
                background_color="#1c1e21",
                width="100%",
                height="100%",
            ),
            width="90%",
            height="90vh",
            border_radius="20px",
            color="white",
            padding="20px",
            background_color=ADMIN_MAIN_CONTENT,
            margin="0 auto",  
        ),
        
        
        width="100%",
        height="100vh",
        # border_radius="20px",
        color="white",
        padding="20px",
        background_color=ADMIN_BACKGROUND_COLOR,
        margin="0 auto", 
    )