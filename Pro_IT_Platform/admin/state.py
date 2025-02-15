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

load_dotenv()

SECRET_KEY = os.getenv("GOOGLE_SECRET_AUTHENTIFICATOR_KEY")

def verify_code(user_code):
    totp = pyotp.TOTP(SECRET_KEY)
    return totp.verify(user_code)

class AuthState(rx.State):
    code: str = ""
    error: str = ""
    is_verified: bool = False  #* check if the user verified

    def verify_and_redirect(self):
        if verify_code(self.code):
            self.is_verified = True
        else:
            self.error = "Неверный код. Попробуйте снова."
            return rx.toast(self.error)

    def logout(self):
        #* clear the "session"
        self.is_verified = False
        self.code = ""
        self.error = ""