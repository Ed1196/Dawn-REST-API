# Will allow us to link entities/Models to the database rows/columns via SQLAlchemy
from db import db

class LobbyModel(db.Model):
    """ 
    This is a class for Lobby Models. It will link our SQLAlchemy fields to columns and Rows in our DB.
    Objects created with this class will be able to update, delete themselves.
    Class functions will allow us to retrieve data from the DB and create a LobbyModel object from them.
      
    Attributes: 
        See __init__ function
        
    """
    __tablename__ = 'lobbies'

    lobbyId =       db.Column(db.Integer, primary_key=True)
    lobbyOwner =    db.Column(db.String(10))
    lobbySize =     db.Column(db.Integer)

     # Tells sqlAlchemy that there is a relationship with ItemModel
    # It is a list of ItemModel's since there is a many to one relationship
    # between a StoreModel and an ItemModel
    # As soon as we create a store model, we will create an item that matches that store_id
    players = db.relationship('PlayerModel', lazy='dynamic')

    def __init__(self, lobbyOwner):
        """ __init__ for LobbyModel Objects

            Will initialize a Lobby Model Objects with a the players playerName as the 
            lobbyOwner of the player who created it. You will be added to the lobby as Owner
            and the size of the lobby gets set to 1.

            Args:
                lobbyOwner (str): Comes from the jwt of the current user.

        """
        self.lobbyOwner = lobbyOwner
        self.lobbySize = 1

    def json(self):
        """ Will return a LobbyModel object as a JSON.

            Note:
                Called via lobby = LobbyModel("Edwin")
                           lobby.json()

            Args:

            Return:
                Will return most of the fields from LobbyModel as a JSON object

        """
        return {
            'lobbyId'   :self.lobbyId, 
            'lobbyOwner': self.lobbyOwner, 
            'lobbySize' : self.lobbySize,
            'players': [player.json() for player in self.players.all()]
            }
    
    @classmethod
    def findById(cls, lobbyId):
        """Will find a Lobby in the lobbies table of the DB using lobbyId

            Note:
                Called via LobbyModel.findById(1)

            Args:
                lobbyId (str): Comes from the URL parameter when a request is made to an endpoint

            Return:
                Will return data for a single lobby from the DB

        """
        return cls.query.filter_by(lobbyId=lobbyId).first()

    @classmethod
    def findByOwner(cls, lobbyOwner):
        """Will find a Lobby from the lobbies table of the DB using playerName

            Args:
                lobbyOwner (str): Comes from the URL parameter when a request is made to an aendpoint

            Return:
                Will return data for a single lobby from the DB

        """
        return cls.query.filter_by(lobbyOwner=lobbyOwner).all()

    def save_to_db(self):
        """ If called by a LobbyModel object, it will save its current state to the DB
    
            Args:
            Return:
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ If called by a LobbyModel object, it will delete its current state to the DB
    
            Args:
            Return:
        """
        db.session.delete(self)
        db.session.commit()



    