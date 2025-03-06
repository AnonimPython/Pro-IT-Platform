import reflex as rx
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel
from ..ui.info_card import info_card
from ..admin.get_weather import get_weather
from ..database.all_data import *




def admin_panel():
    #* take data
    personal_count = get_personal_count()
    students_count = get_students_count()
    groups_count = get_groups_count()

    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                #* main content | search
                rx.box(
                    rx.hstack(
                        #* search
                        rx.text("Главная страница", font_size="20px"),
                        rx.input(placeholder="Поиск", width="300px", style=input_style),
                        justify="between",
                        width="100%",
                        align="center", 
                        align_self="center"
                    ),
                    width="100%",
                ),
                #* cards with info
                rx.hstack(
                    info_card("Персонал", personal_count, "linear-gradient(45deg, var(--yellow-9), var(--orange-9))"),
                    info_card("Дети", students_count, "linear-gradient(45deg, var(--blue-9), var(--cyan-9))"),
                    info_card("Группы", groups_count, "linear-gradient(45deg, var(--red-9), var(--pink-9))"),
                    spacing="4",
                    width="100%",
                    padding="10px",
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
        color="white",
        padding="20px",
        background_color=ADMIN_BACKGROUND_COLOR,
        margin="0 auto", 
    )