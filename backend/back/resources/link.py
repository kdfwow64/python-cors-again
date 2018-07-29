from flask_restful import Resource, reqparse, request
from models.link import LinkModel
import json

class Link(Resource):
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      link = LinkModel.find_by_id(id)
      if link: return link.json(), 200
      else: return {'error': 'link not found'}, 404
    link = LinkModel.find(**queryData)
    return {'links': list(map(lambda x: x.json(), link))}, 200

  def post(self, **somedata):
    data = json.loads(request.data)
    link = LinkModel(**data)
    try:
      link.save_to_db()
    except:
      return {"error": "An error occurred creating the link."}, 500
    return link.json(), 201

  def put(self, id):
    data = json.loads(request.data)
    link = LinkModel.find_by_id(id)
    if link:
      link.update(**data)
    else:
      return {'error': 'Group not found'}, 404
    return link.json(), 201

  def delete(self, name):
    link = LinkModel.find_by_id(id)
    if link:
      link.delete_from_db()
    else:
      return {'error': 'Group not found'}, 404
    return {'success': 'link deleted'}, 202
