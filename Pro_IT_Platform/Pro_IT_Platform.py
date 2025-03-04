'''
 ▗▄▖ ▗▖  ▗▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖▗▖  ▗▖▗▄▄▖ ▗▖  ▗▖▗▄▄▄▖▗▖ ▗▖ ▗▄▖ ▗▖  ▗▖
▐▌ ▐▌▐▛▚▖▐▌▐▌ ▐▌▐▛▚▖▐▌  █  ▐▛▚▞▜▌▐▌ ▐▌ ▝▚▞▘   █  ▐▌ ▐▌▐▌ ▐▌▐▛▚▖▐▌
▐▛▀▜▌▐▌ ▝▜▌▐▌ ▐▌▐▌ ▝▜▌  █  ▐▌  ▐▌▐▛▀▘   ▐▌    █  ▐▛▀▜▌▐▌ ▐▌▐▌ ▝▜▌
▐▌ ▐▌▐▌  ▐▌▝▚▄▞▘▐▌  ▐▌▗▄█▄▖▐▌  ▐▌▐▌     ▐▌    █  ▐▌ ▐▌▝▚▄▞▘▐▌  ▐▌
'''

import reflex as rx

from rxconfig import config

from .admin.state import AuthState


#* UI
from .ui.colors import *


#* PAGES
from .pages.main import main
from .pages.login import login
from .pages.task_detail import task_detail
from .pages.error import error

#* ADMIN PAGES
from .admin.main import main as admin_main
from .admin.courses import courses
from .admin.students import students
from .admin.groups import GroupState, groups, group_page
from .admin.personal import personal
from .admin.auth_page import auth_page
from .admin.add_cours import courses_list, course_page
from .admin.main import main as admin_main


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
app.add_page(error, route='/404')

#* ADMIN PAGES
app.add_page(admin_main,route="/admin",title="Админ панель",on_load=AuthState.check_auth)
app.add_page(courses,route="/admin/courses_links",title="Ссылки",on_load=AuthState.check_auth)
app.add_page(students,route="/admin/students",title="Ученики",on_load=AuthState.check_auth)
app.add_page(groups,route="/admin/groups",title="Группы",on_load=AuthState.check_auth)
app.add_page(personal,route="/admin/personal",title="Персонал",on_load=AuthState.check_auth)
app.add_page(courses_list, route="/admin/courses",on_load=AuthState.check_auth)
app.add_page(auth_page, route="/auth") #* this page with inputs form to auth to admin panel
app.add_page(admin_main, route="/admin_main")#* this page need to check auth. If user is not logged in then redirect to /admin_main
app.add_page(course_page, route="/admin/courses/[course_id]",on_load=AuthState.check_auth)
app.add_page(
    group_page,
    route="/admin/groups/[group_id]",
    on_load=GroupState.load_group
)
#* API's


# pip freeze > requirements.txt