import reflex as rx
from ..pages.main import State

def task_detail():
    """Страница с подробным описанием задания."""
    return rx.vstack(
        rx.heading(f"Задание: {State.selected_task}", font_size="2em"),
        rx.text("Здесь будет подробное описание задания...", font_size="1.2em"),
        rx.button("Назад", on_click=rx.redirect("/")),  # Кнопка для возврата на главную страницу
        padding="20px",
    )