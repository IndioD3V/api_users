from database import db

class DataBase:
    db = db
    @staticmethod
    def init_db(app):
        db.init_app(app)
        with app.app_context():
            db.create_all()