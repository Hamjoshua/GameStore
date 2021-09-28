import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class UserGame(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user_game'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    game_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('game.id'),
                                nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('user.id'),
                                nullable=False)

    game = orm.relation('Game')
    user = orm.relation('User')

    def __repr__(self):
        return f'<UserGame> id:{self.id} ({self.user}, {self.game})'