import reflex as rx

from rxconfig import config

#* PAGES
from .pages.main import main
from .pages.main import login


app = rx.App()

app.add_page(main,route="/",title="Main Page")
app.add_page(login,route="/login",title="Login Page")



# pip freeze > requirements.txt