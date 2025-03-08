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
    
    class ModuleType(rx.Base):
        id: int
        name: str
        tasks: List[Dict[str, str]]
    
    modules: List[ModuleType] = []

    @rx.var
    def has_modules(self) -> bool:
        """Check if modules are loaded."""
        return len(self.modules) > 0

    def reset_state(self):
        """Reset state variables to default values."""
        self.selected_module_id = 0
        self.selected_task_id = 0
        self.current_task = {}
        self.student_name = ""
        self.course_name = ""
        self.current_course_id = 0
        self.modules = []

    @rx.event
    async def on_load(self):
        """Load modules if we have a course_id but no modules loaded."""
        if self.current_course_id and not self.has_modules:
            with Session(engine) as session:
                # Get modules for current course
                modules = session.exec(
                    select(Module).where(Module.course_id == self.current_course_id)
                ).all()
                
                # Transform modules into required format
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
        """Event handler for selecting a module."""
        self.selected_module_id = module_id
    
    @rx.event
    def select_task(self, task_id: str, task_text: str):
        """Event handler for selecting a task."""
        self.selected_task_id = int(task_id)
        self.current_task = {"id": task_id, "text": task_text}
        return rx.redirect(f"/task/{task_id}")

    @rx.event
    def logout(self):
        """Event handler for logout."""
        self.reset_state()
        return rx.redirect("/login")

def task_list(module: MainState.ModuleType):
    """Render list of tasks for a module."""
    return rx.vstack(
        rx.foreach(
            module.tasks,
            lambda task: rx.button(
                f"Задание {task['id']}: {task['text']}",
                on_click=lambda t=task: MainState.select_task(t["id"], t["text"]),
                width="100%",
                padding="10px",
                background=BUTTON_BACKGROUND,
                color="white",
                border_radius="10px",
                _hover={
                    "background": INPUT_BACKGROUND,
                    "color": "white",
                },
            )
        ),
        spacing="2",
    )

def module_section():
    """Render module section with expandable task lists."""
    return rx.vstack(
        rx.heading("Модули", size="1"),
        rx.cond(
            MainState.has_modules,
            rx.foreach(
                MainState.modules,
                lambda module: rx.box(
                    rx.button(
                        module.name,
                        on_click=lambda m=module: MainState.select_module(m.id),
                        width="100%",
                        padding="15px",
                        background=BLOCK_BACKGROUND,
                        color="white",
                        border_radius="10px",
                        _hover={
                            "background": INPUT_BACKGROUND,
                            "color": "white",
                        },
                    ),
                    rx.cond(
                        MainState.selected_module_id == module.id,
                        task_list(module),
                        rx.box()
                    )
                )
            ),
            rx.text("Загрузка модулей...", color="gray.500")
        ),
        width="100%",
    )

def header():
    """Render page header with navigation."""
    return rx.hstack(
        rx.hstack(
            rx.image(src="/logo.png", width="3em", height="3em"),
            rx.heading("Pro IT", size="1"),
            spacing="4",
        ),
        rx.spacer(),
        rx.hstack(
            rx.text(MainState.student_name, font_size="1"),
            rx.button(
                "Выйти",
                on_click=MainState.logout,
                color_scheme="red",
                variant="ghost",
            ),
            spacing="4",
        ),
        width="100%",
        padding="4",
        border_bottom="1px solid",
        border_color="gray.200",
    )

def main():
    """Main page layout."""
    return rx.box(
        rx.vstack(
            header(),
            rx.hstack(
                rx.vstack(
                    rx.heading("КУРС", size="1"),
                    rx.heading(MainState.course_name, size="2"),
                    module_section(),
                    width="100%",
                    max_width="800px",
                    spacing="6",
                    padding="6",
                ),
                width="100%",
                justify="center",
            ),
            width="100%",
            min_height="100vh",
            spacing="0",
        ),
        background=BACKGROUND,
        color="white",
        on_mount=MainState.on_load,
    )