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
    code: str = rx.LocalStorage("")  # Храним код в LocalStorage
    login: str = rx.LocalStorage("")  # Храним логин в LocalStorage
    auth_token: str = rx.LocalStorage("")  # Токен авторизации
    error: str = ""
    show_login_field: bool = False
    current_user_name: str = ""
    current_user_role: str = ""

    def verify_code(self):
        """Проверка кода Google Authenticator."""
        if verify_code(self.code):
            self.show_login_field = True
            self.error = ""
        else:
            self.error = "Неверный код"
            return rx.toast.error("Неверный код. Попробуйте снова.")

    def verify_login(self):
        """Проверка логина и установка токена."""
        if not self.login:
            return rx.toast.error("Введите логин")

        with Session(engine) as session:
            user = session.exec(
                select(Personal).where(Personal.login == self.login)
            ).first()

            if user:
                self.auth_token = "authenticated"  # Устанавливаем токен
                self.current_user_name = user.full_name
                self.current_user_role = user.role
                self.error = ""
                return rx.redirect("/admin")  # Перенаправляем на админ-панель
            else:
                self.error = "Неверные учетные данные"
                return rx.toast.error("Пользователь не найден")

    def logout(self):
        """Выход из системы с очисткой storage."""
        self.auth_token = ""
        self.code = ""
        self.login = ""
        self.current_user_name = ""
        self.current_user_role = ""
        self.error = ""
        return rx.redirect("/auth")  # Перенаправляем на страницу авторизации

    def check_auth(self):
        """Проверка авторизации при загрузке страницы."""
        if not self.auth_token:
            return rx.redirect("/auth")  # Перенаправляем на страницу авторизации