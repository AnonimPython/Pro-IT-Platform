import reflex as rx
from ..ui.colors import *


#! TEST DATA
MODULES = [
    {
        "id": 1,
        "name": "Структура",
        "tasks": [
            {"id": 1, "text": "Изучите структуру проекта."},
            {"id": 2, "text": "Создайте новую ветку в Git."},
            {"id": 3, "text": "Напишите документацию."},
        ],
    },
    {
        "id": 2,
        "name": "База",
        "tasks": [
            {"id": 1, "text": "Настройте базу данных."},
            {"id": 2, "text": "Создайте таблицы."},
        ],
    },
    {
        "id": 3,
        "name": "Учеба",
        "tasks": [
            {"id": 1, "text": "Прочитайте главу 1 учебника."},
            {"id": 2, "text": "Решите задачи из главы 1."},
            {"id": 3, "text": "Подготовьтесь к тесту."},
            {"id": 4, "text": "Напишите конспект."},
        ],
    },
    {
        "id": 4,
        "name": "Перекус",
        "tasks": [
            {"id": 1, "text": "Приготовьте бутерброд."},
        ],
    },
    {
        "id": 5,
        "name": "Выпивка",
        "tasks": [
            {"id": 1, "text": "Купите напитки."},
            {"id": 2, "text": "Разлейте по бокалам."},
        ],
    },
]

class State(rx.State):
    # State variable to track the currently selected module
    selected_module: int = 1

    # State variable to track the currently selected task
    selected_task: str = ""
    selected_description: str = ""

    def select_module(self, module: int):
        """Handler for selecting a module."""
        self.selected_module = module

    def select_task(self, task_number: str, task_description: str):
        """Handler for selecting a task. Redirects to the task detail page."""
        self.selected_task = task_number
        self.selected_description = task_description
        #* Redirect to the task detail page| take № of module and № of task
        return rx.redirect(f"/task/{task_number}")


def task_circles(tasks):
    """Component to display task circles (buttons) for a given list of tasks."""
    return rx.hstack(
        *[
            rx.box(
                rx.button(
                    rx.text(f"Задание {task['id']}"),  #* Display only the task name (e.g., "Задание 1")
                    on_click=lambda task=task: State.select_task(str(task["id"]), task["text"]),  #* Pass task number and full text
                    **TASK_CIRCLE_STYLE,  #circle style
                    _hover={
                        "background": INPUT_BACKGROUND,
                        "color":"white", 
                    },
                    transition="0.2s linear",
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
                # f"{module['id']}-{module['name']}",  # Display module ID and name
                rx.text(f"{module['name']}", font_size="20px",weight="bold"),  # Display module name
                on_click=lambda module_id=module["id"]: State.select_module(module_id),  # Handle module selection
                margin_top="20px",
                background=GRAY_LAVANDER,
                width="100%",
                color=BLOCK_BACKGROUND,
                height="50px",
                padding="10px",
                border_radius="10px",
                _hover={
                        "background": INPUT_BACKGROUND,
                        "color":"white", 
                    },
                transition="0.2s linear",
                
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
                rx.text(MODULES[0]["name"], font_size="30px"),  # Display module name
                task_circles(MODULES[0]["tasks"]),  # Display tasks for module 1
            ),
            rx.cond(
                # Check if the selected module is 2
                State.selected_module == 2,
                rx.vstack(
                    rx.text(MODULES[1]["name"], font_size="30px"),  # Display module name
                    task_circles(MODULES[1]["tasks"]),  # Display tasks for module 2
                ),
                rx.cond(
                    # Check if the selected module is 3
                    State.selected_module == 3,
                    rx.vstack(
                        rx.text(MODULES[2]["name"], font_size="30px"),  # Display module name
                        task_circles(MODULES[2]["tasks"]),  # Display tasks for module 3
                    ),
                    rx.cond(
                        # Check if the selected module is 4
                        State.selected_module == 4,
                        rx.vstack(
                            rx.text(MODULES[3]["name"], font_size="30px"),  # Display module name
                            task_circles(MODULES[3]["tasks"]),  # Display tasks for module 4
                        ),
                        rx.vstack(
                            # Default case: module 5
                            rx.text(MODULES[4]["name"], font_size="30px"),  # Display module name
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
        #* Header section
        rx.box(
            rx.flex(
                #* logo and title
                rx.hstack(
                    rx.image("/logo.png", width="3em", border_radius="10px"),
                    rx.heading("Pro IT", font_size="2em"),  
                    align="center", 
                ),
                #* username | exit button
                rx.box(
                    rx.hstack(
                        rx.text(
                            "Никита Сидоров",
                            font_size="25px", 
                            color="white",
                            height="100%",
                            background_color=GRAY_LAVANDER, 
                            padding="5px",
                            border_radius="10px",
                        ),
                        
                        #* exit button
                        rx.box(
                            rx.link(
                               rx.icon(
                                tag="log-out",
                                color="red",
                            ),
                               href="/login" 
                            ),
                            
                            background="#ff00001a",
                            width="50px", 
                            height="50px",
                            border_radius="10px",
                            display="flex", 
                            justify_content="center",
                            align_items="center",
                            _hover={"background_color": "#a92525"},
                            transition="0.2s linear",
                        ),
                        
                    ),
                    
                ),
                justify="between",  
                align="center",
            ),
            width="100%", 
            align="center",
            align_self="center",
        ),

       
        rx.separator(size="4", background=SEPARATOR_COLOR, margin_top="10px"),

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
        height="100vh",
        background_color=BACKGROUND,
    )