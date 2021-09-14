import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Platform(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'platform'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, nullable=False, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)