import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    return rx.container(
        
    )


app = rx.App()
app.add_page(index)



# pip freeze > requirements.txt