import reflex as rx
from ..ui.colors import *

class LoginInputState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        print("Form data:", self.form_data)

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

def login():
    return rx.center( 
        rx.hstack(
            rx.box(
                rx.image(
                    "/login_image.jpg",
                    width="100%",
                    height="500px",
                    object_fit="cover",
                    border_radius="10px",
                ),
                width="50%",
               
                
            ),
            rx.box(
                rx.vstack(
                    rx.heading(
                        "Pro-IT",
                        font_size="30px",
                        width="100%",
                        color="white",
                        margin_bottom="50px",
                        text_align="center",
                    ),
                    rx.box(
                        rx.text("Вход в систему",font_size="20px", color="white"),
                        #! on relize remove .root
                        rx.form.root(
                            rx.vstack(
                                rx.input(
                                    name="login",
                                    placeholder="Логин...",
                                    type="text",
                                    required=True,
                                    style=input_style
                                    ),
                                rx.input(
                                    name="password",
                                    placeholder="Пароль...",
                                    type="password",
                                    required=True,
                                    style=input_style
                                ),
                                rx.button(
                                    rx.text("Войти", font_size="20px"), 
                                    type="submit",
                                    background=BUTTON_BACKGROUND,
                                    width="300px",
                                    height="50px",
                                ),
                                width="100%",
                                # gap="30px",
                            ),
                            on_submit=LoginInputState.handle_submit,
                            reset_on_submit=True,
                        ),                   
                    ),
                ),
                padding="0px 100px 100px 0px",
                # width="50%",
                height="auto",
            ),
            
            width="900px",
            # height="0%",  
            spacing="8",  
            padding="15px",
            border_radius="10px",
            align_items="center",  
            background_color=BLOCK_BACKGROUND,
            color="white",
            justify="between",
            style={
                "-webkit-box-shadow": "0px 4px 64px 24px rgba(34, 60, 80, 0.3)",
                "-moz-box-shadow": "0px 4px 64px 24px rgba(34, 60, 80, 0.3)",
                "box-shadow": "0px 4px 64px 24px rgba(34, 60, 80, 0.3)",
            }
        ),
        width="100vw",  
        height="100vh",
        background_color=BACKGROUND,
    )