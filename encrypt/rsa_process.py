from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class RsaHandler:
    def __init__(self):
        with open("encrypt/public_key.pem", "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(key_file.read())

    # 加密函數
    def encrypt_data(self, data):
        encrypted_data = self.public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_data).decode('utf-8')
