import flask
from flask import jsonify

from . import db_session
from .tasks import Tasks
from .users import User
from flask_restful import abort, Resource

blueprint = flask.Blueprint(
    'uni_api',
    __name__,
    template_folder='templates'
)


def abort_if_deck_not_found(id):
    session = db_session.create_session()
    deck = session.query(User).get(id)
    if not deck:
        abort(404, message=f"User {id} not found")


class UniResource(Resource):
    def get(self, id):
        session = db_session.create_session()
        user = session.query(User).get(id)
        task = session.query(Tasks).filter(Tasks.user_id == id).all()
        print(task)
        return jsonify({'user':
            {
                'info': user.to_dict(only=('id', 'name', 'surname', 'grade')),
                'task': {elem.id: elem.to_dict(only=('date', 'task_block', 'tasks_done', 'right_answers')) for elem in task
             }
            }})
