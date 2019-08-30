from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.locations import LocationModel

class Location(Resource):
    def get(self, location_name):
        return 

class LocationGenerator(Resource):
    def post()