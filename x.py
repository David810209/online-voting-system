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
r = redis.Redis(host='redis-16879.c262.us-east-1-3.ec2.redns.redis-cloud.com',
                               port=16879,
                               password='4crnkgIpt4RRKXZ0nP2WBJp8LUnycrBz',
                            decode_responses=True)
# 使用模式匹配找到所有 voter: 鍵
cursor = 0
while True:
    cursor, keys = r.scan(cursor=cursor, match='voter:*')
    for voter_key in keys:
        # 獲取哈希字段中的時間戳
        timestamp = r.hget(voter_key, 'timestamp')
        
        # 打印結果
        if timestamp:
            print(f'Key: {voter_key}, Timestamp: {timestamp}')
        else:
            print(f'Key: {voter_key}, Timestamp: Not found')

    # 當 cursor 為 0 時退出循環
    if cursor == 0:
        break