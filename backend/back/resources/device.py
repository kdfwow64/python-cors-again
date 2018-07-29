from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.device import DeviceModel
import json
from datetime import datetime
from cryptography.fernet import Fernet
from resources.auth import requires_permission

KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="

class Device(Resource):
    
  @requires_permission('get_device')  
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:  
      device = DeviceModel.find_by_name(name)
      if device: return device.json(), 200
      else: return {'error': 'device not found'}, 404
    devices = DeviceModel.find(**queryData)
    return {'devices': list(map(lambda x: x.json(), devices))}, 200

  @requires_permission('add_device')
  def post(self, name=None):
    data = json.loads(request.data)
    print(data)
    cipher_suite = Fernet(KEY)
    if data.get('login'):
      data['login'] = cipher_suite.encrypt(data.get('login').encode('ascii')).decode('ascii')
    if data.get('password'):
      data['password'] = cipher_suite.encrypt(data.get('password').encode('ascii')).decode('ascii')
    name=data.get("name",name)
    if DeviceModel.find_by_name(name):
      return {'error': "A device with name : {}, already exists.".format(name)}, 400
    device = DeviceModel(**data)
    #try:
    device.save_to_db()
    #except:
      #return {"error": "An error occurred creating the device."}, 500
    return device.json(), 201

  @requires_permission('delete_device')
  def delete(self, name):
    device = DeviceModel.find_by_name(name)
    if device:
      device.delete_from_db()
    else:
      return {'error': 'device not found'}, 404
    return {'success': 'Device deleted'}, 202

  @requires_permission('get_device')
  def put(self, name):
    data = json.loads(request.data)
    device = DeviceModel.find_by_name(name)
    if device:
      cipher_suite = Fernet(KEY)
      if data.get('login'):
        data['login'] = cipher_suite.encrypt(data.get('login').encode('ascii')).decode('ascii')
      if data.get('password'):
        data['password'] = cipher_suite.encrypt(data.get('password').encode('ascii')).decode('ascii')
      device.update(**data)
    else:
      return {'error': 'device not found'}, 404
    return device.json(), 201

class DeviceList(Resource):
  @requires_permission('get_devices')
  def get(self):
    return {
  "devices" : list(map(lambda x: x.json(), DeviceModel.query.all()))}, 200