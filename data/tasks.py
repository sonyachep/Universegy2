import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'relations'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    tasks_done = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    task_block = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    right_answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)