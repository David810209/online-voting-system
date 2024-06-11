import os
import pandas as pd
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

excel_file = "student_id.xlsx"  
df = pd.read_excel(excel_file, engine='openpyxl')


name_column = df.columns[0]  
id_column = df.columns[1]    


output_dir = "students_keys"
os.makedirs(output_dir, exist_ok=True)

for index, row in df.iterrows():
    name = row[name_column]
    student_id = str(row[id_column])
    
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
   
    public_key = private_key.public_key()
    
    
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    
    private_key_file = os.path.join(output_dir, f"{student_id}_private.pem")
    public_key_file = os.path.join(output_dir, f"{student_id}_public.pem")
    
    
    with open(private_key_file, "wb") as f:
        f.write(private_key_pem)
    
    
    with open(public_key_file, "wb") as f:
        f.write(public_key_pem)
    
    print(f"student: {name} (id: {student_id}) generate keys：")
    print(f"private_key：{private_key_file}")
    print(f"public_key：{public_key_file}\n")

print("finish")
