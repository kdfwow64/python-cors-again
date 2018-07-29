from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.rule import RuleModel
import json
from datetime import datetime

class Rule(Resource):
    
  @jwt_required()
  def get(self, id=None):
    queryData = request.args.to_dict()
    if id:  
      rule = RuleModel.find_by_id(id)
      if rule: return rule.json()
      else: return {'message': 'rule not found'}, 404
    rules = RuleModel.find(**queryData)
    return {'rules': list(map(lambda x: x.json(), rules))}

  @jwt_required()  
  def post(self, id):
    data = json.loads(request.data)    
    if RuleModel.find_by_id(id):
      return {'message': "A rule with id : {}, already exists.".format(id)}, 400
    rule = RuleModel(**data)
    try:
      rule.save_to_db(commit=True)
    except:
      return {"message": "An error occurred inserting the rule."}, 500
    return rule.json(), 201

  @jwt_required()  
  def delete(self, id):
    rule = RuleModel.find_by_id(id)
    if rule:
      rule.delete_from_db()
    return {'message': 'rule deleted'}

  @jwt_required()  
  def put(self, id):
    data = json.loads(request.data)
    rule = RuleModel.find_by_id(id)    
    #else:
    #   rule = RuleModel(**data)     
    rule.last_update_time = datetime.now().isoformat()
    rule.save_to_db(commit=True)
    return rule.json()

