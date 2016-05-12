import os

from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
from json import dumps
from datetime import datetime, timezone

SECRET_KEY = 'secret'

application = Flask(__name__)
application.config.from_object(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

tweets = [
    {
        'author': 'me',
        'text': 'yo',
        'author_img': 'http://i.imgur.com/BA98QMi.jpg',
        'timestamp': datetime.now(timezone.utc).astimezone().isoformat()
    }
]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    author_img = db.Column(db.String(80))
    text = db.Column(db.String(140))
    timestamp = db.Column(db.Sring(50))

    def __init__(self, author, author_img, text, timestamp):
        self.author = author
        self.author_img = author_img
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return '<Author %r>' % self.author

class AddForm(Form):
    author = TextField("Author", validators=[DataRequired()])
    author_img = TextField("Author Image", validators=[DataRequired()])
    text = TextField("Text", validators=[DataRequired()])
    submit = SubmitField("Send")


@application.route('/', methods=['GET'])
def get_tweets():
    return make_response(dumps(tweets))

@application.route('/', methods=['POST'])
def add_tweet():
    tweet = {
        'author': request.json['author'],
        'text': request.json['text'],
        'author_img': request.json['author_img'],
        'timestamp': datetime.now(timezone.utc).astimezone().isoformat()
    }
    tweets.append(tweet)
    return jsonify({'results': tweets}), 201

@application.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        tweet = {
            'author': form.author.data,
            'author_img': form.author_img.data,
            'text': form.text.data,
            'timestamp': datetime.datetime.now()
        }
        tweets.append(tweet)
        return redirect(url_for("get_tweets"))
    return render_template('add.html', form=form)

if __name__ == '__main__':
    application.run(debug=True)
