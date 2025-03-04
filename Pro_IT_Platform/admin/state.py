import reflex as rx
import pyotp
import os
from dotenv import load_dotenv
from sqlmodel import Session, select
from ..database.models import Personal, engine

# Load environment variables from .env file
load_dotenv()

# Get the secret key for Google Authenticator from environment variables
SECRET_KEY = os.getenv("GOOGLE_SECRET_AUTHENTIFICATOR_KEY")

def verify_code(user_code):
    """Verify the Google Authenticator code."""
    totp = pyotp.TOTP(SECRET_KEY)
    return totp.verify(user_code)

class AuthState(rx.State):
    code: str = rx.LocalStorage("")  # Store the code in LocalStorage
    login: str = rx.LocalStorage("")  # Store the login in LocalStorage
    auth_token: str = rx.LocalStorage("")  # Store the authentication token in LocalStorage
    error: str = ""  # Store error messages
    show_login_field: bool = False  # Control the visibility of the login field
    current_user_name: str = ""  # Store the current user's name
    current_user_role: str = ""  # Store the current user's role

    def verify_code(self):
        """Verify the Google Authenticator code."""
        if verify_code(self.code):
            self.show_login_field = True  # Show the login field if the code is correct
            self.error = ""  # Clear any previous errors
        else:
            self.error = "Invalid code"  # Set an error message
            return rx.toast.error("Invalid code. Please try again.")  # Show an error toast

    def verify_login(self):
        """Verify the login and set the authentication token."""
        if not self.login:
            return rx.toast.error("Please enter your login")  # Show an error if the login is empty

        with Session(engine) as session:
            user = session.exec(
                select(Personal).where(Personal.login == self.login)
            ).first()

            if user:
                self.auth_token = "authenticated"  # Set the authentication token
                self.current_user_name = user.full_name  # Set the current user's name
                self.current_user_role = user.role  # Set the current user's role
                self.error = ""  # Clear any previous errors
                return rx.redirect("/admin")  # Redirect to the admin panel
            else:
                self.error = "Invalid credentials"  # Set an error message
                return rx.toast.error("User not found")  # Show an error toast

    def logout(self):
        """Log out the user and clear the storage."""
        self.auth_token = ""  # Clear the authentication token
        self.code = ""  # Clear the code
        self.login = ""  # Clear the login
        self.current_user_name = ""  # Clear the current user's name
        self.current_user_role = ""  # Clear the current user's role
        self.error = ""  # Clear any errors
        self.show_login_field = False  # Reset the visibility of the login field
        return rx.redirect("/auth")  # Redirect to the authentication page

    def check_auth(self):
        """Check authentication when the page loads."""
        if not self.auth_token:
            return rx.redirect("/auth")  # Redirect to the authentication page if not authenticated