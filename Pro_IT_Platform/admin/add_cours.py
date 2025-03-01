from typing import List, Optional
import reflex as rx
from sqlmodel import Session, select
from ..database.models import Courses, Module, Task, engine
from ..ui.colors import *
from ..ui.admin_pannel import admin_pannel
from ..ui.cours_card import cours_card

# Состояние для управления курсами, модулями и заданиями
class CourseState(rx.State):
    """State для управления курсами, модулями и заданиями."""
    courses: List[Courses] = []  # Список всех курсов
    current_course: Optional[Courses] = None  # Текущий выбранный курс
    modules: List[Module] = []  # Модули текущего курса
    tasks: List[Task] = []  # Задания текущего модуля
    new_task_text: str = ""  # Текст нового задания
    current_course_id: Optional[int] = None  # ID текущего курса
    current_module_id: Optional[int] = None  # ID текущего модуля
    new_course_name: str = ""  # Название нового курса

    async def load_courses(self):
        """Загрузить все курсы из базы данных."""
        with Session(engine) as session:
            self.courses = session.exec(select(Courses)).all()

    async def load_course(self):
        """Загрузить выбранный курс и его модули."""
        if self.current_course_id is None:
            return
        with Session(engine) as session:
            self.current_course = session.get(Courses, self.current_course_id)
            if self.current_course:
                self.modules = session.exec(
                    select(Module).where(Module.course_id == self.current_course_id)
                ).all()

    async def load_tasks(self, module_id: int):
        """Загрузить задания для выбранного модуля."""
        self.current_module_id = module_id  # Устанавливаем текущий модуль
        with Session(engine) as session:
            self.tasks = session.exec(
                select(Task).where(Task.module_id == module_id)
            ).all()

    async def add_task(self, module_id: int):
        """Добавить задание в модуль."""
        if not self.new_task_text:
            return rx.toast.warning("Введите текст задания")

        with Session(engine) as session:
            task = Task(
                text=self.new_task_text,
                module_id=module_id,
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            self.new_task_text = ""  # Очищаем поле ввода
            await self.load_tasks(module_id)  # Перезагружаем задачи для текущего модуля
            return rx.toast.success("Задание успешно добавлено")

    async def add_course(self):
        """Добавить новый курс и 5 модулей."""
        if not self.new_course_name:
            return rx.toast.warning("Введите название курса")

        with Session(engine) as session:
            # Создаем курс
            course = Courses(
                name=self.new_course_name,
                link="",  # Пока оставляем пустым, можно добавить поле для ссылки
            )
            session.add(course)
            session.commit()
            session.refresh(course)

            # Создаем 5 модулей для курса
            for i in range(1, 6):
                module = Module(
                    name=f"Модуль {i}",
                    course_id=course.id,
                )
                session.add(module)
            session.commit()

            self.new_course_name = ""  # Сбрасываем поле ввода
            await self.load_courses()  # Перезагружаем список курсов
            return rx.toast.success("Курс и модули успешно добавлены")

    async def set_course_id_from_route(self):
        """Извлечь course_id из URL и загрузить курс."""
        self.current_course_id = int(self.router.page.params.get("course_id", 0))
        await self.load_course()

# Диалоговое окно для добавления нового курса
def add_course_dialog() -> rx.Component:
    """Диалоговое окно для добавления нового курса."""
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Добавить курс",
                # background_color=LINK_BACKGROUND_COLOR,
                # border=f"1px solid {ADMIN_YELLOW}",
            )
        ),
        rx.dialog.content(
            rx.dialog.title("Добавить новый курс"),
            rx.dialog.description("Введите название курса"),
            rx.input(
                placeholder="Название курса",
                value=CourseState.new_course_name,
                on_change=CourseState.set_new_course_name,
                required=True,
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button("Отмена", variant="soft", color_scheme="gray"),
                ),
                rx.dialog.close(
                    rx.button(
                        "Сохранить",
                        on_click=CourseState.add_course,  # Используем метод add_course
                    ),
                ),
                spacing="3",
                justify="end",
            ),
        ),
    )

#* list of all courses
def courses_list() -> rx.Component:
    """Список всех курсов."""
    return rx.box(
        rx.hstack(
            admin_pannel(),
            rx.vstack(
                rx.box(
                    rx.hstack(
                        rx.text("Все курсы", font_size="20px"),
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
                        rx.hstack(
                            add_course_dialog(),
                            spacing="4",
                            align="center",
                        ),
                        rx.grid(
                            rx.foreach(
                                CourseState.courses,
                                lambda course: rx.link(
                                    rx.box(
                                        cours_card(course.name),
                                    ),
                                    href=f"/admin/courses/{course.id}",
                                ),
                            ),
                            gap="1rem",
                            columns="3",
                            margin_top="50px",
                            grid_template_columns=[
                                "1fr",
                                "repeat(2, 1fr)",
                                "repeat(2, 1fr)", 
                                "repeat(3, 1fr)",
                                "repeat(3, 1fr)",
                            ],
                            width="100%",
                        ),
                        spacing="4",
                        padding="20px",
                    ),
                    on_mount=CourseState.load_courses,
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
    )
    
# Страница курса с модулями и заданиями
def course_page() -> rx.Component:
    """Страница курса с модулями и заданиями."""
    return rx.box(
        rx.vstack(
            rx.cond(
                CourseState.current_course,
                rx.vstack(
                    rx.text(f"Курс: {CourseState.current_course.name}", font_size="24px", weight="bold"),
                    rx.divider(),
                    rx.foreach(
                        CourseState.modules,
                        lambda module: rx.vstack(
                            rx.hstack(
                                rx.text(f"Модуль {module.id}: {module.name}", font_size="20px"),
                                rx.spacer(),
                                rx.dialog.root(
                                    rx.dialog.trigger(
                                        rx.button("Добавить задание", size="1"),
                                    ),
                                    rx.dialog.content(
                                        rx.dialog.title(f"Добавить задание в {module.name}"),
                                        rx.dialog.description("Введите текст задания"),
                                        rx.input(
                                            placeholder="Текст задания",
                                            value=CourseState.new_task_text,
                                            on_change=CourseState.set_new_task_text,
                                        ),
                                        rx.flex(
                                            rx.dialog.close(
                                                rx.button("Отмена", variant="soft", color_scheme="gray"),
                                            ),
                                            rx.dialog.close(
                                                rx.button(
                                                    "Сохранить",
                                                    on_click=lambda: CourseState.add_task(module.id),
                                                ),
                                            ),
                                            spacing="3",
                                            justify="end",
                                        ),
                                    ),
                                ),
                                spacing="4",
                            ),
                            rx.cond(
                                CourseState.current_module_id == module.id,
                                rx.foreach(
                                    CourseState.tasks,
                                    lambda task: rx.text(f"Задание {task.id}: {task.text}", font_size="16px"),
                                ),
                            ),
                            spacing="2",
                            padding="10px",
                            border_radius="5px",
                            background_color=ADMIN_MAIN_CONTENT,
                        ),
                    ),
                    spacing="4",
                    padding="20px",
                ),
                rx.text("Курс не найден", font_size="20px"),
            ),
        ),
        on_mount=CourseState.set_course_id_from_route,
    )