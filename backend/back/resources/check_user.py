from flask_restful import Resource, reqparse, request
from models.user import UserModel
import json
from flask_jwt import JWT, jwt_required

from resources.auth import requires_token


class Check_User(Resource):
  # @jwt_required()
  @requires_token()
  def get(self):
    return {'check_token': True}, 200