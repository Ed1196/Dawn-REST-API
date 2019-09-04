from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.locations import LocationModel

class Location(Resource):
    """ Class that will handle endpoint requests, this is the extenal representation of the location entity.

        Attributes:
            __player_parse: Variable that will let us to  parse data from payload.

    """
    __location_parser = reqparse.Request_Parser()
    __location_parser.add_argument(
        'owner',
        type=str,
        required=True,
        help='Player name needs to be provided!'
    )
    def get(self, location_name):
        """Class method: GET

            Class method that handles GET requests for the Location Resource.
            Locations data retrieval is accomplished using owner string supplied in
            the Body.

        Args:
            location_name: Name supplied via URL parameters.

        Returns:
            'message' if the location exists return relative data for that location, otherwise 
                        error message stating that the location was not found.

        """
        data = Location.__location_parser.parse_args()
        location = LocationModel.findByName(location_name, data['owner'])
        if location is not None:
            return location.json()
        return {'message': 'Location does not exists'}

class LocationGenerator(Resource):
    """ Class that will handle endpoint requests, this is the extenal representation of the location generator entity.

        Attributes: 


    """
   