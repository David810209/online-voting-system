from flask import Flask, render_template, request, redirect, url_for, flash, session, flash
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#from flask_talisman import Talisman
import base64
from redis_get.redis_db import RedisHandler
from encrypt.rsa_process import rsa_handler
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
        return redirect(url_for('info'))

    return render_template('login.html')
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    if request.method == 'POST':
        president_choice = request.form['president']
        vice_president_choice = request.form['vice_president']
        user_id = session.get('user_id')  # 從會話中獲取用戶 ID
        if redis_handler.has_voted(user_id):  # Check if the user has already voted
            flash('您已經投過票，不能重複投票！(刷新頁面)', 'danger')
            return redirect(url_for('info'))
        rsa = rsa_handler()
        encrypted_president_choice = rsa.encrypt_data(president_choice)
        encrypted_vice_president_choice = rsa.encrypt_data(vice_president_choice)
        redis_handler.update_vote(user_id, encrypted_president_choice, encrypted_vice_president_choice)
        return redirect(url_for('success'))
    return render_template('info.html')
    
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