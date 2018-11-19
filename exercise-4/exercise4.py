from flask import Flask
from flask import redirect, url_for
from flask import request, make_response
from flask import render_template
import math

app = Flask(__name__)


def is_prime(n: int) -> bool:
    for i in range (2, n // 2 + 1):
        if n % i == 0:
            return False
    return True



def get_n_primes(n: int) -> list:
    i = 2
    lst = []
    while True:
        if is_prime(i):
            lst.append(i)
        i = i + 1
        if len(lst) >= n:
            return lst


@app.route('/')
def index():
    if request.args.get('n'):
        return redirect(url_for('get_primes', n=request.args.get('n')))
    
    if request.cookies.get('n'):
        return redirect(url_for('get_primes', n=request.cookies.get('n')))

    return redirect(url_for('ask_a_number'))

@app.route('/<int:n>')
def get_primes(n):
    lst = get_n_primes(n)

    response = make_response(render_template('prime_table.html', lst=lst))
    response.set_cookie('n', str(n))

    return response

@app.route('/ask', methods=['GET', 'POST'])
def ask_a_number():
    if request.method == 'POST':
        n = request.form['n']
        print(n)
        return redirect(url_for('get_primes', n=n))
    return render_template('ask.html')


if __name__ == '__main__':
    app.run()
