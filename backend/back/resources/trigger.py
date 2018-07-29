from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.trigger import TriggerModel
import json
from datetime import datetime
import ast
from resources.auth import requires_permission

class Trigger(Resource):
    
  @requires_permission('get_trigger')
  def get(self, id=None):    
    queryData = request.args.to_dict()
    if id:
      trigger = TriggerModel.find_by_id(id)
      if trigger: return trigger.json(), 200
      else: return {'error': 'trigger not found'}, 404
    triggers = TriggerModel.find(**queryData)
    return {'triggers': list(map(lambda x: x.json(), triggers))}, 200

  @requires_permission('add_trigger')  
  def post(self, **somedata):
    data = json.loads(request.data)
    trigger = TriggerModel(**data)
    try:
      trigger.save_to_db(commit=True)
    except:
      return {"error": "An error occurred inserting the trigger."}, 500
    return trigger.json(), 201

  @requires_permission('delete_trigger')  
  def delete(self, id): 
    trigger = TriggerModel.find_by_id(id)
    if trigger:
      trigger.delete_from_db()
    else: 
      return {'error': 'Trigger not found'}, 404
    return {'success': 'trigger deleted'}, 202

  @requires_permission('update_trigger')  
  def put(self, id):
    data = json.loads(request.data)
    trigger = TriggerModel.find_by_id(id) 
    if trigger:
      trigger.update(**data)
    else: 
      return {'error': 'Trigger not found'}, 404
    return trigger.json(), 201

  