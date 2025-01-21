from flask import Flask
from flask_restful import Api
from models.database import DataBase
from libs.resources import UsersResource
import os
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQL_LITE_TESTS')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DataBase.init_db(app)

api.add_resource(UsersResource, '/users', '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
