'''
This file was created to work with verification from google authenticator
It takes the data from the input field in the verify.py file and passes the numbers to the given file 
if everything is correct, it lets you into the admin panel
if not, it throws an error
'''

import reflex as rx
import pyotp
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from ..database.models import Personal, engine

load_dotenv()

SECRET_KEY = os.getenv("GOOGLE_SECRET_AUTHENTIFICATOR_KEY")

def verify_code(user_code):
    """Проверка кода Google Authenticator."""
    totp = pyotp.TOTP(SECRET_KEY)
    return totp.verify(user_code)

class AuthState(rx.State):
    code: str = ""  # Google Authenticator
    login: str = "" # Login
    error: str = ""  
    show_login_field: bool = False  #? Show Login field
    is_verified: bool = False  #? If user Verified = True and can go to admin panel
    current_user_name: str = ""  # User name
    current_user_role: str = ""  # Role user

    def set_code(self, code: str):
        """Установить код."""
        self.code = code

    def set_login(self, login: str):
        """Установить логин."""
        self.login = login

    def verify_code(self):
        """Check code Google Authenticator."""
        if verify_code(self.code):
            self.show_login_field = True  # Показываем поле для ввода логина
        else:
            return rx.toast.error("Неверный код. Попробуйте снова.")

    def verify_login(self):
        """Check Login status."""
        if not self.login:
            return rx.toast.error("Введите логин")

        with Session(engine) as session:
            user = session.exec(
                select(Personal).where(Personal.login == self.login)
            ).first()

            if not user:
                return rx.toast.error("Пользователь не найден")

            #* save user data in LocalStorage
            self.current_user_name = user.full_name
            self.current_user_role = user.role
            self.is_verified = True
            return rx.redirect("/admin")

    def logout(self):
        """Выйти из системы."""
        self.is_verified = False
        self.show_login_field = False
        self.code = ""
        self.login = ""
        self.current_user_name = ""
        self.current_user_role = ""
        self.error = ""
        return rx.redirect("/login")