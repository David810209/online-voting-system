import redis
import os
from pathlib import Path
from dotenv import load_dotenv
from redis_get.redis_db import RedisHandler
import pandas as pd
load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
RSA_PRIVATE_KEY = os.getenv('RSA_PRIVATE_KEY')

redis_handler = RedisHandler(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

excel_file = "student_id.xlsx"  
df = pd.read_excel(excel_file, engine='openpyxl')
id_column = df.columns[1]    


def read_keys(user_id, directory):
    # 構建文件路徑
    public_key_path = Path(directory) / f"{user_id}_public.pem"
    private_key_path = Path(directory) / f"{user_id}_private.pem"

    # 讀取公鑰
    public_key = ""
    if public_key_path.exists():
        with open(public_key_path, 'r') as file:
            public_key = file.read()

    # 讀取私鑰
    private_key = ""
    if private_key_path.exists():
        with open(private_key_path, 'r') as file:
            private_key = file.read()

    return public_key, private_key

for index, row in df.iterrows():
    user_id = str(row[id_column])
    public_key, private_key = read_keys(user_id, "students_keys")
    redis_handler.set_key(user_id, public_key, private_key)
    print(f"student: {user_id} keys updated")