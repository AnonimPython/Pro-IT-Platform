from typing import List, Optional
import reflex as rx
from sqlmodel import Session, select
from ..database.models import Group, Student, Personal, Courses, engine
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel


class GroupState(rx.State):
    """State management for groups."""
    courses: List[str] = []  #? List of courses (dynamic)
    new_group_course: str = ""  #? Selected course
    groups: List[Group] = []  #? List of all groups
    current_group: Optional[Group] = None  #? Current selected group
    students: List[Student] = []  #? List of students in the current group
    teachers: List[str] = []  #? List of personal (teachers)

    #* inputs for create group
    new_group_name: str = ""
    new_group_school: str = ""
    new_group_description: str = ""
    new_teacher: str = ""  #* selected teacher

    #* inputs for create student
    new_student_first_name: str = ""
    new_student_last_name: str = ""
    new_student_login: str = ""
    new_student_password: str = ""
    new_student_phone: str = ""
    new_student_school: str = ""
    new_student_class_number: str = ""

    async def load_courses(self):
        """Load courses from the database."""
        with Session(engine) as session:
            courses = session.exec(select(Courses)).all()
            self.courses = [course.name for course in courses]  # Преобразуем в список названий

    async def load_teachers(self):
        """Load teachers from the database."""
        with Session(engine) as session:
            teachers = session.exec(select(Personal)).all()
            self.teachers = [teacher.full_name for teacher in teachers]

    async def load_groups(self):
        """Load all groups from the database."""
        with Session(engine) as session:
            self.groups = session.exec(select(Group)).all()
        await self.load_courses()  # Загрузить курсы

    async def load_group(self):
        """Load the current group and its students."""
        group_id = self.router.page.params.get("group_id", "")
        if group_id and group_id.isdigit():
            with Session(engine) as session:
                group = session.get(Group, int(group_id))
                if group:
                    self.current_group = group
                    self.students = session.exec(
                        select(Student).where(Student.group_id == int(group_id))
                    ).all()
                    
    async def delete_student(self, student_id: int):
        """Delete a student by ID."""
        with Session(engine) as session:
            student = session.get(Student, student_id)
            if student:
                session.delete(student)
                session.commit()
                await self.load_group()  # Перезагрузить группу
                return rx.toast.success("Студент успешно удален")
            else:
                return rx.toast.error("Студент не найден")


    async def add_group(self):
        """Add a new group."""
        if not self.new_group_name or not self.new_group_school or not self.new_group_course or not self.new_teacher:
            return rx.toast.warning("Заполните все обязательные поля")

        with Session(engine) as session:
            group = Group(
                name=self.new_group_name,
                school=self.new_group_school,
                course=self.new_group_course,
                description=self.new_group_description,
                teacher=self.new_teacher,
            )
            session.add(group)
            session.commit()
            session.refresh(group)
            await self.load_groups()  # Перезагрузить группы
            # Сбросить поля формы
            self.new_group_name = ""
            self.new_group_school = ""
            self.new_group_course = ""
            self.new_group_description = ""
            self.new_teacher = ""
            return rx.toast.success("Группа успешно добавлена")

    async def add_student(self):
        """Add a student to the group."""
        if (
            not self.new_student_first_name
            or not self.new_student_last_name
            or not self.new_student_phone
            or not self.new_student_school
            or not self.new_student_class_number
        ):
            return rx.toast.warning("Заполните все поля")

        if not self.current_group:
            return rx.toast.error("Группа не выбрана")

        try:
            class_number = int(self.new_student_class_number)
        except ValueError:
            return rx.toast.error("Класс должен быть числом")

        with Session(engine) as session:
            student = Student(
                first_name=self.new_student_first_name,
                last_name=self.new_student_last_name,
                phone=self.new_student_phone,
                login=self.new_student_login, # Добавить
                password=self.new_student_password, # Добавить
                school=self.new_student_school,
                class_number=class_number,
                group_id=int(self.current_group.id),
                course=self.current_group.course,
            )
            session.add(student)
            try:
                session.commit()
                session.refresh(student)
                await self.load_group()  #* reload
                # Сбросить поля формы
                self.new_student_first_name = ""
                self.new_student_last_name = ""
                self.new_student_phone = ""
                self.new_student_school = ""
                self.new_student_class_number = ""
                self.new_student_login = ""
                self.new_student_password = ""
                return rx.toast.success("Студент успешно добавлен")
            except Exception as e:
                return rx.toast.error(f"Ошибка при добавлении студента: {str(e)}")


