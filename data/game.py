import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Game(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game'

    id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    release_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    publisher_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey('publisher.id'),
                                     nullable=False)
    developer_id = sqlalchemy.Column(sqlalchemy.Integer,
                                     sqlalchemy.ForeignKey('developer.id'),
                                     nullable=False)
    rating = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    publisher = orm.relation('Publisher')
    developer = orm.relation('Developer')