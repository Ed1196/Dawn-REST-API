from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required 
from security import authenticate, identity
from datetime import timedelta
from resources.player import PlayerRegister, Player
from resources.lobby   import CreateLobby, Lobby

# app will have the value "app.py"
app = Flask(__name__)

#Allow us to add resources for our Restfult_API
api = Api(app)

# Key that will help with decryption
app.secret_key = 'Edwin'

# Lets SQLALCHEMY know where to locate the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 

# Disabled, but it's purpose is to track modification of objects and emit signals.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# If Flask-JWT raises an error, then the Flask app will not see the error, unless this is true
app.config['PROPAGATE_EXCEPTIONS'] = True

#config JWT to expire within hald an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds = 1800)

#config JWT auth key name to be 'email' instead of default 'username'
app.config['JWT_AUTH_USERNAME_KEY'] = 'playerName'

# config JWT auth password key will change from default 'password' to 'secretKey'
app.config['JWT_AUTH_PASSWORD_KEY'] = 'secretKey'


#JWT: Will create a new endpoint
    #we send JWT a user name and a password
        #then it will call the authenticate method
        #if authentication is good, a JWT token will be sent back and stored in jwt
    #JWT will only use the identity_function when it sends a JWT token
jwt = JWT(app, authenticate, identity) # /auth, /login after 'JWT_AUTH_URL_RULE'


@app.route("/", methods=['GET'])
def homePage():
    return "Dawn's API, nothing to see here"

# Specify what fields to returb after succesful auth
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
        'authorization' : access_token.decode('utf-8'),
        'playerId': identity.id
    })

# With this flask decorator will run the method below it before the first request
# db.create_all() will create all the tables in the database
@app.before_first_request
def create_tables():
    db.create_all()

# This line of code makes the resource accesible to the API
api.add_resource(PlayerRegister, '/player-register')
api.add_resource(Player, '/player/<string:playerName>')

api.add_resource(CreateLobby, '/create-lobby')
api.add_resource(Lobby, '/lobby/<int:lobby_id>')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug =True)



