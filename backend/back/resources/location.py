from flask_restful import Resource, reqparse, request
from models.location import LocationModel
import json

class Location(Resource):
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:
      location = LocationModel.find_by_name(name)
      if location:
        return location.json(), 200
      else:
        return {'error': 'location not found'}, 404
    locations = LocationModel.find(**queryData)
    return {'locations': list(map(lambda x: x.json(), locations))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    if LocationModel.find_by_name(name):
      return {'error': "A location with name '{}' already exists.".format(name)}, 400
    location = LocationModel(**data)
    try:
      location.save_to_db()
    except:
      return {"error": "An error occurred creating the location."}, 500
    return location.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    location = LocationModel.find_by_name(name)
    if location:
      location.update(**data)
    else:
      return {'error': 'Location not found'}, 404
    location.save_to_db(commit=True)
    return location.json(), 201

  def delete(self, name):
    location = LocationModel.find_by_name(name)
    if location:
      location.delete_from_db()
    else:
      return {'error': 'Location not found'}, 404
    return {'success': 'location deleted'}, 202

class LocationList(Resource):
  def get(self):
    return {'locations': list(map(lambda x: x.json(), LocationModel.query.all()))}, 200

class Deviceinlocation(Resource):
  def get(self, name):
    location = LocationModel.find_by_name(name)
    if location:
      return location.deviceinlocation()

class Childinlocation(Resource):
  def get(self, name):
    location = LocationModel.find_by_name(name)
    if location:
      return location.childinlocation()