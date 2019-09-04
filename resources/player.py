from flask_restful import Resource, reqparse
from models.player  import PlayerModel
from models.locations import LocationModel

class PlayerRegister(Resource):
    """ 
    This is a Resource for player registration operations. 
      
    Attributes: 
        __player_parse: Variable that will let us to  parse data from payload. 
    """
    #: object variable that will allow us to parse data from request body
    __player_parse = reqparse.RequestParser()

    # Using __player_parse to specify the data we want to use from the data being passed from the request body
    __player_parse.add_argument(
        'playerName',
        type=str,
        required=True,
        help='Player name needs to be provided!'
    )
    # Using __player_parse to specify the data we want to use from the data being passed from the request body
    __player_parse.add_argument(
        'secretKey',
        type=str,
        required=True,
        help='Secret Key name needs to be provided!'
    )

    def post(self):
        """Class methods: POST

            Class method that handles post requests for the PlayerRegister Resource.
            Using payload from the POST request, it will use the 'playerName' and 
            the 'secretKey' that were provided to create a new player. This class will
            only handle the registering process.

        Args:

        Returns:
            'message' if either the user already exists or if the player was created succesfully.

        """

        #: object of parsed items set to their appropiate type: This data is reetrieved from payload.
        data = PlayerRegister.__player_parse.parse_args()

        # Check if the player name is already taken
        if(PlayerModel.findByPlayerName(data['playerName'])):
            return {'message': 'User already exists!'}, 409 #Conflict

        
        # Uses the PlayerRegister function save_to_db() function that uses SQLAlchemys save and commit to register the player
        # to the database
        player = PlayerModel(data['playerName'], data['secretKey'], 'player', 'alive', 'none', 100, 100)
        player.save_to_db()
        

        return {'message': 'Player was created succesfully!'}, 201


class Player(Resource):
    """
    This resource will handle any update, deletions and retrival of player data.

    Attributes:
        __player_parse: Variable that will let us to  parse data from payload. 

    """

    __player_parse = reqparse.RequestParser()

    __player_parse.add_argument(
        'location',
        type = str, 
        required= True,
        help='Location must be provided!'
    )

    @classmethod
    def get(cls, playerName):
        """Class method: GET

            Class method that handles GET requests for the Player Resource.
            Player data retrieval is accomplished using player id supplied in
            the URL parameters

        Args:
            playerName: Name supplied via URL parameters

        Returns:
            'message' if the player exists return relative data for that player, otherwise 
                        error message stating that the user was not found.

        """
        
        try:
            #: Object of type PlayerModel: Will store an object of the player we want data from.
            player = PlayerModel.findByPlayerName(playerName)
        except:
            return {'message': 'There was an error finding the player in the DB!'}

        if player is not None:
            return player.json()

        return {'message': 'Player was not found!'}