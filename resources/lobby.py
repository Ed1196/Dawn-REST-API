from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.lobby import LobbyModel
from models.player import PlayerModel
from models.locations import LocationModel

class CreateLobby(Resource):
    """Class use to handle game lobby creation endpoints. This is the external representation of the 
        lobby entity. This is what other programmers will use to access our data.

    Attributes:

    """
    @jwt_required()
    def post(self):
        """ Class method: POST  


            Class method that will handle POST request for the CreateLobby Resource.
            Users that will hit the '/create-lobby' will use this method. 

            Attributes:
            Return:
                return a successful message that the Lobby has been created.
                return an error message if the lobby could not be made

        """
        playerName = current_identity.playerName
        player     = PlayerModel.findByPlayerName(playerName)

        # Checks if the user creating the lobby isn't part of one already
        if(player.currentLobby == -1):

            try:
                newLobby            = LobbyModel(player.playerName)
                newLobby.save_to_db()
            except:
                return {'message': 'Could not create lobby. Error with creating lobby.'}
            
            try:
                home                = LocationModel(player.playerName, 'home')
                home.save_to_db()
            except:
                return {'message': 'Could not create lobby. Error with creating player home.'}
            
            try:
                player.currentLobby = newLobby.lobbyId
                player.homeId       = home.id
                player.locationId   = home.id 
                player.save_to_db()
            except:
                return {'message': 'Could not create lobby. Error with setting player details'}

            try:
                clerkName=''.join(reversed(player.playerName))
                secretKey=''.join(reversed(player.secretKey))

                storeClerk =PlayerModel(clerkName, secretKey, 'npc', 'alive', 'none', 100, 100)
                store = LocationModel(clerkName, 'store')
                store.save_to_db()

                storeClerk.homeId = store.id
                storeClerk.locationId = store.id
                storeClerk.currentLobby = player.currentLobby
                storeClerk.save_to_db()
            except:
                return {'message': 'Could not create lobby. Error with creating clerk'}

            return {'message': 'Lobby was created succesfully!'}

        return {'message': 'Lobby already exists!'}


class Lobby(Resource):
    """Class use to handle game lobby access and lobby update endpoints. This class is separate from
        the CreateLobby resources as we can only join and not create lobbies in this endpoint.

    Attributes:

    """
    #
    def get(self,lobby_id):
        """Class Method used for GET request for game lobby data.

        Args:
            lobby_id: Id of the lobby we want to trieve data from.

        Return:
            Lobby object json, if lobby exists
            error message, if lobby does not exists

        """
        #: Object of type LobbyModel: Using SQLAlchemy this object will give us access and allow us to manipulate the lobby object in the DB
        lobby = LobbyModel.findById(lobby_id)
        if lobby is not None:
            return lobby.json()

        return {'message': 'Lobby does not exist!'}

    # Post request to join a lobby.
    @jwt_required()
    def post(self, lobby_id):
        """Class Method used for POST request for game lobby data.

        Args:
            lobby_id: Id of the lobby we want to trieve data from.

        Return:
            success message, if the game lobby exists, is not full and player is not part of it
            error message, if is full, player is part of it or doesn't exists

        """
        # Checking if lobby exists
        #: Object of type LobbyModel: Used with SQLAlchemy for access and manipulation of obj. in DB
        lobby = LobbyModel.findById(lobby_id)
        if lobby is None:
            return { 'message': 'Lobby does not exists!'}

        if(lobby.lobbySize == 3):
            return {'message': 'Lobby is full'}
        # Adding player to the lobby
        #: str : retrieves the playerName from the current jwt token 
        playerName = current_identity.playerName
        #: Object of type PlayerModel: Used with SQLAlchemy to access and manipulate the obj. in the DB
        player = PlayerModel.findByPlayerName(playerName)
        if(player.currentLobby == lobby_id):
            return {'message': 'You are already part of the lobby!'}
        elif(player.currentLobby != -1):
            return {'message': 'You are part of a different lobby!'}
    
        # sets playes lobbyId to the one he joined
        player.currentLobby = lobby.lobbyId
        # Increases lobby size to account new player
        lobby.lobbySize = lobby.lobbySize + 1
        lobby.save_to_db()
        # Create a home for new player
        home = LocationModel(player.playerName, 'home')
        home.save_to_db()

        player.locationId = home.id
        player.homeId = home.id


        player.save_to_db()
        
        
        return {'message': 'You have succesfully joined the lobby!'}
    

    @jwt_required()
    def delete(self, lobby_id):
        """Class Method used for DELETE request for game lobby data.

        Args:
            lobby_id: Id of the lobby we want to trieve data from.

        Return:
            success message, if game lobby is deleted succesfully
            error message, if an un-authorized user tries to delete the game lobby

        """
        playerName = current_identity.playerName
        lobby = LobbyModel.findById(lobby_id)
        players = lobby.players.all()

        # Will check if you are the owner of the lobby you are trying to delete.
        if(lobby.lobbyOwner == playerName):
            for player in players:
                player.currentLobby = -1
                player.homeId = -1
                player.locationId = -1
                player.save_to_db()

            lobby.delete_from_db()
            return {'message': 'Lobby has been deleted!'}
        return {'message': 'You cannot delete the lobby!'}


    




    
