from cryptography.fernet import Fernet
from django.conf import settings

# settings.py dosyasındaki sabit anahtarı kullan
cipher_suite = Fernet(settings.FERNET_KEY)

def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message
