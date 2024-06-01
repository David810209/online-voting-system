from flask import Flask, render_template, request, redirect, url_for, flash, session, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#from flask_talisman import Talisman
import base64
from redis_get.redis_db import RedisHandler
from encrypt.rsa_process import load_private_key, decrypt_data, encrypt_data,generate_rsa_key_pair
from config import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD, FLASK_SECRET_KEY

app = Flask(__name__)
#Talisman(app)
redis_handler = RedisHandler(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "300 per hour"]
)

app.secret_key = FLASK_SECRET_KEY  # 用於會話加密，請更換為更安全的值

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_id = request.form['userid']

        if redis_handler.user_exists(user_id):
            flash('您已經投過票，不能重複投票！', 'danger')
            return redirect(url_for('login'))
        else:
            redis_handler.set_db(user_name, user_id)
            flash('新用戶創建成功', 'success')

        session['user_id'] = user_id  # 存儲用戶 ID 在會話中
        return redirect(url_for('info'))

    return render_template('login.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        president_choice = request.form['president']
        vice_president_choice = request.form['vice_president']
        #print(president_choice, vice_president_choice)
        user_id = session.get('user_id')  # 從會話中獲取用戶 ID
        public_key,private_key,public_key_pem, private_key_pem = generate_rsa_key_pair()
        encrypted_president_choice = encrypt_data(public_key,president_choice)
        encrypted_vice_president_choice = encrypt_data(public_key,vice_president_choice)
        #print(encrypted_president_choice, encrypted_vice_president_choice)
        redis_handler.store_key(user_id, public_key_pem, private_key_pem)
        redis_handler.update_vote(user_id, encrypted_president_choice, encrypted_vice_president_choice, president_choice, vice_president_choice)
        return redirect(url_for('success'))
   

    return render_template('info.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    decrypted_president_choice = None
    decrypted_vice_president_choice = None

    if request.method == 'POST':
        user_id = request.form['user_id']
        private_key_pem = request.form['private_key']

        encrypted_president_choice_b64 = redis_handler.get_president_encrypted(user_id)
        encrypted_vice_president_choice_b64 = redis_handler.get_vice_president_encrypted(user_id)

        if not encrypted_president_choice_b64 or not encrypted_vice_president_choice_b64:
            flash('沒有可顯示的結果', 'error')
            return redirect(url_for('check'))

        encrypted_president_choice = base64.b64decode(encrypted_president_choice_b64)
        encrypted_vice_president_choice = base64.b64decode(encrypted_vice_president_choice_b64)

        try:
            private_key = load_private_key(private_key_pem.encode('utf-8'))
        except ValueError as e:
            flash(f"Invalid private key", "error")
            return redirect(url_for('check'))

        # 解密用戶選擇
        decrypted_president_choice = decrypt_data(private_key, encrypted_president_choice)
        decrypted_vice_president_choice = decrypt_data(private_key, encrypted_vice_president_choice)

    return render_template('check.html', 
                           president_choice=decrypted_president_choice, 
                           vice_president_choice=decrypted_vice_president_choice)
    
@app.route('/success')
def success():
    user_id = session.get('user_id')
    
    president_choice = redis_handler.get_president_text(user_id)
    vice_president_choice = redis_handler.get_vice_president_text(user_id)

    return render_template('success.html',
                           president_choice=president_choice,
                           vice_president_choice=vice_president_choice)
        
@app.route('/haha')
def haha():
    return render_template('haha.html')

if __name__ == '__main__':
    app.run(debug=True)