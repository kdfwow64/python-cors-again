from flask_restful import Resource, reqparse, request
from models.deviceClass import DeviceClassModel
import json

class DeviceClass(Resource):
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:
      deviceClass = DeviceClassModel.find_by_name(name)
      if deviceClass:
        return deviceClass.json(), 200
      else:
        return {'error': 'deviceClass not found'}, 404
    deviceClasses = DeviceClassModel.find(**queryData)
    return {'deviceClasses': list(map(lambda x: x.json(), deviceClasses))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    if DeviceClassModel.find_by_name(name):
      return {'error': "A deviceClass with name '{}' already exists.".format(name)}, 400
    deviceClass = DeviceClassModel(**data)
    try:
      deviceClass.save_to_db()
    except:
      return {"error": "An error occurred creating the deviceClass."}, 500
    return deviceClass.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    deviceClass = DeviceClassModel.find_by_name(name)
    if deviceClass:
      deviceClass.update(**data)
    else:
      return {'error': 'deviceClass not found'}, 404
    return deviceClass.json(), 201

  def delete(self, name):
    deviceClass = DeviceClassModel.find_by_name(name)
    if deviceClass:
      deviceClass.delete_from_db()
    else:
      return {'error': 'deviceClass not found'}, 404
    return {'success': 'deviceClass deleted'}, 202

class DeviceClassList(Resource):
  def get(self):
    return {'deviceClasses': list(map(lambda x: x.json(), DeviceClassModel.query.all()))}, 201

class DeviceindeviceClass(Resource):
  def get(self, name):
    deviceClass = DeviceClassModel.find_by_name(name)
    if deviceClass:
      return deviceClass.deviceindeviceClass()

class ChildindeviceClass(Resource):
  def get(self, name):
    deviceClass = DeviceClassModel.find_by_name(name)
    if deviceClass:
      return deviceClass.childindeviceClass()