import base64
from cryptography.fernet import Fernet
from app.core.config import settings


class SecretStore:
    def __init__(self, key: str = settings.VFSMAX_ENCRYPTION_KEY):
        """AES-256 Fernet encryption for credentials at rest."""
        # Fernet expects a 32-byte base64 encoded string
        # To generate/mock a 32-byte key: base64.urlsafe_b64encode(os.urandom(32))
        try:
            self.cipher_suite = Fernet(key.encode())
        except ValueError:
            # Fallback for dev if key is not correctly formatted
            mock_key = base64.urlsafe_b64encode(b"0"*32)
            self.cipher_suite = Fernet(mock_key)

    def encrypt(self, plaintext: str) -> str:
        """Encrypts a string to an AES-256 cipher string."""
        if not plaintext:
            return ""
        return self.cipher_suite.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Decrypts an AES-256 cipher string to plaintext."""
        if not ciphertext:
            return ""
        try:
            return self.cipher_suite.decrypt(ciphertext.encode()).decode()
        except Exception:
            return "DECRYPTION_FAILED"


def get_secret_store():
    return SecretStore()


# JWT logic using python-jose
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt
