from flask import Flask, request, render_template, redirect, abort, session, jsonify, url_for
import os

from data import db_session
from data.__all_models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'amogus'


@app.route('/')
@app.route('/main')
def main_page():
    return render_template('base.html')


@app.route('/game/<int:game_id>')
def game(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == game_id).first()
    genres = db_sess.query(GenreGame).filter(GenreGame.game_id == game_id).all()
    print(genres[0].genre.name)
    platforms = db_sess.query(PlatformGame).filter(PlatformGame.game_id == game_id).all()
    img_urls = list()
    game_img_path = f'static/game/{game_id}'
    try:
        for _, _, filenames in os.walk(game_img_path):
            for filename in filenames:
                print(filename)
                img_urls.append('/' + game_img_path + '/' + filename)

    except Exception as e:
        print(e)
        img_urls = ['/static/missing.png']

    if not img_urls:
        img_urls = ['/static/missing.png']

    print(img_urls)
    return render_template('game.html', game=game, genres=genres,
                           platforms=platforms, img_urls=img_urls)


if __name__ == '__main__':
    db_session.global_init('db/gamestore.db')
    app.run(host='127.0.0.1', port=8080)
