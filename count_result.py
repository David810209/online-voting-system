import os
import base64
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib

# 設定 matplotlib 支持中文
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 'Microsoft YaHei' 是一種常見的中文字體
matplotlib.rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題
from redis_get.redis_db import RedisHandler
from encrypt.rsa_process import  decrypt_data
import streamlit as st
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
            private_key = redis_handler.get_private_key(user_id)
            president_choice = decrypt_data(ciphertext, private_key)
        else:
            president_choice = None

        if vice_president_ciphertext:
            ciphertext_2 = base64.b64decode(vice_president_ciphertext)
            print(f"Decoded vice_president ciphertext: {ciphertext_2}")
            vice_president_choice = decrypt_data(ciphertext_2, private_key)
        else:
            vice_president_choice = None
        if president_choice and vice_president_choice:
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

def plot_votes(data, title, chart_type='bar'):
    fig, ax = plt.subplots()
    candidates = list(data.keys())
    votes = list(data.values())

    if chart_type == 'bar':
        ax.bar(candidates, votes, color='blue')
    elif chart_type == 'pie':
        ax.pie(votes, labels=candidates, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.set_title(title)
    return fig

st.title('投票結果展示')


st.header('會長選票結果')
chart_type = st.radio("選擇圖表類型 (會長):", ('圓餅圖','長條圖'))
president_fig = plot_votes(president_votes, "會長選票", 'bar' if chart_type == '長條圖' else 'pie')
st.pyplot(president_fig)

st.header('副會長選票結果')
chart_type = st.radio("選擇圖表類型 (副會長):", ('圓餅圖','長條圖'))
vice_president_fig = plot_votes(vice_president_votes, "副會長選票", 'bar' if chart_type == '長條圖' else 'pie')
st.pyplot(vice_president_fig)











# print("投票結果:")
# for result in results:
#     print(f"Username: {result['username']}, UserID: {result['userid']}, President Choice: {result['president']}, Vice President Choice: {result['vice_president']}")

# print("\n會長選票結果:")
# for candidate, votes in president_votes.items():
#     print(f"{candidate}: {votes} 票")

# print("\n副會長選票結果:")
# for candidate, votes in vice_president_votes.items():
#     print(f"{candidate}: {votes} 票")
