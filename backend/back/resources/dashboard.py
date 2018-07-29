from models.dashboard import DashboardModel
from flask_restful import request, Resource, reqparse
from flask_jwt import jwt_required

class Dashboard(Resource):
  def __init__(self):
      pass
  
  def get(self, id):
    queryData = request.args.to_dict()
    if id:
      dashboard = DashboardModel.findById(id)
      if dashboard: return dashboard.json()
      else: return {'message': 'dashboard not found'}, 404
    dashboards = DashboardModel.find(**queryData)
    return {'dashboards': list(map(lambda x: x.json(), dashboards))}