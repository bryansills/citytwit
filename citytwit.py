from flask import Flask, jsonify, request
import datetime

application = Flask(__name__)

tweets = [
    {
        'author': 'me',
        'text': 'yo',
        'author_img': 'http://i.imgur.com/BA98QMi.jpg',
        'timestamp': datetime.datetime.now()
    }
]

@application.route('/', methods=['GET'])
def get_tweets():
    return jsonify({'results': tweets})

@application.route('/', methods=['POST'])
def add_tweet():
    tweet = {
        'author': request.json['author'],
        'text': request.json['text'],
        'author_img': request.json['author_img'],
        'timestamp': datetime.datetime.now()
    }
    tweets.append(tweet)
    return jsonify({'results': tweets}), 201

if __name__ == '__main__':
    application.run(debug=True)
