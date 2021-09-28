from flask import Flask, request, render_template, redirect, abort, session, jsonify, url_for, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
import random
import json

from functools import wraps
from data import db_session
from data.__all_models import *
from forms.register import Register
from forms.login import Login
from forms.buy_game import BuyGame
from forms.edit_user import EditUser
from forms.edit_game import EditGame
from forms.edit_publisher import EditPublisher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'amogus'
login_manager = LoginManager()
login_manager.init_app(app)

MISSING_IMAGE = '/static/missing.png'
NOT_FOUND_IMAGE = '/static/not_found.png'
FORBIDDEN_IMAGE = '/static/forbidden.png'


@app.errorhandler(401)
def unlogin_page(e):
    return redirect('/login')


@app.errorhandler(403)
def forbidden_page(e):
    print(e)
    error_image = FORBIDDEN_IMAGE
    return render_template('error.html', code=403, error_image=error_image, status='Доступ отклонен')


@app.errorhandler(404)
def unknown_page(e):
    print(e)
    error_image = NOT_FOUND_IMAGE
    return render_template('error.html', code=404,
                           error_image=error_image, status='Страница не найдена')


def admin_required(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if current_user.role_id == 2:
            return func(*args, **kwargs)
        else:
            return abort(403, 'Access denied')
    return decorated_func


def is_admin(user):
    if user.is_authenticated:
        return user.role_id == 2


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/main')
def main_page():
    db_sess = db_session.create_session()

    top_game = random.choice(db_sess.query(Game).filter(Game.rating > 9).all())
    genres = random.sample(db_sess.query(Genre).all(), 3)
    genres_games = list()

    for genre in genres:
        game_platforms = dict()
        game = db_sess.query(Game).\
            join(GenreGame, Game.id == GenreGame.game_id).\
            join(Genre, Genre.id == GenreGame.genre_id).\
            filter(Genre.id == genre.id).all()
        if len(game) > 3:
            game = game[0:3]
        game_platforms = list()
        for g in game:
            game_platforms_dict = dict()
            game_platforms_dict['game'] = g
            game_platforms.append(game_platforms_dict)
        genres_games.append({'genre': genre, 'games': game_platforms})
    publishers = random.sample(db_sess.query(Publisher).all(), 3)

    return render_template('main.html', top_game=top_game, genres_games=genres_games,
                           publishers=publishers)


@app.route('/game/<int:game_id>', methods=['GET', 'POST'])
def game_page(game_id):
    if request.method == 'POST':
        buy_data = json.dumps({'game_id': game_id})
        return redirect(url_for('.buy_game_page', buy_data=buy_data))

    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == game_id).first()
    genres = db_sess.query(GenreGame).filter(GenreGame.game_id == game_id).all()
    platforms = db_sess.query(PlatformGame).filter(PlatformGame.game_id == game_id).all()
    img_urls = get_images(game)

    usergame = None
    if current_user.is_authenticated:
        usergame = db_sess.query(UserGame). \
            filter((UserGame.game_id == game_id) & (UserGame.user_id == current_user.id)).first()

    return render_template('game.html', game=game, genres=genres,
                           platforms=platforms, img_urls=img_urls, usergame=usergame)


@app.route('/publisher/<int:pub_id>')
def publisher_page(pub_id):
    db_sess = db_session.create_session()
    publisher = db_sess.query(Publisher).filter(Publisher.id == pub_id).first()
    games = db_sess.query(Game).filter(Game.publisher_id == pub_id).all()
    genres = db_sess.query(Genre).join(GenreGame, GenreGame.genre_id == Genre.id).\
        join(Game, Game.id == GenreGame.game_id)\
        .filter(Game.publisher_id == pub_id).all()
    platforms = db_sess.query(Platform).join(PlatformGame, PlatformGame.platform_id == Platform.id).\
        join(Game, Game.id == PlatformGame.game_id) \
        .filter(Game.publisher_id == pub_id).all()
    developers = db_sess.query(Developer).join(Game, Game.developer_id == Developer.id)\
        .filter(Game.publisher_id == pub_id).all()

    img_urls_dict = dict()

    for game in games:
        img_urls_dict[game] = get_images(game)[0]

    publisher_img_url = get_images(publisher)

    return render_template('publisher.html', games=games, genres=genres, developers=developers,
                           platforms=platforms, publisher=publisher, img_urls_dict=img_urls_dict,
                           publisher_img_url=publisher_img_url)


