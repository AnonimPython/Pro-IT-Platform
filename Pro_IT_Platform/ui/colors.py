
#*  COLORS
BACKGROUND = "#676177"
BLOCK_BACKGROUND = SEPARATOR_COLOR = "#2c2638"
BUTTON_BACKGROUND = "#6d54b5"
BORDER_INPUT = GRAY_LAVANDER = "#aba1c4"
INPUT_BACKGROUND = "#39374c"


#*  ADMIN COLORS
ADMIN_BACKGROUND_COLOR = "#5e6873" # remake
ADMIN_MAIN_CONTENT = "#242529"
ADMIN_YELLOW = "#fff37a"
ADMIN_LIGHT_GRAY = "#dcdcdc"
LINK_BACKGROUND_COLOR = "#363538"

#*  STYLES
TASK_CIRCLE_STYLE = {
    "width": "300px",
    "height": "150px",
    "border_radius": "10px",
    "background_color": GRAY_LAVANDER,
    "color": BLOCK_BACKGROUND,
    "font_size": "30px",
    "display": "flex",
    "align_items": "center",
    "justify_content": "center",
    "margin_right": "10px",
}

input_style: dict = {
    "width": "300px",
    "height": "50px",
    "--text-field-focus-color": BORDER_INPUT,
    "background": INPUT_BACKGROUND,
    "color": "white",
    "& input::placeholder": {
        "padding-left":"10px",
        "color": "white"
    },
    "font-size": "20px",
    }

admin_input_style: dict = {
    "width": "200px",
    "height": "50px",
    "border-radius": "10px",
    "border": f"1px solid {ADMIN_YELLOW}",
    "--text-field-focus-color": ADMIN_YELLOW,
    "background": ADMIN_MAIN_CONTENT,
    "color": "white",
    "& input::placeholder": {
        "padding-left":"10px",
        "color": "white"
    },
    "font-size": "20px", 
    "margin": "10px",
}