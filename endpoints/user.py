from models import Users
from .resources import BaseResource

class UsersResource(BaseResource):
    table = Users
    def put(self, user_id):
        return super().put('id', user_id)
    
    def get(self, user_id=None):
        return super().get('id', user_id)
    
    def delete(self, user_id):
        return super().delete('id', user_id)