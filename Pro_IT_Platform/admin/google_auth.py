
#/ I will use a google authentificator in mobile. This will be used for authentication in admin panel
import pyotp

#* .env file
import os
from dotenv import load_dotenv
load_dotenv()


# Создание URI для добавления в Google Authenticator
def generate_google_authenticator_uri(secret_key, email):
    return pyotp.totp.TOTP(secret_key).provisioning_uri(name=email, issuer_name="MyApp")

# Проверка введенного кода
def verify_code(secret_key, user_code):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(user_code)

# Основная функция
def auth_google_authenticator():
    # Генерация секретного ключа
    secret_key = os.getenv('GOOGLE_SECRET_AUTHENTIFICATOR_KEY')
    # print(f"Ваш секретный ключ: {secret_key}")

    # Генерация URI для Google Authenticator
    # email = "user@example.com"
    # google_auth_uri = generate_google_authenticator_uri(secret_key, email)
    # print(f"Добавьте этот URI в Google Authenticator: {google_auth_uri}")

    # Пример: проверка кода
    while True:
        user_code = input("Введите код из Google Authenticator: ")
        if verify_code(secret_key, user_code):
            print("Код верный! Доступ разрешен.")
            break
        else:
            print("Неверный код. Попробуйте снова.")
            
auth_google_authenticator()