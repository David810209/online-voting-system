from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from dotenv import load_dotenv
import base64
import os
load_dotenv()

RSA_PUBLIC_EXPONENT = int(os.getenv('RSA_PUBLIC_EXPONENT'))
RSA_KEY_SIZE = int(os.getenv('RSA_KEY_SIZE'))

def generate_rsa_key_pair():
    # 生成 RSA 密钥对
    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE
    )
    public_key = private_key.public_key()

    # 序列化公钥和私钥
    with open("private_key.pem", "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
             )
        )
        
    with open("public_key.pem", "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

# 加密函數
def encrypt_data(public_key, data):
    encrypted_data = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_data).decode('utf-8')

def load_private_key(filepath):
    with open(filepath, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def load_public_key(filepath):
    with open(filepath, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read()
        )
    return public_key
    
def decrypt_data(private_key, ciphertext):
    if not isinstance(ciphertext, bytes):
        raise TypeError("Ciphertext must be bytes.")
    
    try:
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

def main():
    # public_key,private_key,public_key_pem, private_key_pem = generate_rsa_key_pair()
    public_key = load_public_key("encrypt/public_key.pem")
    private_key = load_private_key("private_key.pem")
    print(public_key)
    print(private_key)
    # print(public_key_pem)
    # print(private_key_pem)
    encrypted_data = encrypt_data(public_key, "0.邱禹峰")
    print(encrypted_data,'\n\n')
    decrypted_data = decrypt_data(private_key, base64.b64decode(encrypted_data))
    print(decrypted_data.decode('utf-8'))   

if __name__ == '__main__':
    main()