from typing import List, Optional
import reflex as rx
from sqlmodel import Session, select
from ..database.models import Group, Student, engine
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel

class GroupState(rx.State):
    """State management for groups."""
    groups: List[Group] = []
    current_group: Optional[Group] = None
    students: List[Student] = []
    new_group_name: str = ""
    new_group_school: str = ""
    new_group_course: str = ""
    new_group_description: str = ""
    new_student_first_name: str = ""
    new_student_last_name: str = ""
    new_student_phone: str = ""
    new_student_school: str = ""
    new_student_class_number: str = ""

    @property
    def group_id(self) -> str:
        return self.router.page.params.get("group_id", "")

    def load_groups(self):
        with Session(engine) as session:
            self.groups = session.exec(select(Group)).all()

    def load_group(self):
        group_id = self.group_id
        if group_id and group_id.isdigit():
            with Session(engine) as session:
                group = session.get(Group, int(group_id))
                if group:
                    self.current_group = group
                    self.students = list(group.students)

    def add_group(self):
        with Session(engine) as session:
            group = Group(
                name=self.new_group_name,
                school=self.new_group_school,
                course=self.new_group_course,
                description=self.new_group_description,
            )
            session.add(group)
            session.commit()
            session.refresh(group)
            self.load_groups()
            # Reset form fields
            self.new_group_name = ""
            self.new_group_school = ""
            self.new_group_course = ""
            self.new_group_description = ""

    def add_student(self):
        if not self.current_group:
            return
            
        try:
            class_number = int(self.new_student_class_number) if self.new_student_class_number else None
        except ValueError:
            return rx.window_alert("Класс должен быть числом")
            
        with Session(engine) as session:
            student = Student(
                first_name=self.new_student_first_name,
                last_name=self.new_student_last_name,
                phone=self.new_student_phone,
                school=self.new_student_school,
                class_number=class_number,  # Теперь может быть None
                group_id=int(self.group_id)
            )
            session.add(student)
            try:
                session.commit()
                session.refresh(student)
                self.load_group()
                # Reset form fields
                self.new_student_first_name = ""
                self.new_student_last_name = ""
                self.new_student_phone = ""
                self.new_student_school = ""
                self.new_student_class_number = ""
            except Exception as e:
                return rx.window_alert(f"Ошибка при добавлении студента: {str(e)}")

def add_group_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Создать группу"),
        ),
        rx.dialog.content(
            rx.dialog.title("Добавить новую группу"),
            rx.dialog.description("Заполните информацию о группе"),
            rx.form(
                rx.flex(
                    rx.input(
                        placeholder="Название группы",
                        value=GroupState.new_group_name,
                        on_change=GroupState.set_new_group_name,
                        required=True,
                    ),
                    rx.input(
                        placeholder="Школа",
                        value=GroupState.new_group_school,
                        on_change=GroupState.set_new_group_school,
                    ),
                    rx.input(
                        placeholder="Курс",
                        value=GroupState.new_group_course,
                        on_change=GroupState.set_new_group_course,
                    ),
                    rx.input(
                        placeholder="Описание",
                        value=GroupState.new_group_description,
                        on_change=GroupState.set_new_group_description,
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Отмена", variant="soft", color_scheme="gray"),
                        ),
                        rx.dialog.close(
                            rx.button("Сохранить", type="submit"),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=GroupState.add_group,
            ),
            max_width="450px",
        ),
    )

def student_list() -> rx.Component:
    return rx.cond(
        GroupState.students,
        rx.vstack(
            rx.text("Список студентов:", font_size="18px", margin_top="20px"),
            rx.foreach(
                GroupState.students,
                lambda student: rx.text(f"{student.first_name} {student.last_name}"),
            ),
        ),
        rx.text("В группе нет студентов", font_size="16px", margin_top="20px"),
    )

def add_student_form() -> rx.Component:
    return rx.vstack(
        rx.input(
            placeholder="Имя",
            value=GroupState.new_student_first_name,
            on_change=GroupState.set_new_student_first_name,
            style=input_style,
        ),
        rx.input(
            placeholder="Фамилия",
            value=GroupState.new_student_last_name,
            on_change=GroupState.set_new_student_last_name,
            style=input_style,
        ),
        rx.input(
            placeholder="Телефон",
            value=GroupState.new_student_phone,
            on_change=GroupState.set_new_student_phone,
            style=input_style,
        ),
        rx.input(
            placeholder="Школа",
            value=GroupState.new_student_school,
            on_change=GroupState.set_new_student_school,
            style=input_style,
        ),
        rx.input(
            placeholder="Класс",
            value=GroupState.new_student_class_number,
            on_change=GroupState.set_new_student_class_number,
            type_="number",
            min_="1",
            max_="11",
            style=input_style,
        ),
        rx.button("Добавить студента", on_click=GroupState.add_student),
        spacing="2",
        margin_top="20px",
    )

def groups() -> rx.Component:
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.text("Группы", font_size="20px"),
                        rx.input(placeholder="Поиск", width="300px", style=input_style),
                        justify="between",
                        width="100%",
                        align="center",
                        align_self="center",
                    ),
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        add_group_dialog(),
                        rx.foreach(
                            GroupState.groups,
                            lambda group: rx.link(
                                rx.vstack(
                                    rx.text(f"Группа: {group.name}"),
                                    rx.text(f"Школа: {group.school}"),
                                    rx.text(f"Курс: {group.course}"),
                                    rx.text(f"Описание: {group.description}"),
                                ),
                                href=f"/group/{group.id}",
                            ),
                        ),
                    ),
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
        on_mount=GroupState.load_groups,
    )

def group_page() -> rx.Component:
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                rx.cond(
                    GroupState.current_group,
                    rx.vstack(
                        rx.text(f"Группа: {GroupState.current_group.name}", font_size="20px"),
                        rx.text(f"Школа: {GroupState.current_group.school}"),
                        rx.text(f"Курс: {GroupState.current_group.course}"),
                        rx.text(f"Описание: {GroupState.current_group.description}"),
                        student_list(),
                        add_student_form(),
                    ),
                    rx.text("Группа не найдена", font_size="20px"),
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
        on_mount=GroupState.load_group,
    )