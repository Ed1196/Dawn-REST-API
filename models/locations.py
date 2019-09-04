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
    players       =     db.relationship("PlayerModel",   foreign_keys='PlayerModel.locationId')

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
            'playersAtLocation' : self.playersAtLocation
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findByName(self, locationName, locationOwner):
        return cls.query.filter_by(self.locationName == locationName, self.locationOwner == locationOwner)




        
