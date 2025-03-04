import reflex as rx


def info_card(title: str="N/A", count: int=0, gradient: str="linear-gradient(45deg, var(--red-9), var(--pink-9))"):
    return rx.box(
        rx.vstack(
            rx.text(title, font_size="20px", color="white", weight="bold"),
            rx.text(str(count), font_size="30px", color="white", weight="bold"),
            align="center",
            justify="center",
        ),
        background=gradient,  # Градиентный фон
        border_radius="15px",
        padding=["1em", "1.5em", "2em"],
        style={
            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
        },
        _hover={
            "transform": "scale(1.02)",
            "transition": "all 0.3s ease-out",
        },
        # margin="1em",
        width=["90%", "70%", "50%", "20%"],  # Адаптивная ширина
    )