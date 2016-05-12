import os

from flask import Flask, jsonify, request, render_template, redirect, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
from json import dumps
from datetime import datetime, timezone

SECRET_KEY = 'secret'

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80))
    author_img = db.Column(db.String(80))
    text = db.Column(db.String(140))
    timestamp = db.Column(db.String(50))

    def __init__(self, author, author_img, text, timestamp):
        self.author = author
        self.author_img = author_img
        self.text = text
        self.timestamp = timestamp

    def json_dump(self):
        return dict(author=self.author, author_img=self.author_img, text=self.text, timestamp=self.timestamp)

    def __repr__(self):
        return '<Author %r>' % self.author

class AddForm(Form):
    author = TextField("Author", validators=[DataRequired()])
    author_img = TextField("Author Image", validators=[DataRequired()])
    text = TextField("Text", validators=[DataRequired()])
    submit = SubmitField("Send")


@app.route('/', methods=['GET'])
def get_tweets():
    tweets = Tweet.query.all()
    return make_response(dumps([t.json_dump() for t in tweets]))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        author = form.author.data
        author_img = form.author_img.data
        text = form.text.data
        timestamp = datetime.now(timezone.utc).astimezone().isoformat()
        tweet = Tweet(author, author_img, text, timestamp)

        db.session.add(tweet)
        db.session.commit()

        return redirect(url_for("get_tweets"))
    return render_template('add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
