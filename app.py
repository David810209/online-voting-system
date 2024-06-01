from flask import Flask, render_template, request, redirect, url_for, flash, session

from redis_get.redis_db import RedisHandler
from encrypt.rsa_process import rsa_handler
from config import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD
app = Flask(__name__)
redis_handler = RedisHandler(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
rsa_handler = rsa_handler()
app.secret_key = 'supersecretkey'  # 用於會話加密，請更換為更安全的值

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_id = request.form['userid']

        if redis_handler.user_exists(user_id):
            flash('用戶已存在', 'success')
        else:
            redis_handler.set_db(user_name, user_id)
            flash('新用戶創建成功', 'success')

        session['user_id'] = user_id  # 存儲用戶 ID 在會話中
        return redirect(url_for('info'))

    return render_template('login.html')

@app.route('/info', methods=['GET', 'POST'])
def candidates():
    if request.method == 'POST':
        president_choice = request.form['president']
        vice_president_choice = request.form['vice_president']
        user_id = session.get('user_id')  # 從會話中獲取用戶 ID
        encrypted_president_choice = rsa_handler.encrypt(president_choice)
        encrypted_vice_president_choice = rsa_handler.encrypt(vice_president_choice)
        redis_handler.update_private_key(user_id, encrypted_president_choice, encrypted_vice_president_choice)
   

    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)