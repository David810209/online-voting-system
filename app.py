from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/candidates')
def candidates():
    return render_template('candidates.html')

if __name__ == '__main__':
    app.run(debug=True)
