import reflex as rx
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel
from typing import List
from sqlmodel import Session, select
from ..database.models import Student, engine

class StudentState(rx.State):
    students: List[Student] = []

    def load_students(self):
        """Load all students in the database"""
        with Session(engine) as session:
            self.students = session.exec(select(Student)).all()

def students() -> rx.Component:
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                #* main content | search
                rx.box(
                    rx.hstack(
                        #* search
                        rx.text("Ученики", font_size="20px"),
                        rx.input(placeholder="Поиск", width="300px", style=input_style),
                        justify="between",
                        width="100%",
                        align="center", align_self="center"
                    ),
                    width="100%",
                ),
                #* Список студентов
                rx.box(
                    rx.scroll_area(
                        rx.flex(
                            rx.foreach(
                                StudentState.students,
                                lambda student: rx.link(
                                    rx.box(
                                        rx.text(
                                            f"{student.first_name} {student.last_name}",
                                            font_size="20px",
                                        ),
                                        padding="10px",
                                        border_radius="5px",
                                        background=ADMIN_MAIN_CONTENT,
                                        _hover={"background": ADMIN_YELLOW},
                                    ),
                                    href=f"/admin/groups/{student.group_id}",  #* link to group
                                ),
                            ),
                            direction="column",
                            spacing="2",
                        ),
                        scrollbars="vertical",
                        type="scroll",
                        height="70vh",
                    ),
                    width="100%",
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
        on_mount=StudentState.load_students,  #* load all students
    )