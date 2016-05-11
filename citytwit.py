from flask import Flask, jsonify, request, render_template, redirect, url_for
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import Form
import datetime

SECRET_KEY = 'secret'

application = Flask(__name__)
application.config.from_object(__name__)

tweets = [
    {
        'author': 'me',
        'text': 'yo',
        'author_img': 'http://i.imgur.com/BA98QMi.jpg',
        'timestamp': datetime.datetime.now().isoformat('T')
    }
]

class AddForm(Form):
    author = TextField("Author", validators=[DataRequired()])
    author_img = TextField("Author Image", validators=[DataRequired()])
    text = TextField("Text", validators=[DataRequired()])
    submit = SubmitField("Send")


@application.route('/', methods=['GET'])
def get_tweets():
    return jsonify({'results': tweets})

@application.route('/', methods=['POST'])
def add_tweet():
    tweet = {
        'author': request.json['author'],
        'text': request.json['text'],
        'author_img': request.json['author_img'],
        'timestamp': datetime.datetime.now().isoformat('T')
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
