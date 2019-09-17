from db import db

class LocationModel(db.Model):
    """
    This is a class used to model the different locations in the game. This class
    will use SQLAlchemy via the db import to map our model to columns and rows in 
    our DB. Objects created with this class will be able to update and delete themselves.
    Containes class functions that will allow us to create and retrieve location data and
    make objects out of them.

    Attributes:

    """

    __tablename__ = "locations"

    id   =              db.Column(db.Integer, primary_key = True)
    locationName  =     db.Column(db.String(10))
    locationOwner =     db.Column(db.String(10))
    numOfPlayers  =     db.Column(db.Integer)

    home          =     db.relationship("PlayerModel",   foreign_keys='PlayerModel.homeId')
    players       =     db.relationship("PlayerModel",   foreign_keys='PlayerModel.locationId', lazy='dynamic')

    def __init__(self, locationOwner, locationName):
        """ Will initialize a location object using all the fields from the LocationModel

            Note:
                Created via location = LocationModel(Owner)
            Arguments:
                locationOwner (str): Comes from the Body of the request
                locationName  (str): Comes from the Body if the request
        """
        self.locationName   = locationName
        self.locationOwner  = locationOwner
        self.numOfPlayers   = 1

    def json(self):
        """ Returns a LocationModel object as a json that can be returned

            Args:
            Return:
                Will return a json object
        """
        return {
            'locationId'        : self.id,
            'locationName'      : self.locationName,
            'locationOwner'     : self.locationOwner,
            'numOfPlayers'      : self.numOfPlayers,
            'players'           : [player.json() for player in self.players.all()]
        }

    

    def save_to_db(self):
        """ Will allow us to commit the changes of the changing object to the DB.

        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ Deletes an object from the DB

        """
        db.session.delete(self)
        db.session.commit()


    @classmethod
    def findByName(cls, locationName, locationOwner):
        """ Allows us to find a location via locationName and Ownership

            Arguments:
                locationName: Name of the location we are looking for. 
                locationOwner: Name of the owner of the location.

        """
        return cls.query.filter_by(locationName == locationName,locationOwner == locationOwner)

    @classmethod
    def findById(cls,location_id):
        """ Allows us to find a location via locationId. This id will be provided via a URL parameter.

            Arguments:
                locationId: Id of a location
        """
        return cls.query.filter_by(id=location_id).first()




        
