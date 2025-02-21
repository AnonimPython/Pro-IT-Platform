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
    new_teacher: str = ""
    
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
                teacher=self.new_teacher,
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
            self.new_teacher = ""
            
    def delete_student(self, student_id: int):
        """Delete studer by ID."""
        with Session(engine) as session:
            student = session.get(Student, student_id)
            if student:
                session.delete(student)
                session.commit()
                self.load_group()  #* reload the group list after delete
                return rx.toast("Студент успешно удален")
            else:
                return rx.toast("Студент не найден")
            
    def add_student(self):
        """Adding a student to the group"""
        #* check to empty input's
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

        #* protect for class number if input take str value
        try:
            class_number = int(self.new_student_class_number)
        except ValueError:
            return rx.toast.error("Класс должен быть числом")

        #* adding student to the group
        with Session(engine) as session:
            student = Student(
                first_name=self.new_student_first_name,
                last_name=self.new_student_last_name,
                phone=self.new_student_phone,
                school=self.new_student_school,
                class_number=class_number,
                group_id=int(self.group_id),
            )
            session.add(student)
            try:
                session.commit()
                session.refresh(student)
                self.load_group()  #* reload the group list after delete
                # Reset values from input's
                self.new_student_first_name = ""
                self.new_student_last_name = ""
                self.new_student_phone = ""
                self.new_student_school = ""
                self.new_student_class_number = ""
                return rx.toast.success("Студент успешно добавлен")
            except Exception as e:
                return rx.toast.error(f"Ошибка при добавлении студента: {str(e)}")

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
                        required=True,
                        
                    ),
                    rx.input(
                        placeholder="Курс",
                        value=GroupState.new_group_course,
                        on_change=GroupState.set_new_group_course,
                        required=True,
                        
                    ),
                    rx.input(
                        placeholder="Преподаватель",
                        value=GroupState.new_teacher,
                        on_change=GroupState.set_new_teacher,
                        required=True,
                        
                    ),
                    rx.input(
                        placeholder="Описание",
                        value=GroupState.new_group_description,
                        on_change=GroupState.set_new_group_description,
                        required=True,
                        
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