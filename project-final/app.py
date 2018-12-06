from flask import Flask
from flask import redirect, url_for
from flask import request, make_response
from flask import render_template
from flask import jsonify
import records
import datetime
import json

app = Flask(__name__, static_url_path='/static')

db = records.Database('postgres://lpdcysppdcnrhz:38fb0220bc38e2910cb463f5ee390397c933b2d2c413f21b8adab8d95b479b86@ec2-54-197-249-140.compute-1.amazonaws.com:5432/dbgpvgsk9i4es5')

db.query('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
db.query('CREATE TABLE IF NOT EXISTS posts (id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), title TEXT, author TEXT, content TEXT, date TEXT, userId INT );')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        d = datetime.datetime.today().strftime('%m/%d/%Y')

        p = db.query('INSERT INTO posts (title, author, content, date) VALUES (:title, :author, :content, :date) RETURNING *',
        title=title, author=author, content=content, date=d)
        
        i = p.as_dict()[0]['id']
        return redirect(url_for('read', postId=i))
    return render_template('edit.html')

@app.route('/read/<postId>')
def read(postId):
    p = db.query('SELECT * FROM posts WHERE id=:id', id=postId).first()
    return render_template('post.html', id=postId, title=p.title, author=p.author, content=p.content, date=p.date)

@app.route('/edit/<postId>', methods=['GET', 'POST'])
def edit(postId):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        d = datetime.datetime.today().strftime('%m/%d/%Y')

        p = db.query('UPDATE posts SET title=:title, author=:author, content=:content, date=:date WHERE id=:id',
        title=title, author=author, content=content, date=d, id=postId)
        
        return redirect(url_for('read', postId=postId))
    p = db.query("SELECT * FROM posts WHERE id='" + postId + "' ").first()
    return render_template('edit.html', id=postId, title=p.title, author=p.author, content=p.content, date=p.date)

@app.route('/api/edit/<postId>', methods=['POST'])
def editApi(postId):
    data = request.data.decode('ascii')
    p = json.loads(data)

    d = datetime.datetime.today().strftime('%m/%d/%Y')

    db.query('UPDATE posts SET title=:title, author=:author, content=:content, date=:date WHERE id=:id',
    title=p['title'], author=p['author'], content=p['content'], date=d, id=postId)

    return jsonify(success=True)

if __name__ == '__main__':
    app.run()
