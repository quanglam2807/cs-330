from flask import Flask
from flask import redirect, url_for
from flask import request, make_response
from flask import render_template
from flask import session

app = Flask(__name__)

app.secret_key = '2361534534'

@app.route('/')
def index():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login')
def login():
    if request.args.get('username'):
        session['username'] = request.args.get('username')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
