#db is the linker that will search for Models and map them to the database
from db import db
import numpy as np

#We create a class Player 
#   db.Model: will tell the sqlAlchemy that this file represents a sql table with respective columns and rows
class PlayerModel(db.Model):
    """ 
    This is a class for Player Models. It will link our SQLAlchemy fields to columns and Rows in our DB  
      
    Attributes: 
        See __init__ function
        
    """
    #Here we specify the tablename, columns and rows.
    #local class variables will be mapped to the sql database
    __tablename__ = 'players'
    playerName =    db.Column(db.String(10))
    secretKey =     db.Column(db.String(10))
    id =            db.Column(db.Integer, primary_key = True)
    role =          db.Column(db.String(10))
    status =        db.Column(db.String(10))
    heldItem =      db.Column(db.String(10))
    strength =      db.Column(db.Integer)
    stamina =       db.Column(db.Integer)
    # Items foreign key: This is the relationship between item and store
    # Foreign keys will prevent linked items from being deleted.
    # Every item will be linked to a store,
    currentLobby =        db.Column(db.Integer, db.ForeignKey('lobbies.lobbyId'))
    lobby =               db.relationship('LobbyModel', foreign_keys = [currentLobby])

    homeId =              db.Column(db.Integer, db.ForeignKey('locations.id'))
    home =                db.relationship('LocationModel', foreign_keys = [homeId])

    
    # Equivalent of a join in sequel
    

    locationId =   db.Column(db.Integer, db.ForeignKey('locations.id'))    
    location =     db.relationship('LocationModel', foreign_keys = [locationId])


    # Initializes the item
    def __init__(self, playername, secretKey, role, status, heldItem, strength, stamina):
        """ __init__ for PlayerModel Objects

            Will initialize a Player ModelObject with user's playername nad secretKey
            The rest of the fields will be defualted

            Args:
                playerName   (str): Player name. 
                secretKey    (str): Key that a user will use to authenticate.
                id           (int): Integer that will auto-increment and serve as user ID
                role         (str): Civilian, killer, hero.
                status       (str); Will keep track if dead, alive, detained
                heldItem     (str): Current item help by a player/NPC
                location     (str): Represents the players current location
                strength     (int): Represents the players strength as a stat
                stamina      (int): Represents the players stamina as a stat
                currentLobby (int): Will keep track of the lobby that the player is part of   

        """
        self.playerName      = playername
        self.secretKey       = secretKey
        self.role            = role
        self.status          = status
        self.heldItem        = heldItem
        self.strength        = strength
        self.stamina         = stamina
        self.currentLobby    = -1
        self.homeId          = -1
        self.locationId      = -1 
                 
    # Will return the item as a json/dictionary
    def json(self):
        """ Will return a PlayerModel object as a JSON.

            Args:

            Return:
                Will return most of the fields from PlayerModel as a JSON object

        """
        return {
            'playerName'    : self.playerName,
            'id'            : self.id,
            'role'          : self.role,
            'status'        : self.status,
            'heldItem'      : self.heldItem,
            'strength'      : self.strength,
            'stamina'       : self.stamina,
            'currentLobby'  : self.currentLobby,
            'homeId'        : self.homeId,
            'locationId'    : self.locationId
        }

    # CREATING OR DELETING TO DATABASE

    def save_to_db(self):
        """ Will allow us to save an object of type PlayerModel to the database.

        Note:
            player1 = PlayerModel()
            player1.save_to_db()

        Args:
        Return:

        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ Will allow us to delete an object of type PlayerModel to the database.

        Note:
            player1 = PlayerModel()
            player1.delete_from_db()

        Args:
        Return:

        """
        db.session.delete(self)
        db.session.commit
               
    # FORMS OF ACCESSING THE DATABASE
    
    # return = SELECT * FROM players WHERE playerName = playerName LIMIT 1
    @classmethod
    def findByPlayerName(cls, playerName):
        """ Will allow us to find a user with the name 'playerName' and return it.
        
        Note:
            player1 = PlayerModel.findByPlayerName('Edwin')

        Args:
            playerName: Obtained from URL parameters. Holds a players name

        Return:
            WIll return one PlayerModel object from the DB who's name matches 'playerName'

        """
        return cls.query.filter_by(playerName=playerName).first()

    @classmethod
    def findByPlayerId(cls, playerId):
        """ Will allow us to find a user with the name 'playerId' and return it.
        
        Note:
            player1 = PlayerModel.findByPlayerName(1)

        Args:
            playerId: Obtained from URL parameters. Holds a players ID

        Return:
            WIll return one PlayerModel object from the DB who's name matches 'playerId'

        """
        return cls.query.filter_by(id=playerId).first()

    @classmethod
    def findAll(cls):
        """ Will allow us access all of the current users.
        
        Note:
            players = PlayerModel.findAll()

        Args:
        Return:
            Will return a list of players of PlayerModel type

        """
        return cls.query.all()

    def confront(self, target):
        print(self.playerName)
        selfPlayer = .5
        targetPlayer = .5
        players = [self.playerName, target.playerName]
        
        if(target.status == 'sleep'):
            selfPlayer = .9
            targetPlayer = .1
            probabilities = [selfPlayer, targetPlayer]
            winner = np.random.choice(players, p=probabilities)
            return winner
            
        if(self.heldItem == 'gun' and targetPlayer.heldItem == 'gun'):
            selfPlayer = .50
            targetPlayer = .50

        else:
            if(self.heldItem == 'gun' ):
                selfPlayer = .80
                targetPlayer = .20
               
            if(target.heldItem == 'gun'):
                selfPlayer = .20
                targetPlayer = .80
            

        strengthDiff = self.strength - target.strength
        print(strengthDiff)
        # self.strength is stronger
        if(strengthDiff < 0):
            if(strengthDiff <= 10 ):
                selfPlayer = selfPlayer - .1
                targetPlayer = targetPlayer + .1
            elif (strengthDiff <= 20 ):
                selfPlayer = selfPlayer - .2
                targetPlayer = targetPlayer + .2
            elif(strengthDiff <= 30 ):
                selfPlayer = selfPlayer - .3
                targetPlayer = targetPlayer + .3
            else:
                selfPlayer = selfPlayer - .4
                targetPlayer = targetPlayer + .4

        # target is stronger
        elif(strengthDiff > 0):
            abs(strengthDiff)
            if(abs(strengthDiff) <= 10 ):
                selfPlayer = selfPlayer + .1
                targetPlayer = targetPlayer - .1
            elif (abs(strengthDiff) <= 20 ):
                selfPlayer = selfPlayer + .2
                targetPlayer = targetPlayer - .2
            elif(abs(strengthDiff) <= 30 ):
                selfPlayer = selfPlayer + .3
                targetPlayer = targetPlayer - .3
            else:
                selfPlayer = selfPlayer + .4
                targetPlayer = targetPlayer - .4

        staminaDiff = self.stamina - target.stamina
        print(staminaDiff)
        # self.strength is stronger
        if(staminaDiff  < 0):
            if(staminaDiff  <= 10 ):
                selfPlayer = selfPlayer - .05
                targetPlayer = targetPlayer + .05
            elif (staminaDiff  <= 20 ):
                selfPlayer = selfPlayer - .1
                targetPlayer = targetPlayer + .1
            else:
                selfPlayer = selfPlayer - .15
                targetPlayer = targetPlayer + .15

        # target is stronger
        elif(staminaDiff  > 0):
            abs(strengthDiff)
            if(abs(staminaDiff ) <= 10 ):
                selfPlayer = selfPlayer + .05
                targetPlayer = targetPlayer - .05
            elif (abs(staminaDiff) <= 20 ):
                selfPlayer = selfPlayer + .1
                targetPlayer = targetPlayer - .1
            else:
                selfPlayer = selfPlayer + .15
                targetPlayer = targetPlayer - .15
                
        if(selfPlayer < 0 or selfPlayer > 1):
            if(selfPlayer < 0):
                selfPlayer = .05
            if(selfPlayer > 1):
                selfPlayer = .95

        if(targetPlayer < 0 or targetPlayer > 1):
            if(targetPlayer < 0):
                targetPlayer = .05
            if(targetPlayer > 1):
                targetPlayer = .95

        probabilities = [selfPlayer, targetPlayer]

        winner = np.random.choice(players, p=probabilities)
        # Testing: print('{} won! attacker: {}%   target: {}%'.format(winner, round(selfPlayer,4), round(targetPlayer,4)))
        return winner
        # Testing: return '{} won! attacker: {}%   target: {}%'.format(winner, round(selfPlayer,4), round(targetPlayer,4))




