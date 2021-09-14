import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class GenreGame(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genre_game'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    game_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('game.id'),
                                nullable=False)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('genre.id'),
                                 nullable=False)

    game = orm.relation('Game')
    genre = orm.relation('Genre')
