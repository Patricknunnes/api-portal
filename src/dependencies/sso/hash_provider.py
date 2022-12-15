import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

from src.settings.settings import BASE_DIR

load_dotenv(os.path.join(BASE_DIR, '../../.env'))

fernet = Fernet(os.getenv("SSO_SECRET"))


def get_password_hash(password):
    return fernet.encrypt(password.encode()).decode()


def verify_password(plain_password, hashed_password):
    decode = decode_password(hashed_password)
    return decode == plain_password


def decode_password(hashed_password):
    return fernet.decrypt(hashed_password.encode()).decode()
