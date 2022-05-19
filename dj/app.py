import os
import requests
import getreddit
import json
from producer import publish

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
from flask_migrate import Migrate, MigrateCommand

# YT_API_KEY, yt_query, , url_to_stream old, nn?
from search_yt import get_vid_name


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://test:test@db:5432/dj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

CORS(app)

db = SQLAlchemy(app)

db.drop_all()
db.create_all()
migrate = Migrate(app, db)


@dataclass
class Song(db.Model):
    __tablename__ = 'songs'
    # __table_args__ = {''}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    url = db.Column(db.String(200))

    UniqueConstraint('id', 'url', name='id_url_unique')

    def serialize(self):
        return {'id': self.id, 'title': self.title, 'url': self.url}


@dataclass
class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    user_in = db.Column(db.String(200))

    def serialize(self):
        return {'id': self.id, 'user_in': self.user_in}


@app.route('/api/songs')
def index():
    return jsonify(Song.query.all())


@app.route('/api/<string:cmd>/<string:terms>')
def make_playlist(cmd, terms):
    print('MAKING PLAYLIST')
    if cmd == 'r':
        try:
            dirty_terms = json.loads(getreddit.get_yt_subs(terms))
            return jsonify(dirty_terms)
        except:
            print('Error getting reddit subs, probably not found')
            return


@app.route('/api/<string:cmd>/<string:terms>/clean')
def clean_playlist(cmd, terms):
    if cmd == 'r':
        res = make_playlist(cmd, terms)
        print(res)
        playlist = json.loads(res.data)
        print(playlist)
        for track in playlist:
            print(track)
            print(playlist[track])
            playlist[track] = get_vid_name(playlist[track])
        print(playlist)
        return jsonify(playlist)


@app.route('/api/<string:cmd>/<string:terms>/playlist')
def publish_songs(cmd, terms):
    res = clean_playlist(cmd, terms)
    playlist = json.loads(res.data)
    for track in playlist:
        song = Song(title=playlist[track]['title'], url=playlist[track]['url'])
        publish('song_created', song.serialize())
    return jsonify(playlist)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
