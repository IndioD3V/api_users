# External
from flask_restful import Resource
from flask import request, jsonify, make_response
from models.query import Query

# Internal
from models import Users
from dataclasses import dataclass


@dataclass
class BaseResource(Resource, Query):
    table = None
    
    def get(self, field=None, key_value=None):
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        data = self.get_values(**{
            'page': page,
            'per_page': per_page,
            'field': field,
            'key_value': key_value
            }
        )
        
        return make_response(jsonify({
            'data': [row for row in data],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': self.total,
                'total_pages': self.total_pages
            }
        }), 200)

    def post(self):
        data = request.get_json()

        return make_response(
            jsonify({
                "operation": "created",
                "values": [row for row in self.insert_values(data)]
            }), 201
        )
    
    def put(self, field, key_value):
        data = request.get_json()
        
        status, values = self.update_values(data, field, key_value)
        
        if status:
            return make_response(
                jsonify({
                    "success": True,
                    "operation": "update",
                    "values": values
                }), 200
            )
        else:
            return make_response(jsonify({
                "success": False,
                "error": "NotFound",
                "message": values
            }), 404)
    
    def delete(self, field, key_value):
        
        if self.remove_values(field, key_value):
            return make_response(jsonify({"success": True}), 204)
        else:
            return make_response(jsonify({"success": False}), 404)
            

@dataclass
class UsersResource(BaseResource):
    table = Users
    def put(self, user_id):
        return super().put('id', user_id)
    
    def get(self, user_id=None):
        return super().get('id', user_id)
    
    def delete(self, user_id):
        return super().delete('id', user_id)
    
