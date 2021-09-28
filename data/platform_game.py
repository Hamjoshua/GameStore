import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class PlatformGame(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'platform_game'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    game_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('game.id'),
                                nullable=False)
    platform_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey('platform.id'),
                                    nullable=False)

    platform = orm.relation('Platform')
    game = orm.relation('Game')

    def __repr__(self):
        return f'<PlatformGame> id:{self.id} ({self.platform}, {self.game})'