from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class PuppyFeed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content= db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Feed %r>' % self.id
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_feed = PuppyFeed(content=task_content)

        try:
            db.session.add(new_feed)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your feed record'

    else:
        feeds= PuppyFeed.query.order_by(PuppyFeed.date_created).all()
        return render_template('index.html', feeds=feeds)
    

@app.route('/delete/<int:id>')
def delete(id):
    feed_to_delete = PuppyFeed.query.get_or_404(id)

    try:
        db.session.delete(feed_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that feed record'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    feed = PuppyFeed.query.get_or_404(id)
    if request.method == 'POST':
        feed.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a issue updating your feed record'
    else:
        return render_template('update.html', feed=feed)

    

