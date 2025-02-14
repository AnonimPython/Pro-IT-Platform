import reflex as rx
from ..ui.colors import *


#! TEST DATA
# Data structure for modules and their tasks 
MODULES = [
    {"id": 1, "name": "Структура", "tasks": ["Задание 1", "Задание 2", "Задание 3"]},
    {"id": 2, "name": "База", "tasks": ["Задание 1", "Задание 2"]},
    {"id": 3, "name": "Учеба", "tasks": ["Задание 1", "Задание 2", "Задание 3", "Задание 4"]},
    {"id": 4, "name": "Перекус", "tasks": ["Задание 1"]},
    {"id": 5, "name": "Выпивка", "tasks": ["Задание 1", "Задание 2"]},
]

class State(rx.State):
    # State variable to track the currently selected module
    selected_module: int = 1

    # State variable to track the currently selected task
    selected_task: str = ""

    def select_module(self, module: int):
        """Handler for selecting a module."""
        self.selected_module = module

    def select_task(self, task: str):
        """Handler for selecting a task. Redirects to the task detail page."""
        self.selected_task = task
        #* Redirect to the task detail page| take № of module and № of task
        return rx.redirect(f"/task/{task}")


def task_circles(tasks):
    """Component to display task circles (buttons) for a given list of tasks."""
    return rx.hstack(
        *[
            rx.box(
                rx.button(
                    rx.text(task),  #* Display the task name
                    on_click=lambda task=task: State.select_task(task),  #* Handle task selection
                    **TASK_CIRCLE_STYLE,  #circle style
                ),
            )
            for task in tasks  #* Loop through each task in the list
        ],
        flex_wrap="wrap", 
    )

def module_buttons():
    """Component to display buttons for selecting modules."""
    return rx.vstack(
        *[
            rx.button(
                f"{module['id']}-{module['name']}",  # Display module ID and name
                on_click=lambda module_id=module["id"]: State.select_module(module_id),  # Handle module selection
                margin_top="20px",  # Add margin between buttons
            )
            #* we using for bucause we need to create 5 moduls. It's simple way to create this thing
            for module in MODULES 
        ],
    )

def selected_module_content():
    """Component to display the content of the selected module."""
    return rx.vstack(
        rx.cond(
            # Check if the selected module is 1
            State.selected_module == 1,
            rx.vstack(
                rx.text("Модуль 1 выбран - Структура", font_size="30px"),  # Display module name
                task_circles(MODULES[0]["tasks"]),  # Display tasks for module 1
            ),
            rx.cond(
                # Check if the selected module is 2
                State.selected_module == 2,
                rx.vstack(
                    rx.text("Модуль 2 выбран - База", font_size="30px"),  # Display module name
                    task_circles(MODULES[1]["tasks"]),  # Display tasks for module 2
                ),
                rx.cond(
                    # Check if the selected module is 3
                    State.selected_module == 3,
                    rx.vstack(
                        rx.text("Модуль 3 выбран - Учеба", font_size="30px"),  # Display module name
                        task_circles(MODULES[2]["tasks"]),  # Display tasks for module 3
                    ),
                    rx.cond(
                        # Check if the selected module is 4
                        State.selected_module == 4,
                        rx.vstack(
                            rx.text("Модуль 4 выбран - Перекус", font_size="30px"),  # Display module name
                            task_circles(MODULES[3]["tasks"]),  # Display tasks for module 4
                        ),
                        rx.vstack(
                            # Default case: module 5
                            rx.text("Модуль 5 выбран - Выпивка", font_size="30px"),  # Display module name
                            task_circles(MODULES[4]["tasks"]),  # Display tasks for module 5
                        ),
                    ),
                ),
            ),
        ),
    )

def main():
    """Main component representing the entire page."""
    return rx.vstack(
        # Header section
        rx.box(
            rx.flex(
                #* logo and title
                rx.hstack(
                    rx.image("/logo.png", width="3em", border_radius="10px"),
                    rx.heading("Pro IT", font_size="2em"),  
                    align="center", 
                ),
                #* username
                rx.box(
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button(
                                rx.text("Никита Сидоров", font_size="30px", color="white"), 
                                variant="soft",  
                                height="auto",  
                                background_color=GRAY_LAVANDER, 
                            ),
                        ),
                        rx.menu.content(
                            rx.menu.item(
                                "Выход", 
                                color="red",  
                                _hover={"background_color": "#ff00001a"},  
                            ),
                            width="100%",  
                        ),
                    ),
                ),
                justify="between",  
                align="center",
            ),
            width="100%", 
        ),

       
        rx.separator(size="4", background=SEPARATOR_COLOR, margin_top="20px"),

        #* main content
        rx.hstack(
            #* left side
            rx.box(
                rx.text("КУРС", font_size="30px"),
                rx.heading("Scratch", font_size="45px"),
                rx.box(
                    rx.text("Модули", font_size="30px"),
                    module_buttons(),  #* Display module buttons
                    margin_top="50px",
                ),
                width="15%", 
            ),

            rx.divider(orientation="vertical", size="4", height="700px", background=SEPARATOR_COLOR),
            #* right side
            rx.box(
                selected_module_content(),  # Display content for the selected module
                width="70%",
            ),
            spacing="4", 
            width="100%",
            height="10vh",
        ),
        padding="20px", 
        color="white", 
        width="100%",
    )