import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..scr.loc_file_scr import app_data

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=app_data['salt'].encode(),
    iterations=100000,
    backend=default_backend()
)

key = base64.urlsafe_b64encode(kdf.derive(app_data['key'].encode()))
f1 = Fernet(key)


# encryption
def encrypter(value: str):
    return f1.encrypt(value.encode()).decode()


# decryption
def decrypter(value: str):
    return f1.decrypt(value.encode()).decode()
