import reflex as rx

from rxconfig import config

#* UI
from .ui.colors import *


#* PAGES
from .pages.main import main
from .pages.login import login
from .pages.task_detail import task_detail

#* ADMIN PAGES
from .admin.main import main as admin_main
from .admin.courses import courses
from .admin.students import students
from .admin.groups import groups



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
        # "background_color": BACKGROUND,
        "height": "100%",
        "width": "100%",
    }
)
#* USER PAGES
app.add_page(main,route="/",title="Main Page")
app.add_page(login,route="/login",title="Login Page")
app.add_page(task_detail, route="/task/[task]")

#* ADMIN PAGES
app.add_page(admin_main,route="/admin",title="Админ панель")
app.add_page(courses,route="/admin/courses",title="Курсы")
app.add_page(students,route="/admin/students",title="Ученики")
app.add_page(groups,route="/admin/groups",title="Группы")

#* API's


# pip freeze > requirements.txt