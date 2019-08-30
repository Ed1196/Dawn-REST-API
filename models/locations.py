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

    locationId   =      db.Column(db.Integer, primary_key = True)
    locationName =      db.Column(dbString(10))
    numOfPlayers =      db.Column(db.Integer)

    playersAtLocation = db.relationship('PlayerModel', lazy='dynamic')


        
