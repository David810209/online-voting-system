from flask import Flask, render_template, request, redirect, url_for, flash, session, flash
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#from flask_talisman import Talisman
import base64
from redis_get.redis_db import RedisHandler
from encrypt.rsa_process import encrypt_data, decrypt_data
from config import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD, FLASK_SECRET_KEY

app = Flask(__name__)
#Talisman(app)
redis_handler = RedisHandler(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

    
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "300 per hour"]
)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("請先登入！(刷新頁面)", "danger")
            return redirect(url_for('login'))  # 將用戶重定向到登入頁面
        return f(*args, **kwargs)
    return decorated_function

app.secret_key = FLASK_SECRET_KEY  # 用於會話加密，請更換為更安全的值

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_id = request.form['userid']
        redis_handler.set_db(user_name, user_id)

        session['user_id'] = user_id  # 存儲用戶 ID 在會話中
        return redirect(url_for('select'))

    return render_template('login.html')
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')

@app.route('/select', methods=['GET', 'POST'])
@login_required
def select():
    return render_template('select.html')

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    if request.method == 'POST':
        president_choice = request.form['president']
        vice_president_choice = request.form['vice_president']
        public_key = request.form['public_key']
        user_id = session.get('user_id')  # 从会话中获取用户 ID
        
        if redis_handler.has_voted(user_id):  # 检查用户是否已经投票
            flash('您已经投过票，不能重复投票！(刷新页面)', 'danger')
            return redirect(url_for('info'))
        
        encrypted_president_choice = encrypt_data(president_choice,public_key)
        encrypted_vice_president_choice = encrypt_data(vice_president_choice,public_key)
        
        redis_handler.update_vote(user_id, encrypted_president_choice, encrypted_vice_president_choice)
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

        # 解密用戶選擇
        decrypted_president_choice = decrypt_data(encrypted_president_choice,private_key_pem)
        decrypted_vice_president_choice = decrypt_data(encrypted_vice_president_choice,private_key_pem)

    return render_template('check.html', 
                           president_choice=decrypted_president_choice, 
                           vice_president_choice=decrypted_vice_president_choice)



@app.route('/getkey', methods=['POST'])
def get_key():
    data = request.get_json()
    user_id = data['user_id']
    public_key = redis_handler.get_public_key(user_id)
    private_key = redis_handler.get_private_key(user_id)
    return render_template("getkey.html", private_key=private_key, public_key=public_key)

@app.route('/success')
@login_required
def success():
    return render_template('success.html')
        
@app.route('/haha')
@login_required
def haha():
    return render_template('haha.html')

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)  # 清除會話中的用戶 ID
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)