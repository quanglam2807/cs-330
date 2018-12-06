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
db.query('CREATE TABLE IF NOT EXISTS posts (id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), title TEXT, author TEXT, content TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')
db.query('CREATE TABLE IF NOT EXISTS revisions (id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), title TEXT, author TEXT, content TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, postid UUID);')
db.query('CREATE TABLE IF NOT EXISTS views (id SERIAL PRIMARY KEY, postId UUID, ip TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        p = db.query('INSERT INTO posts (title, author, content) VALUES (:title, :author, :content) RETURNING *',
        title=title, author=author, content=content)
        
        postId = p.as_dict()[0]['id']

        db.query('INSERT INTO revisions (title, author, content, postId) VALUES (:title, :author, :content, :postId)',
        title=title, author=author, content=content, postId=postId)

        return redirect(url_for('read', postId=postId))
    return render_template('new.html')

@app.route('/read/<postId>')
def read(postId):
    p = db.query('SELECT * FROM posts WHERE id=:id', id=postId).first()

    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    db.query('INSERT INTO views (postId, ip) VALUES (:postId, :ip)', postId=postId, ip=ip)

    v = db.query('SELECT COUNT(DISTINCT ip) FROM views WHERE postId=:postId', postId=postId).first()

    return render_template('post.html', id=postId, title=p.title or 'Untitled', author=p.author or 'Unknown', content=p.content, date=p.date.strftime('%m/%d/%Y'), viewCount=v.count)

@app.route('/revisions/<postId>')
def revisions(postId):
    revisions = db.query('SELECT * FROM revisions WHERE postId=:postId ORDER BY date DESC', postId=postId).all()

    return render_template('revisions.html', title='Revisions', postId=postId, revisions=revisions)

@app.route('/revision/<revisionId>')
def revision(revisionId):
    p = db.query('SELECT * FROM revisions WHERE id=:id', id=revisionId).first()

    return render_template('revision.html', title=p.title or 'Untitled', author=p.author or 'Unknown', content=p.content, date=p.date.strftime('%m/%d/%Y'), postId=p.postid)


@app.route('/edit/<postId>', methods=['GET', 'POST'])
def edit(postId):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        db.query('UPDATE posts SET title=:title, author=:author, content=:content, date=CURRENT_TIMESTAMP',
            title=title, author=author, content=content, id=postId)

        db.query('INSERT INTO revisions (title, author, content, postId) VALUES (:title, :author, :content, :postId)',
            title=title, author=author, content=content, postId=postId)

        return redirect(url_for('read', postId=postId))
    p = db.query("SELECT * FROM posts WHERE id='" + postId + "' ").first()
    return render_template('edit.html', id=postId, author=p.author, title=p.title, content=p.content)

@app.route('/api/edit/<postId>', methods=['POST'])
def editApi(postId):
    data = request.data.decode('ascii')
    p = json.loads(data)

    db.query('UPDATE posts SET title=:title, author=:author, content=:content, date=CURRENT_TIMESTAMP WHERE id=:id',
        title=p['title'], author=p['author'], content=p['content'], id=postId)

    db.query('INSERT INTO revisions (title, author, content, postId) VALUES (:title, :author, :content, :postId)',
        title=p['title'], author=p['author'], content=p['content'], postId=postId)


    return jsonify(success=True)

if __name__ == '__main__':
    app.run()
