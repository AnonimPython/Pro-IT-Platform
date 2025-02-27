from typing import List, Optional
import reflex as rx
from sqlmodel import Session, select
from ..database.models import Group, Student, Personal, engine
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel

class GroupState(rx.State):
    """State management for groups."""
    new_group_course: str = "" 
    courses: List[str] = ["Scratch", "Roblox", "Python", "Robotics", "GDevelop"]
    groups: List[Group] = []
    current_group: Optional[Group] = None
    students: List[Student] = []
    teachers: List[str] = []  #? list of personal (teachers)

    #* inputs for create group(s)
    new_group_name: str = ""
    new_group_school: str = ""
    new_group_course: str = ""
    new_group_description: str = ""
    new_teacher: str = ""  #* selected teacher

    #* inputs for create student(s)
    new_student_first_name: str = ""
    new_student_last_name: str = ""
    new_student_login: str = ""
    new_student_password: str = ""
    new_student_phone: str = ""
    new_student_school: str = ""
    new_student_class_number: str = ""

    @property
    def group_id(self) -> str:
        """Get the group ID from the page parameters."""
        return self.router.page.params.get("group_id", "")

    def load_groups(self):
        """Load all groups from the database."""
        with Session(engine) as session:
            self.groups = session.exec(select(Group)).all()

    def load_group(self):
        """Load the current group and its students."""
        group_id = self.group_id
        if group_id and group_id.isdigit():
            with Session(engine) as session:
                group = session.get(Group, int(group_id))
                if group:
                    self.current_group = group
                    self.students = list(group.students)

    def load_teachers(self):
        """Load all teachers from the database and sort by full name."""
        with Session(engine) as session:
            teachers = session.exec(
                select(Personal)
            ).all()
            #! TEST
            # print(f"Найдено преподавателей: {len(teachers)}")
            # for teacher in teachers:
                # print(f"Преподаватель: {teacher.full_name}, Роль: {teacher.role}")

            #* sort personal
            self.teachers = sorted([teacher.full_name for teacher in teachers])
            #! TEST
            # print(f"Список преподавателей: {self.teachers}")

    def add_group(self):
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
            self.load_groups()
            # Сбросить поля формы
            self.new_group_name = ""
            self.new_group_school = ""
            self.new_group_course = ""
            self.new_group_description = ""
            self.new_teacher = ""
            return rx.toast.success("Группа успешно добавлена")

    def delete_student(self, student_id: int):
        """Delete a student by ID."""
        with Session(engine) as session:
            student = session.get(Student, student_id)
            if student:
                session.delete(student)
                session.commit()
                self.load_group()
                return rx.toast.success("Студент успешно удален")
            else:
                return rx.toast.error("Студент не найден")

    def add_student(self):
        """Add a student to the group."""
        #? Check for empty fields
        if (
            not self.new_student_first_name
            or not self.new_student_last_name
            or not self.new_student_phone
            or not self.new_student_school
            or not self.new_student_class_number
            or not self.new_student_login
            or not self.new_student_password
        ):
            return rx.toast.warning("Заполните все поля")

        if not self.current_group:
            return rx.toast.error("Группа не выбрана")

        #? Check if class number is an integer
        try:
            class_number = int(self.new_student_class_number)
        except ValueError:
            return rx.toast.error("Класс должен быть числом")

        #* Check for uniqueness of phone number
        with Session(engine) as session:
            existing_student = session.exec(
                select(Student).filter(Student.phone == self.new_student_phone)
            ).first()
            if existing_student:
                return rx.toast.error("Студент с таким номером телефона уже существует.")

            #* Add student to the group
            student = Student(
                first_name=self.new_student_first_name,
                last_name=self.new_student_last_name,
                phone=self.new_student_phone,
                school=self.new_student_school,
                class_number=class_number,
                group_id=int(self.group_id),
                course=self.current_group.course,
                login=self.new_student_login,
                password=self.new_student_password,
            )
            session.add(student)
            try:
                session.commit()
                session.refresh(student)
                self.load_group()  #* reload list of students
                #* reset all inputs in dialog
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

            
    def set_new_group_course(self, value: str):
        self.new_group_course = value
            
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
                    #! In production change to rx.select
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

def student_list() -> rx.Component:
    return rx.cond(
        GroupState.students,
        rx.vstack(
            rx.text("Список студентов", font_size="30px", margin_bottom="20px", weight="bold"),
            rx.scroll_area(
                rx.flex(
                    rx.foreach(
                        GroupState.students,
                        lambda student:rx.box(
                            rx.button(
                                "Х",
                                on_click=lambda: GroupState.delete_student(student.id),
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
                            #! create login and password for acccount
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
        #! reamek design
        rx.text("В группе нет студентов", font_size="16px", margin_top="20px"),
    )

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
                                    # grid_template_columns=[
                                    #     "repeat(2, 1fr)",  
                                    #     "repeat(2, 1fr)",  
                                    #     "repeat(2, 1fr)",  
                                    #     "repeat(3, 1fr)",  
                                    #     "repeat(3, 1fr)",  
                                    #     "repeat(3, 1fr)",
                                    # ],
                                    # columns="3",
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
                            #! remake link to Yandex maps| 
                            # rx.link(
                            #     f"Школа: {GroupState.current_group.school}",
                            #     href=f"https://yandex.ru/maps/?text={GroupState.current_group.school}",
                            #     target="_blank",
                            # ),
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