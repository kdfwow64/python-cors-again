from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.task import TaskModel
import json
from resources.auth import requires_permission

class Task(Resource):
    
  @requires_permission('get_tasks')  
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      task = TaskModel.findById(id)
      if task: return task.json(), 201
      else: return {'message': 'task not found'}, 404
    tasks = TaskModel.find(**queryData)
    return {'tasks': list(map(lambda x: x.json(), tasks))}, 200
