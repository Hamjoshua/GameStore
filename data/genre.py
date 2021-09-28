import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Genre(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genre'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f'<Genre> id:{self.id} {self.name}'