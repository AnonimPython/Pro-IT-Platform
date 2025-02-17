import reflex as rx
from .state import AuthState
from ..ui.colors import *

input_style: dict = {
    "width": "300px",
    "height": "50px",
    "--text-field-focus-color": BORDER_INPUT,
    "background": INPUT_BACKGROUND,
    "color": "white",
    "& input::placeholder": {
        "padding-left":"10px",
        "color": "white"
    },
    "font-size": "20px",
    }
def auth_form():
    return rx.center(
        rx.vstack(
            rx.text("Введите код из Google Authenticator", size="6", weight="bold",text_align="center",color="white"),
            #! on relize remove .root
            rx.form.root(
                rx.vstack(
                    rx.input(
                        placeholder="6-значный код",
                        value=AuthState.code,
                        on_change=AuthState.set_code,
                        style=input_style,
                        
                        
                    ),
                    rx.button(
                        "Войти",
                        type="submit",
                        width="300px",
                        background=BLOCK_BACKGROUND,
                        transition="0.3s",
                        _hover={
                            "background": BORDER_INPUT,
                        }
                        
                    ),
                    
                ),
                on_submit=AuthState.verify_and_redirect,
            ),
            width="100%",
            # spacing="4",
        ),
        height="100vh",
        width="100%",
    )