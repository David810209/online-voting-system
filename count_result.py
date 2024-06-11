import os
import base64
from dotenv import load_dotenv
from redis_get.redis_db import RedisHandler
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

load_dotenv()
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
RSA_PRIVATE_KEY = os.getenv('RSA_PRIVATE_KEY')

redis_handler = RedisHandler(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

voters = redis_handler.get_all_voters()

results = []
president_votes = {}
vice_president_votes = {}
 
def load_private_key(filepath):
    with open(filepath, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
        )
    return private_key

def decrypt_data(private_key, ciphertext):
    decrypted_data = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data

private_key = load_private_key("private_key.pem")

for voter_key in voters:
    user_id = voter_key.split(':')[1]
    details = redis_handler.get_voter_details(user_id)
    username = details.get('user_name')
    president_ciphertext = details.get("president")
    vice_president_ciphertext = details.get("vice_president")

    print(f"Encoded president ciphertext: {president_ciphertext}")
    print(f"Encoded vice_president ciphertext: {vice_president_ciphertext}")

    try:
        if president_ciphertext:
            ciphertext = base64.b64decode(president_ciphertext)
            print(f"Decoded president ciphertext: {ciphertext}")
            president_choice = decrypt_data(private_key, ciphertext).decode('utf-8')
        else:
            president_choice = None

        if vice_president_ciphertext:
            ciphertext_2 = base64.b64decode(vice_president_ciphertext)
            print(f"Decoded vice_president ciphertext: {ciphertext_2}")
            vice_president_choice = decrypt_data(private_key, ciphertext_2).decode('utf-8')
        else:
            vice_president_choice = None

        results.append({
            'username': username,
            'userid': user_id,
            'president': president_choice,
            'vice_president': vice_president_choice
        })

        if president_choice:
            president_votes[president_choice] = president_votes.get(president_choice, 0) + 1

        if vice_president_choice:
            vice_president_votes[vice_president_choice] = vice_president_votes.get(vice_president_choice, 0) + 1
    except Exception as e:
        print(f"Error processing voter {user_id}: {e}")

print("投票結果:")
for result in results:
    print(f"Username: {result['username']}, UserID: {result['userid']}, President Choice: {result['president']}, Vice President Choice: {result['vice_president']}")

print("\n會長選票結果:")
for candidate, votes in president_votes.items():
    print(f"{candidate}: {votes} 票")

print("\n副會長選票結果:")
for candidate, votes in vice_president_votes.items():
    print(f"{candidate}: {votes} 票")
