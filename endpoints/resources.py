# External
from flask_restful import Resource
from flask import request, jsonify, make_response
from models.query import Query


class BaseResource(Resource, Query):
    table = None
    
    def get(self, field=None, key_value=None):
        
        page = request.args.get('page', 1, type=int)
        peer_page = request.args.get('peer_page', 10, type=int)
        
        data = self.get_values(**{
            'page': page,
            'peer_page': peer_page,
            'field': field,
            'key_value': key_value
            }
        )
        
        return make_response(jsonify({
            'data': [row for row in data],
            'pagination': {
                'page': page,
                'peer_page': peer_page,
                'total': self.total,
                'total_pages': self.total_pages
            }
        }), 200)

    def post(self):
        data = request.get_json()

        return make_response(
            jsonify({
                "operation": "created",
                "values": self.insert_values(data)
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
            



    
