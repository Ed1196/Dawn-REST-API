from flask_restful import Resource, reqparse
from models.player  import PlayerModel
from models.locations import LocationModel
from flask_jwt import jwt_required, current_identity

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
        """ Class methods: POST
            Endpoint: /player-register

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
        """ Class method: GET
            Endpoint: /player

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

class PlayerLocation(Resource):
    """This resource will handle game logic when it comes to a player wanting to change location.

    Attributes:
        __player_parse: Variable that will let us to  parse data from payload. 
    """

    parse = reqparse.RequestParser()
    parse.add_argument(
        'locationId',
        type=int,
        required = True,
        help='Location must be provided!'

    )

    @jwt_required()
    def get(self):
        """ Class method: GET
            Endpoint: /player-location

            Will return a players current location details only if that player is authorized and part of a lobby.
        """
        player   = PlayerModel.findByPlayerId(current_identity.id)
        if(player.locationId == -1):
            return {'message': 'You are not currently part of a lobby!'}
        location = LocationModel.findById(player.locationId)
        return location.json()

    @jwt_required()
    def post(self):
        """ Class method: POST
            Endpoint: /player-location

            Will change a players location depending on the id of the location they want to go. 
            Error check must look for the following. If player is part of the lobby, 
        """
        data = PlayerLocation.parse.parse_args()
        player = PlayerModel.findByPlayerId(current_identity.id)
        
        if(player.locationId == data['locationId']):
            return {'message':'Already at that location.'}

        try:
            player.locationId = data['locationId']
            player.stamina    = player.stamina - 10
            if(player.stamina == 0):
                player.status = "sleep"
                player.save_to_db()
                return {'message': 'You are out of stamina and have fallen asleep!'}
            player.save_to_db()
        except:
            return {'message': 'Error saving to the DB!'}

        return {'message': 'You have succesfully changed locations.'}


class PlayerConfrontation(Resource):
    """ This resource will handle the player confrontation action and will alter player stats as they make choices.

        Attributes:
            parse: Variable that will let us parse the data from the payload from the request body.

    """
    parse = reqparse.RequestParser()
    parse.add_argument(
        'player',
        type=str,
        required=True,
        help='No target was selected!'
    )

    @jwt_required()
    def post(self):
        data = PlayerConfrontation.parse.parse_args()
        player = PlayerModel.findByPlayerId(current_identity.id)
        enemy = PlayerModel.findByPlayerId(data['player'])
        confrontation = player.confront(enemy.playerName)
        return {'message':confrontation}


class PlayerAction(Resource):
    """This resource will handle different player actions and will alter player stats as they make choices.

        Attributes:
            parse: Variable that will let us parse the data from the payload from the request body.
    """ 

    parse = reqparse.RequestParser()
    parse.add_argument(
        'action',
        type=str,
        required=True,
        help='Action is required!'
    )


    @jwt_required()
    def post(self):
        """ Class method: POST
            /action

        """
        data = PlayerAction.parse.parse_args()

        
        if(data['action'] == 'sleep'):
            player = PlayerModel.findByPlayerId(current_identity.id)
            player.stamina = player.stamina + 10
            player.save_to_db()
            return {'message': 'You decided to sleep: +10 stamina'}
        elif(data['action'] == 'workout'):
            if(player.stamina == 0):
                player.status = "sleep"
                player.save_to_db()
                return {'message': 'You are out of stamina and have fallen asleep!'}

            player = PlayerModel.findByPlayerId(current_identity.id)
            player.strength = player.strength + 10
            player.stamina = player.stamina - 10
            player.status = "sleep"
            
            player.save_to_db()
            return {'message': 'You decided to sleep: +10 strength -10 stamina'}
        else:
            return {'message': 'Action is not supported!'}




        



