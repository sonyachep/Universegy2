import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class Tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'relations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    task_block = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tasks_done = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    right_answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
