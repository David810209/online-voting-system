import redis
class RedisHandler():
    def __init__(self,host,port,password) :
        self.rds = redis.Redis(host=host,
                               port = port ,
                               password=password,
                            decode_responses=True)
    def set_db(self,user_name,user_id):
        self.rds.hmset(f'voter:{user_id}',{
            "user_name":user_name,
            'user_id':user_id,
            'public_key':"",
            "private_key":"",
            "president":"",
            "vice_president":"",
            "president_text":"",
            "vice_president_text":"",
        })
        
    def get_user_name(self,user_id):
        return self.rds.hget(f'voter:{user_id}','user_name')

    def get_user_id(self,user_id):
        return self.rds.hget(f'voter:{user_id}','user_id')
    
    def get_public_key(self,user_id):
        return self.rds.hget(f'voter:{user_id}','public_key')

    def get_private_key(self,user_id):
        return self.rds.hget(f'voter:{user_id}','private_key')

    def get_president_choice(self,user_id):
        return self.rds.hget(f'voter:{user_id}','president_text')

    def get_vice_president_choice(self,user_id):
        return self.rds.hget(f'voter:{user_id}','vice_president_text')
    
    def store_key(self,user_id,public_key, private_key):
        self.rds.hset(f'voter:{user_id}','public_key',public_key)
        self.rds.hset(f'voter:{user_id}','private_key',private_key)
        
    def user_exists(self, user_id):
        return self.rds.exists(f'voter:{user_id}')
    
    def update_vote(self, user_id, president_choice, vice_president_choice):
        self.rds.hmset(f'voter:{user_id}', {
            'president': president_choice,
            'vice_president': vice_president_choice
        })
    
        
   
