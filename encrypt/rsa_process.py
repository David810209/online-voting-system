from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64


def encrypt_data(data,public_key_pem):
    public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8')
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

def decrypt_data(ciphertext, private_key_pem):
    if not isinstance(ciphertext, bytes):
        raise TypeError("Ciphertext must be bytes.")
    
    try:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
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
        return decrypted_data.decode('utf-8')
    except ValueError as e:
        print(f"Error decrypting data: {e}")
        return None 
    except Exception as e:
        print(f"Unexpected error during decryption: {e}")
        return None

