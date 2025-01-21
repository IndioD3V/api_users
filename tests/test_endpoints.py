import pytest 
from app import app
from database import db
from models import Users
from os import getenv
from datetime import date

SQL_LITE_TESTS = getenv('SQL_LITE_TESTS')

@pytest.fixture
def test_app():
    app.config['SQLALCHEMY_DATABASE_URI'] = SQL_LITE_TESTS
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_client(test_app):
    """Cria um cliente de teste para as requisições HTTP"""
    return test_app.test_client()


class TestCustomerResource:
    @pytest.fixture(autouse=True)
    def setup(self, test_client):
        self.client = test_client
    
    def test_post_new_customer(self):

        data =  [
                {
                    "birthday": str(date.today()),
                    "cpf": "026499461",
                    "email": "john.dee@blackmg.com",
                    "name": "John Dee",
                    "phone": "1361527169"
                }
            ]
        
        response = self.client.post("/users", json=data)
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data["operation"] == "created"
    
    def test_get_with_filter_id(self):

        new_customer = Users(**{
                    "id": 1,
                    "birthday": date.today(),
                    "cpf": "026499461",
                    "email": "john.dee@blackmg.com",
                    "name": "John Dee",
                    "phone": "1361527169"
                })
        db.session.add(new_customer)
        db.session.commit()


        response = self.client.get("/users/1")
        json_data = response.get_json()
        assert response.status_code == 200
        assert json_data['data'][0]["email"] == "john.dee@blackmg.com"


    def test_put_existing_record(self):

        new_customer = Users(**{
                    "id": 1,
                    "birthday": date.today(),
                    "cpf": "026499461",
                    "email": "john.dee@blackmg.com",
                    "name": "John Dee",
                    "phone": "1361527169"
                })
        db.session.add(new_customer)
        db.session.commit()

        updated_data = {
                "phone": "1361527170"
            }

        response = self.client.put(
            "/users/1", json=updated_data
        )

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["success"] is True
        assert json_data["operation"] == "update"
        assert json_data["values"]["phone"] == "1361527170"

    def test_put_nonexistent_record(self):

        new_customer = Users(**{
                    "id": 1,
                    "birthday": date.today(),
                    "cpf": "026499461",
                    "email": "john.dee@blackmg.com",
                    "name": "John Dee",
                    "phone": "1361527169"
                })
        db.session.add(new_customer)
        db.session.commit()

        updated_data = [
            {
                "phone": "1361527170"
            }
        ]

        response = self.client.put(
            "/users/1000", json=updated_data 
        )
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data["message"] == "User with field id:1000 not found."

    def test_delete_existing_record(self):
        
        new_customer = Users(**{
                    "id": 1,
                    "birthday": date.today(),
                    "cpf": "026499461",
                    "email": "john.dee@blackmg.com",
                    "name": "John Dee",
                    "phone": "1361527169"
                })
        db.session.add(new_customer)
        db.session.commit()
        
        response = self.client.delete(
            "/users/1"
        )
        
        assert response.status_code == 204


    def test_delete_nonexistent_record(self):
        new_customer = Users(**{
                    "id": 1,
                    "birthday": date.today(),
                    "cpf": "026499461",
                    "email": "john.dee@blackmg.com",
                    "name": "John Dee",
                    "phone": "1361527169"
                })
        db.session.add(new_customer)
        db.session.commit()
        
        response = self.client.delete(
            "/users/100"
        )
        
        assert response.status_code == 404
        json_data = response.get_json()
        assert json_data["success"] is False