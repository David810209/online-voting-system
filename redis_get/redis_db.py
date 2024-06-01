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
            "president_private_key":"",
            "vice_president_private_key":""
        })
        
    def get_user_name(self,user_id):
        return self.rds.hget(f'voter:{user_id}','user_name')

    def get_user_id(self,user_id):
        return self.rds.hget(f'voter:{user_id}','user_id')
    
    def get_private_key(self,user_id):
        return self.rds.hget(f'voter:{user_id}','private_key')
    
    def user_exists(self, user_id):
        return self.rds.exists(f'voter:{user_id}')
    
    def update_private_key(self, user_id, president_choice, vice_president_choice):
        self.rds.hmset(f'voter:{user_id}', {
            'president_private_key': president_choice,
            'vice_president_private_key': vice_president_choice
        })
        
   
