from flask import Flask, render_template, request, redirect, url_for, flash

from redis_get.redis_db import RedisHandler
from config import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD
app = Flask(__name__)
redis_handler = RedisHandler(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
app.secret_key = 'supersecretkey'  # 用於會話加密，請更換為更安全的值
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_id = request.form['userid']

        if redis_handler.user_exists(user_id):
            flash('用戶已存在', 'success')
            return redirect(url_for('candidates'))
        else:
            redis_handler.set_db(user_name, user_id)
            flash('新用戶創建成功', 'success')
            return redirect(url_for('candidates'))

    return render_template('login.html')

@app.route('/candidates')
def candidates():
    return render_template('candidates.html')

if __name__ == '__main__':
    app.run(debug=True)