from flask import Flask
from flask_migrate import Migrate
import os
from flask_restful import Api
from models.database import DataBase
from libs.resources import (
    UsersResource
)

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, os.getenv('SQLALCHEMY_DATABASE_URI'))}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DataBase.init_db(app)

db = DataBase.db
migrate = Migrate(app, db)

api.add_resource(UsersResource, '/users', '/users/<int:user_id>' )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