@app.route('/user/<int:user_id>')
def user_page(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    games = db_sess.query(Game)\
        .join(UserGame, UserGame.game_id == Game.id)\
        .join(User, User.id == UserGame.user_id)\
        .filter(User.id == user_id).all()
    print(user.avatar_url)

    return render_template('user.html', games=games, user=user)


@app.route('/register', methods=['GET', 'POST'])
def register_user_page():
    form = Register()
    if form.validate_on_submit() and request.method == 'POST':
        db_sess = db_session.create_session()
        print(form.email)
        user_with_same_email = db_sess.query(User).filter(User.email == form.email.data).first()
        if user_with_same_email:
            flash('Пользователь с таким почтовым адресом уже существует')
            return render_template('register.html', form=form)

        user = User()
        user.login = form.login.data
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        user.role_id = 1
        user.description = form.description.data
        user.birthday = form.birthday.data
        user.address = form.address.data
        db_sess.add(user)
        db_sess.commit()
        flash('Добро пожаловать!')
        return redirect('/login')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user_page():
    form = Login()
    if form.validate_on_submit() and request.method == 'POST':
        db_sess = db_session.create_session()
        print(form.email.data)
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(user)
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect('/')
            flash('Неверный пароль')
        flash('Неверные данные')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/buy_game', methods=['GET', 'POST'])
@login_required
def buy_game_page():
    def add_game_to_user():
        usergame = UserGame()
        usergame.game_id = buy_data_json['game_id']
        usergame.user_id = current_user.id
        db_sess.add(usergame)
        db_sess.commit()

    buy_data = request.args['buy_data']
    # buy_data = session['buy_data']
    buy_data_json = json.loads(buy_data)
    if buy_data:
        form = BuyGame()
        db_sess = db_session.create_session()
        if form.validate_on_submit() and request.method == 'POST':
            add_game_to_user()
            return redirect(f'/user/{current_user.id}')
        game = db_sess.query(Game).get(buy_data_json['game_id'])
        if game.price == 0:
            add_game_to_user()
            return redirect(f'/user/{current_user.id}')

        usergame = db_sess.query(UserGame).\
            filter((UserGame.game_id == game.id) & (UserGame.user_id == current_user.id)).first()
        if usergame:
            return redirect('/')
        return render_template('buy_game.html', game=game, form=form)
    return redirect('/')


@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user_page(user_id):
    if current_user.id != user_id:
        return abort(403)

    form = EditUser()
    if form.validate_on_submit() and request.method == 'POST':
        db_sess = db_session.create_session()

        file_bg = form.bg_url.data
        file_body_bg = form.body_bg_url.data
        file_avatar = form.avatar_url.data

        print(file_bg.filename, 1)
        bg_url, body_bg_url, avatar_url = '', '', ''
        user = db_sess.query(User).get(current_user.id)

        if file_bg:
            bg_url = f'/static/user/bg/{file_bg.filename}'
            file_bg.save(bg_url[1:])
            if user.bg_url:
                os.remove(user.bg_url[1:])
            user.bg_url = bg_url

        if file_body_bg:
            body_bg_url = f'/static/user/body-bg/{file_body_bg.filename}'
            file_body_bg.save(body_bg_url[1:])
            if user.body_bg_url:
                os.remove(user.body_bg_url[1:])
            user.body_bg_url = body_bg_url

        if file_avatar:
            avatar_url = f'/static/user/avatar/{file_avatar.filename}'
            file_avatar.save(avatar_url[1:])
            if user.avatar_url:
                os.remove(user.avatar_url[1:])
            user.avatar_url = avatar_url

        user.name = form.name.data
        user.description = form.description.data
        user.address = form.address.data
        user.birthday = form.birthday.data
        db_sess.commit()

        return redirect(f'/user/{current_user.id}')

    form.name.data = current_user.name
    form.description.data = current_user.description
    form.bg_url.data = current_user.bg_url
    form.body_bg_url.data = current_user.body_bg_url
    form.avatar_url.data = current_user.avatar_url
    form.address.data = current_user.address
    form.birthday.data = current_user.birthday

    return render_template('edit_user.html', form=form)


@app.route('/game/<int:game_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_game_page(game_id):
    form = EditGame()
    db_sess = db_session.create_session()
    game = db_sess.query(Game).get(game_id)
    if request.method == 'POST':
        is_new_game = False
        if not game:
            game = Game()
            is_new_game = True
        game.name = form.name.data
        game.description = form.description.data
        game.rating = form.rating.data
        game.release_date = form.release_date.data
        game.publisher_id = form.publisher.data
        game.developer_id = form.developer.data
        if is_new_game:
            db_sess.add(game)

        clear_folder(game, form.old_img_urls.data)
        counter = 1
        for key in request.files:
            file = request.files[key]
            if file.filename:
                img_path = f'/static/game/{game_id}/{counter}.{file.filename.split(".")[1]}'
                file.save(img_path[1:])
            counter += 1

        update_genres(form, db_sess, game_id, game)
        update_platforms(form, db_sess, game_id, game)
        db_sess.commit()
        return redirect(f'/game/{game_id}')

    form.genres.choices = [(g.id, g.name) for g in db_sess.query(Genre)]
    form.platforms.choices = [(g.id, g.name) for g in db_sess.query(Platform)]
    form.developer.choices = [(g.id, g.name) for g in db_sess.query(Developer)]
    form.publisher.choices = [(g.id, g.name) for g in db_sess.query(Publisher)]
    if game:
        form.name.data = game.name
        form.genres.data = [g.id for g in get_genres(game)]
        form.platforms.data = [g.id for g in get_platforms(game)]
        form.developer.data = str(game.developer_id)
        form.publisher.data = str(game.publisher_id)
        form.description.data = game.description
        form.release_date.data = game.release_date
        form.rating.data = game.rating
        form.old_img_urls.data = str(get_images(game))
        form.validate_on_submit()
        # form.images.data = get_images(game)

    return render_template('edit_content.html', form=form, images_on=True,
                           game=game, title=f'Редактирование {game.name}')


@app.route('/publisher/<int:publisher_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_publisher_page(publisher_id):
    form = EditPublisher()
    return render_edit_content_page(form, publisher_id, Publisher)


@app.route('/developer/<int:developer_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_developer_page(developer_id):
    form = EditPublisher()  # разработчик и издатель схожи, поэтому форма не меняется
    return render_edit_content_page(form, developer_id, Developer)


def render_edit_content_page(form, persona_id, PersonaClass):
    db_sess = db_session.create_session()
    persona = db_sess.query(PersonaClass).get(persona_id)

    if request.method == 'POST':
        if not persona:
            persona = PersonaClass()
            db_sess.add(persona)
        persona.name = form.name.data
        persona.description = form.description.data
        avatar_img = form.avatar_url.data
        if avatar_img.filename:
            image_path = f'static/{persona.__tablename__}/{persona_id}'
            if not os.path.exists(image_path):
                os.mkdir(image_path)
            for _, _, filename in os.walk(image_path):
                if filename:
                    os.remove(f'{image_path}/{filename}')
            avatar_img.save(f'{image_path}/{avatar_img.filename}')
        db_sess.commit()
        return redirect(f'/{persona.__tablename__}/{persona_id}')

    if persona:
        form.name.data = persona.name
        form.description.data = persona.description
        form.avatar_url.data = get_images(persona)

    return render_template('edit_content.html', form=form, avatar_on=True,
                           titile=f'Редактирование {persona.name}')


def update_genres(form, db_sess, game_id, game):
    data_genres = form.genres.data

    for genre_id in data_genres:
        genre_game = db_sess.query(GenreGame) \
            .filter((GenreGame.game_id == game_id) & (GenreGame.genre_id == genre_id)).first()
        if not genre_game:
            new_genre_game = GenreGame(game_id=game_id, genre_id=genre_id)
            db_sess.add(new_genre_game)
            db_sess.commit()
    for genre_id in [g.id for g in get_genres(game)]:
        if genre_id not in data_genres:
            genre_game = db_sess.query(GenreGame) \
                .filter((GenreGame.game_id == game_id) & (GenreGame.genre_id == genre_id)).first()
            db_sess.delete(genre_game)
            db_sess.commit()


def update_platforms(form, db_sess, game_id, game):
    data_platforms = form.platforms.data

    for platform_id in data_platforms:
        platform_game = db_sess.query(PlatformGame) \
            .filter((PlatformGame.platform_id == platform_id)
                    & (PlatformGame.game_id == game_id)).first()
        if not platform_game:
            new_platform_game = PlatformGame(game_id=game_id, platform_id=platform_id)
            db_sess.add(new_platform_game)
            db_sess.commit()
    for platform_id in [p.id for p in get_platforms(game)]:
        if platform_id not in data_platforms:
            platform_game = db_sess.query(PlatformGame) \
                .filter((PlatformGame.game_id == game_id)
                        & (PlatformGame.platform_id == platform_id)).first()
            db_sess.delete(platform_game)
            db_sess.commit()


def clear_folder(sql_object, old_objects=[]):
    img_path = f'static/{sql_object.__tablename__}/{sql_object.id}'
    if not os.path.exists(img_path):
        os.mkdir(img_path)
    for _, _, filename in os.walk(img_path):
        for fn in filename:
            full_filename = f'{img_path}/{fn}'
            if os.path.isfile(full_filename) and ('/' + full_filename) not in old_objects:
                os.remove(full_filename)


def get_images(sql_object):
    if isinstance(sql_object, Game):
        img_path = f'static/game/{sql_object.id}'
        return get_all_images(img_path)
    else:
        img_path = f'static/{sql_object.__tablename__}/{sql_object.id}'
        return get_top_image(img_path)


def get_top_image(img_path):
    for _, _, filenames in os.walk(img_path):
        if filenames:
            return '/'.join(['', img_path, filenames[0]])
    return '/static/missing_avatar.png'


def get_all_images(img_path):
    img_urls = list()
    for _, _, filenames in os.walk(img_path):
        for filename in filenames:
            img_urls.append('/' + img_path + '/' + filename)
    if not img_urls:
        return [MISSING_IMAGE]
    return img_urls


def get_platforms(game: Game):
    db_sess = db_session.create_session()
    platforms = db_sess.query(Platform).\
        join(PlatformGame, PlatformGame.platform_id == Platform.id)\
        .filter(PlatformGame.game_id == game.id).all()
    return platforms


def get_genres(game: Game):
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).\
        join(GenreGame, GenreGame.genre_id == Genre.id).\
        filter(GenreGame.game_id == game.id)
    return genres


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


if __name__ == '__main__':
    app.jinja_env.globals.update(get_images=get_images)
    app.jinja_env.globals.update(get_platforms=get_platforms)
    app.jinja_env.globals.update(is_admin=is_admin)
    db_session.global_init('db/gamestore.db')
    app.run(host='127.0.0.1', port=8080)
