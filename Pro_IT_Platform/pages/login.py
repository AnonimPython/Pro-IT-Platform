import reflex as rx


class LoginInputState(rx.State):
    form_data: dict = {}

    @rx.event
    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        print("Form data:", self.form_data)

def main():
    return rx.vstack(
        rx.heading("Login Form"),
            rx.form.root(
                rx.hstack(
                    rx.input(
                        name="input",
                        placeholder="Enter text...",
                        type="text",
                        required=True,
                    ),
                    rx.button("Submit", type="submit"),
                    width="100%",
                ),
                on_submit=LoginInputState.handle_submit,
                reset_on_submit=True,
            ),
        
        rx.button("Click me!", color_scheme="blue"),
    )