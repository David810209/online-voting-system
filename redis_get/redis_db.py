import redis
class RedisHandler():
    def __init__(self,host,port,password) :
        self.rds = redis.Redis(host=host,
                               port = port ,
                               password=password,
                            decode_responses=True)
    def set_db(self,user_name,user_id):
        self.rds.hmset(f'voters:{user_id}',{
            "user_name":user_name,
            'user_id':user_id
        })
        
    def get_user_name(self,user_id):
        return self.rds.hget(f'voters:{user_id}','user_name')

    def get_user_id(self,user_id):
        return self.rds.hget(f'voters:{user_id}','user_id')

    def get_president_encrypted(self,user_id):
        return self.rds.hget(f'voters:{user_id}','president')
    
    def get_vice_president_encrypted(self,user_id):
        return self.rds.hget(f'voters:{user_id}','vice_president')
    
    def user_exists(self, user_id):
        return self.rds.exists(f'voters:{user_id}')
    
    def key_exists(self, user_id):
        return self.rds.exists(f'keys:{user_id}')
    
    def get_public_key(self, user_id):
        return self.rds.hget(f'keys:{user_id}', 'public_key')
    
    def get_private_key(self, user_id):
        return self.rds.hget(f'keys:{user_id}', 'private_key')
    
        
    def set_key(self, user_id, public_key,private_key):
        self.rds.hmset(f'keys:{user_id}', {
            'user_id': user_id,
            'private_key': private_key,
            'public_key': public_key
        })
    def has_voted(self, user_id):
        return self.rds.hexists(f'voters:{user_id}', 'president')
    
    def update_vote(self, user_id, president_choice, vice_president_choice):
        self.rds.hmset(f'voters:{user_id}', {
            'president': president_choice,
            'vice_president': vice_president_choice
        })
    
    def get_all_voters(self):
        return self.rds.keys('voters:*')
    
    def get_voter_details(self, user_id):
        return self.rds.hgetall(f'voters:{user_id}')
        
   
   
