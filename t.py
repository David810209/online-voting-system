# import redis

# import os
# from dotenv import load_dotenv
# load_dotenv()
# REDIS_HOST = os.getenv('REDIS_HOST')
# REDIS_PORT = int(os.getenv('REDIS_PORT'))  
# REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# rds = redis.Redis(host=REDIS_HOST,
#                                port = REDIS_PORT,
#                                password=REDIS_PASSWORD,
#                             decode_responses=True)

# dell = rds.keys('leaderboard:*')
# if dell:
#     rds.delete(*dell)
import redis
import time

import os
from dotenv import load_dotenv
load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))  
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

r = redis.Redis(host=REDIS_HOST,
                               port = REDIS_PORT,
                               password=REDIS_PASSWORD,
                            decode_responses=True)

# 使用模式匹配找到所有 voter: 鍵
voter_keys = r.keys('voter:*')

# 遍歷每個 voter: 鍵並取得其哈希字段和值
for voter_key in voter_keys:
    # 獲取哈希字段和值
    voter_data = r.hgetall(voter_key)
    
    # 打印結果
    print(f'Key: {voter_key.decode("utf-8")}')
    for field, value in voter_data.items():
        print(f'  {field.decode("utf-8")}: {value.decode("utf-8")}')