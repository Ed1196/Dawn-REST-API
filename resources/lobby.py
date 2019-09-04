from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.lobby import LobbyModel
from models.player import PlayerModel
from models.locations import LocationModel

class CreateLobby(Resource):
    """Class use to handle game lobby creation endpoints.

    Attributes:

    """
    @jwt_required()
    def post(self):
        playerName = current_identity.playerName
        player     = PlayerModel.findByPlayerName(playerName)
        
        if(player.currentLobby == -1):
            newLobby = LobbyModel(player.playerName)
            home     = LocationModel(player.playerName, 'home')

            player.currentLobby = newLobby.lobbyId
            player.homeId       = home.id
            player.locationId   = home.id

            try:
                newLobby.save_to_db()
                home.save_to_db()
                player.save_to_db()
            except:
                return {'message': 'Error saving to the DB!'}

            return {'message': 'Lobby was created succesfully!'}

        return {'message': 'Lobby already exists!'}


class Lobby(Resource):
    """Class use to handle game lobby access and lobby update endpoints.

    Attributes:

    """

    def get(self,lobby_id):
        """Class Method used for GET request for game lobby data.

        Args:
            lobby_id: Id of the lobby we want to trieve data from.

        Return:
            Lobby object json, if lobby exists
            error message, if lobby does not exists

        """
        #: Object of type LobbyModel: Using SQLAlchemy this object will give
        #    us access and allow us to manipulate the lobby object in the DB
        lobby = LobbyModel.findById(lobby_id)
        if lobby is not None:
            return lobby.json()

        return {'message': 'Lobby does not exist!'}

    # Will let you join a lobby
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
    
        home = Loca
        player.currentLobby = lobby_id
        lobby.lobbySize = lobby.lobbySize + 1
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

        if(lobby.lobbyOwner == playerName):
            for player in players:
                player.currentLobby = -1
                player.save_to_db()

            lobby.delete_from_db()
            return {'message': 'Lobby has been deleted!'}
        return {'message': 'You cannot delete the lobby!'}


    




    
