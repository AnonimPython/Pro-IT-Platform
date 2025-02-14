import reflex as rx

from rxconfig import config

#* UI
from .ui.colors import *


#* PAGES
from .pages.main import main
from .pages.login import login
from .pages.task_detail import task_detail




app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
    ),
    #* font
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Rubik:ital,wght@0,300..900;1,300..900&display=swap"
    ],
    #* global styles
    style={
        "font_family": "Rubik",
        "background_color": BACKGROUND,
        "height": "100%",
        "width": "100%",
    }
)

app.add_page(main,route="/",title="Main Page")
app.add_page(login,route="/login",title="Login Page")
app.add_page(task_detail, route="/task/[task]")  # Страница с заданием



# pip freeze > requirements.txt