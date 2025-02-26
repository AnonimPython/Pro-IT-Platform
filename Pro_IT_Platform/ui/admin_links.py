import reflex as rx
from ..ui.colors import *


import reflex as rx

#* Links
#? Need to make simple add liks to admin pannel. Like a Django
nav_items = [
    {"icon": "grid-2x2", "text": "Главная", "href": "/admin"},
    {"icon": "users", "text": "Ученики", "href": "/admin/students"},
    {"icon": "boxes", "text": "Группы", "href": "/admin/groups"},
    {"icon": "presentation", "text": "Курсы", "href": "/admin/courses"},
    {"icon": "person-standing", "text": "Персонал", "href": "/admin/personal"},
    {"icon": "archive-restore", "text": "Рассылки", "href": "/admin/mailing"}, #! make
]

def nav_link(item: dict):
    return rx.box(
        rx.link(
            rx.hstack(
                rx.icon(tag=item["icon"], color="white"),
                rx.text(item["text"], color="white", weight="bold", font_size="20px"),
                align="center",
            ),
            href=item["href"],
        ),
        padding="5px",
        width="100%",
        transition="0.3s",
        border_radius="5px",
        _hover={"background": "rgba(255, 255, 255, 0.1)"},
    )


def admin_links() -> rx.Component:
    return rx.vstack(
        rx.foreach(nav_items, nav_link),
        spacing="2",
    )