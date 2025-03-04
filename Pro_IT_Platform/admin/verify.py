# import reflex as rx
# from .state import AuthState
# from ..ui.colors import *

# def auth_form():
#     return rx.center(
#         rx.vstack(
#             rx.text("Вход в админ панель", size="6", weight="bold", text_align="center", color="white"),
#             rx.cond(
#                 ~AuthState.show_login_field,
#                 rx.vstack(
#                     rx.input(
#                         placeholder="6-значный код",
#                         value=AuthState.code,
#                         on_change=AuthState.set_code,
#                         style=input_style,
#                     ),
#                     rx.button(
#                         "Проверить код",
#                         on_click=AuthState.verify_code,
#                         width="300px",
#                         background=BLOCK_BACKGROUND,
#                         transition="0.3s",
#                         _hover={"background": BORDER_INPUT}
#                     ),
#                 ),
#                 rx.vstack(
#                     rx.input(
#                         placeholder="Логин",
#                         value=AuthState.login,
#                         on_change=AuthState.set_login,
#                         style=input_style,
#                     ),
#                     rx.button(
#                         "Войти",
#                         on_click=AuthState.verify_login,
#                         width="300px",
#                         background=BLOCK_BACKGROUND,
#                         transition="0.3s",
#                         _hover={"background": BORDER_INPUT}
#                     ),
#                 ),
#             ),
#             width="100%",
#         ),
#         height="100vh",
#         width="100%",
#     )