# Secure way to compare strings
from werkzeug.security import safe_str_cmp

# Use player model to auth users
from models.player import PlayerModel

# Function that will be called by the /auth endpoint.
def authenticate(playername, secretKey):
    player = PlayerModel.findByPlayerName(playername)
    if player and safe_str_cmp(secretKey, player.secretKey):
        return player

# Any function that has a @jwt_required will use the identity function
def identity(payload):
        user_id = payload['identity']
        return PlayerModel.findByPlayerId(user_id)