def add_group_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button("Создать группу", on_click=GroupState.load_teachers),
        ),
        rx.dialog.content(
            rx.dialog.title("Добавить новую группу"),
            rx.dialog.description("Заполните информацию о группе"),
            rx.form.root(
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
                        required=True,
                    ),
                    rx.select.root(
                        rx.select.trigger(placeholder="Курс"),
                        rx.select.content(
                            rx.select.group(
                                rx.foreach(
                                    GroupState.courses,
                                    lambda course: rx.select.item(course, value=course)
                                )
                            ),
                        ),
                        value=GroupState.new_group_course,
                        on_change=GroupState.set_new_group_course,
                        required=True,
                    ),
                    rx.select.root(
                        rx.select.trigger(placeholder="Преподаватель"),
                        rx.select.content(
                            rx.select.group(
                                rx.foreach(
                                    GroupState.teachers,
                                    lambda teacher: rx.select.item(teacher, value=teacher)
                                )
                            ),
                        ),
                        value=GroupState.new_teacher,
                        on_change=GroupState.set_new_teacher,
                        required=True,
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

# Список студентов
def student_list() -> rx.Component:
    return rx.cond(
        GroupState.students,
        rx.vstack(
            rx.text("Список студентов", font_size="30px", margin_bottom="20px", weight="bold"),
            rx.scroll_area(
                rx.flex(
                    rx.foreach(
                        GroupState.students,
                        lambda student: rx.box(
                            rx.button(
                                "Х",
                                on_click=lambda student_id=student.id: GroupState.delete_student(student_id),
                                background_color="red",
                                color="white",
                                border_radius="50%",
                                size="1",
                                _hover={"background_color": "darkred"},
                            ),
                            rx.text(
                                f"{student.first_name} {student.last_name} {student.phone}",
                                font_size="25px",
                            ),
                        ),
                    ),
                    direction="column",
                    spacing="4",
                ),
                scrollbars="vertical",
                type="scroll",
                height="100%",
            ),
            padding="20px",
        ),
        rx.text("В группе нет студентов", font_size="16px", margin_top="20px"),
    )
# Форма для добавления студента
def add_student_form() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Добавить ученика",
                background_color=LINK_BACKGROUND_COLOR,
                border=f"1px solid {ADMIN_YELLOW}",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Добавить ученика"),
            rx.dialog.description(
                "В данном окне введите правильные значения для добавления ребенка в группу",
            ),
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Имя",
                        value=GroupState.new_student_first_name,
                        on_change=GroupState.set_new_student_first_name,
                        style=admin_input_style
                    ),
                    rx.input(
                        placeholder="Фамилия",
                        value=GroupState.new_student_last_name,
                        on_change=GroupState.set_new_student_last_name,
                        style=admin_input_style,
                    ),
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Логин",
                        value=GroupState.new_student_login,
                        on_change=GroupState.set_new_student_login,
                        style=admin_input_style
                    ),
                    rx.input(
                        placeholder="Пароль",
                        value=GroupState.new_student_password,
                        on_change=GroupState.set_new_student_password,
                        style=admin_input_style,
                    ),
                ),
                rx.input(
                    placeholder="Телефон",
                    value=GroupState.new_student_phone,
                    on_change=GroupState.set_new_student_phone,
                    style=admin_input_style,
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Школа",
                        value=GroupState.new_student_school,
                        on_change=GroupState.set_new_student_school,
                        style=admin_input_style,
                    ),
                    rx.input(
                        placeholder="Класс",
                        value=GroupState.new_student_class_number,
                        on_change=GroupState.set_new_student_class_number,
                        type_="number",
                        min_="1",
                        max_="11",
                        style=admin_input_style,
                    ),
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Отмена",
                            size="2", 
                            color="red",  
                            background_color="#ff00001a",
                            border="1px solid red",
                            margin="5px",
                            transition="all 0.2s ease-in-out",
                            _hover={
                                "background_color": "#851f2f",
                            }
                        ),
                    ),
                    rx.button(
                        "Добавить",
                        size="2", 
                        color="green",  
                        border="1px solid green",
                        background_color="#00ff001a",
                        margin="5px",
                        transition="all 0.2s ease-in-out",
                        _hover={
                            "background_color": "#56d551",
                        },
                        on_click=GroupState.add_student
                    ),
                ),
                spacing="2",
                margin_top="20px",
            ),
            style={
                "background": ADMIN_MAIN_CONTENT,  
                "color": "white" 
            },
        ),
        color_scheme="dark",
    )

# Страница со списком групп
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
                        rx.box(
                            rx.scroll_area(
                                rx.flex(
                                    rx.foreach(
                                        GroupState.groups,
                                        lambda group: rx.link(
                                            rx.vstack(
                                                rx.text(f"Группа: {group.name}"),
                                                rx.text(f"Школа: {group.school}"),
                                                rx.text(f"Курс: {group.course}"),
                                                rx.text(f"Описание: {group.description}"),
                                                rx.text(f"Преподаватель: {group.teacher}"),
                                                background=ADMIN_MAIN_CONTENT,
                                                padding="10px",
                                                border_radius="10px",
                                                width="300px",
                                            ),
                                            href=f"/admin/groups/{group.id}",
                                        ),
                                    ),
                                    flex_wrap="wrap",
                                    spacing="4",
                                    width="100%",
                                ),
                                type="hover",
                                scrollbars="vertical",
                                style={"height": "70vh"},
                                width="100%",
                            ),
                            width="100%",
                        ),
                        width="100%",
                        height="100%",
                    ),
                    height="100%",
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
        on_mount=GroupState.load_groups,
    )

# Страница группы
def group_page() -> rx.Component:
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                rx.cond(
                    GroupState.current_group,
                    rx.hstack(
                        rx.vstack(
                            rx.text(f"Группа: {GroupState.current_group.name}", font_size="20px"),
                            rx.text(f"Школа: {GroupState.current_group.school}"),
                            rx.text(f"Преподаватель: {GroupState.current_group.teacher}"),
                            rx.text(f"Курс: {GroupState.current_group.course}"),
                            rx.text(f"Описание: {GroupState.current_group.description}"),
                            add_student_form(),
                            spacing="4",
                        ),
                        rx.box(
                            student_list(),  
                            margin_left="30%",  
                            border_radius="15px",
                            min_width="50%",
                            background_color=ADMIN_MAIN_CONTENT
                        ),
                        width="100%",
                    ),
                    rx.text("Группа не найдена", font_size="20px"),
                ),
                padding="40px",
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
