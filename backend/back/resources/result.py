from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
import json
from models.job import JobModel
from models.task import TaskModel
class Result(Resource):
  
  
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      result = TaskModel.findByJob_Id(id)
      if result:
        return {'result': result.json()}
      else: return {'message': 'job not found'}, 404
    results = TaskModel.find(**queryData)
    return {'result': list(map(lambda x: x.json(), results))}
    
    
    