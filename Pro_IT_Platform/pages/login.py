import reflex as rx
from ..ui.colors import *
from sqlmodel import Session, select
from ..database.models import Student, engine

class LoginInputState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        print("Form data:", self.form_data)
        
        try:
            # Get form data
            login = form_data.get("login", "")
            password = form_data.get("password", "")

            # Connect to the database using SQLModel Session
            with Session(engine) as session:
                # Execute SQL query to find user
                statement = select(Student).where(Student.login == login, Student.password == password)
                user = session.exec(statement).first()

                if user:
                    # Save user data in cookies
                    # rx.set_cookie("student_id", str(user.id))  # Save student ID
                    # rx.set_cookie("course", user.course)  # Save course
                    return rx.redirect("/")  # Redirect to the main page if user is found
                else:
                    return rx.toast.error("Неверный логин или пароль!")  # Show error toast if user is not found

        except Exception as e:
            print(f"Login error: {str(e)}")
            return rx.toast.error("Произошла ошибка при входе в систему")


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
                            margin_bottom="20px",
                        ),                   
                        rx.box(
                            rx.link(
                                rx.text("Войти как преподаватель"),
                                href="/admin/",
                                color=BUTTON_BACKGROUND,
                                text_align="center",
                            ),
                            
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