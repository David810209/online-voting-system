from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64


def encrypt_data(data,public_key):
    public_key = serialization.load_pem_public_key(
            public_key
        )
    encrypted_data = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_data(ciphertext,private_key):
    
    if not isinstance(ciphertext, bytes):
        raise TypeError("Ciphertext must be bytes.")
    
    try:
        private_key = serialization.load_pem_private_key(
            private_key,
            password=None,
        )
        decrypted_data = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data
    except ValueError as e:
        print(f"Error decrypting data: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during decryption: {e}")
        raise

def load_private_key(key_pem):
    private_key = serialization.load_pem_private_key(
        key_pem,
        password=None,
    )
    return private_key

def load_public_key(key_pem):
    public_key = serialization.load_pem_public_key(
            key_pem
        )
    return public_key