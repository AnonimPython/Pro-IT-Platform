import reflex as rx
from sqlmodel import Session, select
from ..database.models import Student, Courses, Module, Task, engine
from ..ui.colors import *
from typing import List, Dict, Optional

class MainState(rx.State):
    selected_module_id: int = 0
    selected_task_id: int = 0
    current_task: Dict[str, str] = {}
    student_name: str = ""
    course_name: str = ""
    current_course_id: int = 0
    is_module_expanded: bool = False
    
    class ModuleType(rx.Base):
        id: int
        name: str
        tasks: List[Dict[str, str]]
    
    modules: List[ModuleType] = []

    @rx.var
    def has_modules(self) -> bool:
        return len(self.modules) > 0

    def reset_state(self):
        self.selected_module_id = 0
        self.selected_task_id = 0
        self.current_task = {}
        self.student_name = ""
        self.course_name = ""
        self.current_course_id = 0
        self.modules = []
        self.is_module_expanded = False

    @rx.event
    async def on_load(self):
        if self.current_course_id and not self.has_modules:
            with Session(engine) as session:
                modules = session.exec(
                    select(Module).where(Module.course_id == self.current_course_id)
                ).all()
                
                self.modules = [
                    self.ModuleType(
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

    @rx.event
    def select_module(self, module_id: int):
        if self.selected_module_id == module_id and self.is_module_expanded:
            self.is_module_expanded = False
            self.selected_module_id = 0
        else:
            self.selected_module_id = module_id
            self.is_module_expanded = True

    @rx.event
    def close_expanded_module(self):
        self.is_module_expanded = False
        self.selected_module_id = 0

    @rx.event
    def select_task(self, task_id: str, task_text: str):
        self.selected_task_id = int(task_id)
        self.current_task = {"id": task_id, "text": task_text}
        return rx.redirect(f"/task/{task_id}")

    @rx.event
    def logout(self):
        self.reset_state()
        return rx.redirect("/login")

def task_list(module: MainState.ModuleType):
    return rx.box(
        rx.flex(
            rx.foreach(
                module.tasks,
                lambda task: rx.box(
                    rx.vstack(
                        rx.text(
                            f"Задание {task['id']}",
                            font_size="18px",
                            font_weight="bold",
                            text_align="center",  # Центрирование текста
                            width="100%"  # Чтобы text_align работал корректно
                        ),
                        justify="center",  # Центрирование содержимого vstack
                        align_items="center",  # Центрирование по горизонтали
                        on_click=lambda t=task: MainState.select_task(t["id"], t["text"]),
                        width="250px",
                        height="150px",
                        padding="15px",
                        background=BUTTON_BACKGROUND,
                        color="white",
                        border_radius="10px",
                        _hover={
                            "background": INPUT_BACKGROUND,
                            "color": "white",
                            "transform": "scale(1.02)",
                            "cursor": "pointer"
                        },
                        transition="all 0.2s ease-in-out",
                        box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                    )
                ),
            ),
            wrap="wrap",
            spacing="4", 
            justify="start",
            align="start",
            width="100%",
        ),
        max_height="80vh",
        overflow_y="auto",
        padding="20px",
    )

def module_card(module: MainState.ModuleType):
    is_selected = MainState.selected_module_id == module.id
    return rx.box(
        rx.cond(
            is_selected,
            rx.center(
                rx.box(
                    rx.vstack(
                        rx.text(
                            module.name,
                            font_size="24px",
                            color="white",
                            text_align="center",
                            margin_bottom="20px",
                        ),
                        task_list(module),
                        align="center",
                        width="100%",
                        spacing="4",
                    ),
                    width="90%",
                    height="90vh", 
                    padding="20px",
                    background=BLOCK_BACKGROUND,
                    border_radius="10px",
                    box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                ),
                position="fixed",
                top="0",
                left="0",
                width="100%",
                height="100%",
                background="rgba(0, 0, 0, 0.5)",
                z_index="100",
                padding="2em",
                on_click=MainState.close_expanded_module,
            ),
            rx.button(
                rx.vstack(
                    rx.text(
                        module.name,
                        font_size="20px",
                        color="white",
                        text_align="center",
                    ),
                    align="center",
                    spacing="2",
                ),
                on_click=lambda: MainState.select_module(module.id),
                width="250px",
                height="150px",
                padding="15px",
                background=BLOCK_BACKGROUND,
                color="white",
                border_radius="10px",
                _hover={
                    "background": INPUT_BACKGROUND,
                    "color": "white",
                    "transform": "scale(1.05)",
                },
                transition="all 0.2s ease-in-out",
                box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
            ),
        ),
        margin="10px",
    )

def module_section():
    return rx.center(
        rx.vstack(
            rx.heading(
                "Модули",
                font_size="24px",
                color="white",
                margin_bottom="20px",
                text_align="center",
            ),
            rx.cond(
                MainState.has_modules,
                rx.flex(
                    rx.foreach(
                        MainState.modules,
                        lambda module: module_card(module)
                    ),
                    wrap="wrap",
                    justify="center",
                    align_items="center",
                    gap="4",
                    width="fit-content",
                    margin="0 auto",
                ),
                rx.text(
                    "Загрузка модулей...",
                    color="gray.500",
                    font_size="16px",
                ),
            ),
            width="100%",
            align_items="center",
        ),
        width="100%",
        height="100%",
        padding_top="2em",
    )

def header():
    return rx.hstack(
        rx.hstack(
            rx.image(
                src="/logo.png",
                width="48px",
                height="48px",
                border_radius="50%",
            ),
            rx.vstack(
                rx.heading(
                    "Pro IT",
                    font_size="24px",
                    color="white",
                ),
                rx.text(
                    MainState.student_name,
                    font_size="16px",
                    color="white",
                ),
                align="start",
                spacing="1",
            ),
            spacing="4",
        ),
        rx.spacer(),
        rx.hstack(
            rx.text(
                f"Курс: {MainState.course_name}",
                font_size="16px",
                color="white",
                align="center",
                align_self="center",
            ),
            rx.button(
                "Выйти",
                on_click=MainState.logout,
                background="transparent",
                color="white",
                transition="all 0.2s ease-in-out",
                _hover={
                    "background_color": "#a60000",
                    "color":"#400101",
                },
                padding="8px 16px",
                border_radius="8px",
            ),
            spacing="4",
        ),
        width="100%",
        padding="16px",
        align="center",
        align_self="center",
        border_bottom=f"1px solid {SEPARATOR_COLOR}",
        background=BLOCK_BACKGROUND,
    )

def main():
    return rx.box(
        rx.vstack(
            header(),
            rx.center(
                rx.container(
                    rx.vstack(
                        module_section(),
                        width="100%",
                        spacing="6",
                        align_items="center",
                        wrap="wrap",
                        justify="center",
                    ),
                    size="3",
                    center_content=True,
                ),
                width="100%",
                height="calc(100vh - 80px)",
            ),
            width="100%",
            height="100vh",
            spacing="0",
        ),
        background=BACKGROUND,
        color="white",
        on_mount=MainState.on_load,
    )