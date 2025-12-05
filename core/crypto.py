# core/crypto.py
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet


class SecurityManager:
    def __init__(self, key_file="my_private_key.pem"):
        self.key_file = key_file
        self.private_key = None
        self.public_key = None
        self.load_or_generate_keys()

    def load_or_generate_keys(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                self.private_key = serialization.load_pem_private_key(
                    f.read(), password=None
                )
        else:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=2048
            )
            with open(self.key_file, "wb") as f:
                f.write(self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                ))
        self.public_key = self.private_key.public_key()

    def get_public_key_pem(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')

    @staticmethod
    def load_public_key_from_pem(pem_str):
        return serialization.load_pem_public_key(pem_str.encode('utf-8'))

    def encrypt_hybrid(self, message: str, recipient_pub_key_pem: str) -> dict:
        """Гибридное шифрование (AES + RSA)"""
        # 1. Генерируем сессионный ключ AES
        session_key = Fernet.generate_key()
        cipher_suite = Fernet(session_key)

        # 2. Шифруем само сообщение
        encrypted_text = cipher_suite.encrypt(message.encode('utf-8'))

        # 3. Шифруем сессионный ключ публичным ключом получателя
        recipient_key = self.load_public_key_from_pem(recipient_pub_key_pem)
        encrypted_session_key = recipient_key.encrypt(
            session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return {
            "enc_session_key": base64.b64encode(encrypted_session_key).decode('utf-8'),
            "ciphertext": base64.b64encode(encrypted_text).decode('utf-8')
        }

    def decrypt_hybrid(self, package: dict) -> str:
        """Расшифровка входящего пакета"""
        enc_session_key = base64.b64decode(package["enc_session_key"])
        ciphertext = base64.b64decode(package["ciphertext"])

        # 1. Достаем сессионный ключ своим приватным ключом
        session_key = self.private_key.decrypt(
            enc_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # 2. Расшифровываем текст
        cipher_suite = Fernet(session_key)
        return cipher_suite.decrypt(ciphertext).decode('utf-8')