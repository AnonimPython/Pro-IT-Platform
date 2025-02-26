import reflex as rx
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel

from typing import List
from sqlmodel import Session, select
from ..database.models import Personal, engine

class PersonalState(rx.State):
    personal: List[Personal] = []

    # Поля для нового человека
    new_login: str = ""
    new_full_name: str = ""
    new_role: str = ""
    new_phone: str = ""

    def load_personal(self):
        """Загрузить всех сотрудников из базы данных"""
        with Session(engine) as session:
            self.personal = session.exec(select(Personal)).all()

    def add_personal(self):
        """Добавить нового сотрудника"""
        if not self.new_login or not self.new_full_name or not self.new_role or not self.new_phone:
            return rx.toast.warning("Заполните все поля")

        with Session(engine) as session:
            person = Personal(
                login=self.new_login,
                full_name=self.new_full_name,
                role=self.new_role,
                phone=self.new_phone,
            )
            session.add(person)
            session.commit()
            session.refresh(person)
            self.load_personal()  # Перезагрузить список сотрудников
            # Сбросить поля формы
            self.new_login = ""
            self.new_full_name = ""
            self.new_role = ""
            self.new_phone = ""
            return rx.toast.success("Сотрудник успешно добавлен")

def add_personal_form() -> rx.Component:
    """Форма для добавления нового сотрудника"""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Добавить человека",
                background_color=LINK_BACKGROUND_COLOR,
                border=f"1px solid {ADMIN_YELLOW}",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Добавить сотрудника"),
            rx.dialog.description(
                "Введите данные нового сотрудника",
            ),
            rx.vstack(
                rx.input(
                    placeholder="Логин",
                    value=PersonalState.new_login,
                    on_change=PersonalState.set_new_login,
                    style=admin_input_style
                ),
                rx.input(
                    placeholder="ФИО",
                    value=PersonalState.new_full_name,
                    on_change=PersonalState.set_new_full_name,
                    style=admin_input_style,
                ),
                rx.input(
                    placeholder="Роль",
                    value=PersonalState.new_role,
                    on_change=PersonalState.set_new_role,
                    style=admin_input_style,
                ),
                rx.input(
                    placeholder="Телефон",
                    value=PersonalState.new_phone,
                    on_change=PersonalState.set_new_phone,
                    style=admin_input_style,
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
                        on_click=PersonalState.add_personal
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

def personal():
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                #* main content | search
                rx.box(
                    rx.hstack(
                        #* search
                        rx.text("Персонал", font_size="20px"),
                        rx.input(placeholder="Поиск",width="300px",style=input_style),
                        justify="between",
                        width="100%",
                        align="center", align_self="center"
                    ),
                    width="100%",
                ),
                rx.box(
                    add_personal_form(),    
                ),
                rx.box(
                    rx.scroll_area(
                        rx.grid(
                            rx.foreach(
                                PersonalState.personal,
                                lambda person: rx.box(
                                        rx.vstack(
                                            rx.text(person.full_name),
                                            rx.text(person.role),
                                            rx.text(person.phone),
                                            font_size="20px",
                                        ),
                                        padding="10px",
                                        border_radius="5px",
                                        background=ADMIN_MAIN_CONTENT,
                                        border=f"1px solid {ADMIN_YELLOW}",
                                        width="100%",
                                        flex_wrap="wrap",
                                ),
                            ),
                            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
                            spacing="4",
                            width="100%",
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
        on_mount=PersonalState.load_personal,
    )