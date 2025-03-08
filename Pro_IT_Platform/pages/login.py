import reflex as rx
from ..ui.colors import *
from sqlmodel import Session, select
from ..database.models import Student, Courses, Module, Task, engine
from ..pages.main import MainState

class LoginInputState(rx.State):
    form_data: dict = {}

    @rx.event
    async def handle_submit(self, form_data: dict):
        try:
            login = form_data.get("login", "")
            password = form_data.get("password", "")

            with Session(engine) as session:
                statement = select(Student).where(
                    Student.login == login, 
                    Student.password == password
                )
                user = session.exec(statement).first()

                if user:
                    # Get main state instance
                    main_state = await self.get_state(MainState)
                    
                    # Reset the state
                    main_state.reset_state()
                    
                    # Get course information
                    course = session.exec(
                        select(Courses).where(Courses.name == user.course)
                    ).first()
                    
                    if course:
                        # Set new state values
                        main_state.student_name = f"{user.first_name} {user.last_name}"
                        main_state.course_name = user.course
                        main_state.current_course_id = course.id
                        
                        # Load modules immediately
                        modules = session.exec(
                            select(Module).where(Module.course_id == course.id)
                        ).all()
                        
                        main_state.modules = [
                            main_state.ModuleType(
                                id=module.id,
                                name=module.name,
                                tasks=[
                                    {"id": str(t.id), "text": t.text}
                                    for t in session.exec(
                                        select(Task).where(Task.module_id == module.id)
                                    ).all()
                                ]
                            )
                            for module in modules
                        ]
                        
                        return rx.redirect("/")
                    else:
                        return rx.toast.error("Курс не найден")
                else:
                    return rx.toast.error("Неверный логин или пароль!")

        except Exception as e:
            print(f"Ошибка при входе: {str(e)}")
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
                        rx.text("Вход в систему", font_size="20px", color="white"),
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
                height="auto",
            ),
            width="900px",
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