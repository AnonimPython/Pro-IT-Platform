import reflex as rx


def main():
    return rx.vstack(
        rx.heading("Welcome to Pro IT Platform"),
        rx.text("Reflex app"),
        rx.button("Click me!", color_scheme="blue"),
    )