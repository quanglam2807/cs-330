from flask import Flask
from flask import redirect, url_for
from flask import request, make_response
from flask import render_template
from flask import jsonify
import json

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get')
def get():
    with open('data.json', 'r') as f:
        data = f.read()
        if len(data) > 0:
            lst = json.loads(data)
            return jsonify(lst)
        return jsonify([])

@app.route('/save', methods=['POST'])
def save():
    data = request.data.decode('ascii')
    with open('data.json', 'w') as f:
        f.write(data)

    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
