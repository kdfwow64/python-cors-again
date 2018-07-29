from sqlalchemy.sql import select
from models.dashboardElement import DashboardElementModel
from flask_restful import request, Resource, reqparse
import json
from flask_jwt import jwt_required


class DashboardElement(Resource):
  def __init__(self):
      pass
  
  '''
  def get(self, id_):
    if id_:
      DE = DashboardElementModel.findById(id_)
      print(DE)
      return DE  
    return values
  '''
  def get(self, name):
    queryData = request.args.to_dict()
    if name:
      dashboardElement = DashboardElementModel.findByName(name)
      if not dashboardElement: return {'message': 'dashboardElement not found'}, 404
      queryResult = dashboardElement.get_values()
      result = dashboardElement.json()
      del result["query"]
      result['data']=queryResult
      return result
    dashboardElements = DashboardElementModel.find(**queryData)
    return {'dashboardElements': list(map(lambda x: x.json(), dashboardElements))}