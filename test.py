from data import db_session
from flask_restful import Api
from flask import Flask, render_template, redirect, request, abort
from data import uni_api


app = Flask(__name__)
api = Api(app)


def main():
    db_session.global_init("db/Universegy.db")
    api.add_resource(uni_api.DeckResource, '/api/uni/<int:id>')
    app.run()


if __name__ == '__main__':
    main()