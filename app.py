from flask import Flask
from flask_restx import Api, Resource, Namespace

app = Flask(__name__)
api = Api(app)

if __name__ == '__main__':
    app.run()
