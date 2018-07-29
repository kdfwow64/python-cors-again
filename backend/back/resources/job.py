from flask_restful import request, Resource, reqparse
from flask_restful.utils import cors
from flask import jsonify
from flask_jwt import jwt_required
from models.job import *
from models.task import *
from models.device import *
from models.user import *
from flask_cors import cross_origin
import json
from jinja2 import Environment
import socket
from datetime import datetime, timedelta
import threading
from cryptography.fernet import Fernet
from resources.auth import requires_permission

KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="

class Job(Resource):

  def __init__(self):
    '''
    '''
    self.job = None
    self._hosts = []
#  @cross_origin(headers=['Content-Type','Authorization'])
  @requires_permission('get_job')   
  def get(self, id = None):
    print("HELLLOOOOO")
    queryData = request.args.to_dict()
    if id:
      job = JobModel.findById(id)
      if job: return job.json(), 200
      else: return {'error': 'job not found'}, 404
    jobs = JobModel.find(**queryData)
    print('JOBSSSS: {}'.format(jobs))
#    return {'jobs': list(map(lambda x: x.json(), jobs))}, 200
    resp = jsonify(jobs)
    return resp
  
  def getList(self, filter):
    device_list = []
    resultCode, resultMessage = True, ""
    if filter["element"] == "all" or filter["value"] == "all":
      try: 
        device_list = list(map(lambda x: x, DeviceModel.query.all()))
      except:
        resultCode, resultMessage = False, "An error occurred getting the device."
    else:
      try:  
        device_list = DeviceModel.find(**{filter["element"]: filter["value"]})
      except:
        resultCode, resultMessage = False, "An error occurred getting the device."
    if filter["device"] == "all":
      self._hosts = device_list
    for device in device_list:
      if filter["device"] in device.name:
        self._hosts.append(device)
    if len(self._hosts) == 0:
      return {"error": "Empty host list."}, 500
    self.job.device_count = len(self._hosts)
    return resultCode, resultMessage
    
  def _processDeviceFilterList(self, filterList):
    '''
    '''
    for filter in filterList:
      resultCode, resultMessage = self.getList(filter)
    # resultCode, resultMessage = True, ""
    return resultCode, resultMessage

  def validIP(self, address):
    parts = address.split(".")
    if len(parts) != 4:
      return False
    for item in parts:
      if not 0 <= int(item) <= 255:
        return False
    return True

  def _processDeviceList(self, deviceList):
    '''
    '''
    ip_addr = ""
    device_name = ""
    resultCode, resultMessage = True, ""
    for host in deviceList:
      device = DeviceModel.find_by_name(host) if DeviceModel.find_by_name(host) is not None else DeviceModel.find_by_ipAddress(host)
      if not device:
        if self.validIP(host):
          try:
            device_name = socket.getfqdn(host)
          except: 
            continue
          ip_addr = host
        else:
          device_name = host
          try:
            ip_addr = socket.gethostbyname(host)
          except:
            continue
          #except: ip_addr = host
        device = DeviceModel(name=device_name, ipAddress=ip_addr, deviceClass=1)
        try:
          device.save_to_db(commit=False)
        except:
          resultCode, resultMessage = False, "An error occurred inserting the device."
      self._hosts.append(device)
    return resultCode, resultMessage

  def _processPostcheck(self, parameters):
    '''
    '''
    resultCode, resultMessage = True, ""
    precheck_id = parameters["jobID"]
    taskList = TaskModel.find(**{"job_id": precheck_id})
    self.job.device_count = len(taskList)
    for task in taskList:
      device = DeviceModel.find_by_id(task.device_id)
      if not device: 
        resultCode, resultMessage = False, "Device not found."
      self._hosts.append(device)
    return resultCode, resultMessage

  def _processHosts(self, hostType, hosts):
    resultCode, resultMessage = [True, '']
    if hostType == 'hostFilter':
        resultCode, resultMessage = self._processDeviceFilterList(hosts)
    elif hostType == 'hostList' or hostType == 'hostsConfiguration':
        resultCode, resultMessage = self._processDeviceList(hosts)
    return resultCode, resultMessage

  def buildCommand(self):
    for deviceName in self.job.parameters["hostsConfiguration"]:
        device = DeviceModel.find_by_name(deviceName)
        if not device: 
          device = DeviceModel(deviceName, deviceClass=1)
          try:
            device.save_to_db(commit=False)
          except:
            resultCode, resultMessage = False, "An error occurred inserting the device."
        command = Environment().from_string(self.job.parameters["remoteCommand"]).render(self.job.parameters["hostsConfiguration"][deviceName])
        task = TaskModel(self.job.id, device.id)
        task.parameters["command"] = command
        task.save_to_db(commit=False)
    return command

  def _processTasks(self, hostsType):
    '''
    '''
    resultCode, resultMessage = True, ""
    if self.job.agent_type == "configuration_sender" and hostsType == "hostsConfiguration":
      self.buildCommand()
    else:
      for device in self._hosts:
        task = TaskModel(self.job.id, device.id, "NEW", {})
        task.save_to_db(commit=False)
    return resultCode, resultMessage
  
  def sendScheduleJob(self):
    try:
      self.job.sendScheduleJob(self.job)
    except:
      self.job.sendJob(self.job.id)
    return
  
  def scheduleJob(self):
    now = datetime.now()
    run_at = datetime.strptime(self.job.schedule_time, '%Y-%m-%d %H:%M:%S')
    delay = (run_at - now).total_seconds()
    threading.Timer(int(delay), self.sendScheduleJob).start()
    return
  
  def validate_and_send_job(self, validation):
    if validation == True:
      if self.job.is_scheduled == True:
        self.scheduleJob()
      else:
        self.job.sendJob(self.job.id)
      return True
    return False
  @requires_permission('add_job')
  def post(self, **uselessData):
    if uselessData: return {"error": "Id not accepted in job creation URI"}, 400
    data = json.loads(request.data)
    print(data)
    #if not data.get('hosts'):
     # return {"error": "Empty host list."}, 500
    cipher_suite = Fernet(KEY)
    if data.get('login'):
      data['login'] = cipher_suite.encrypt(data.get('login').encode('ascii')).decode('ascii')
    if data.get('password'):
      data['password'] = cipher_suite.encrypt(data.get('password').encode('ascii')).decode('ascii')
    if data.get('enable_password'):
      data['enable_password'] = cipher_suite.encrypt(data.get('enable_password').encode('ascii')).decode('ascii')
    self.job = JobModel(**data)
    try:
      self.job.save_to_db(commit=False)
    except:
      return {"error": "An error occurred inserting the job."}, 500
    if data["agent_type"] == "configuration_differ_postcheck":
      resultCode, resultMessage = self._processPostcheck(data['parameters'])
    else:
      if data["hostsType"] == "hostsConfiguration":
        resultCode, resultMessage = self._processHosts(data['hostsType'], data["parameters"]["hostsConfiguration"])
      else:
        resultCode, resultMessage = self._processHosts(data['hostsType'], data['hosts'])
    if not resultCode:
        return {"error": "An error occurred inserting the job. " + resultMessage}, 500
    resultCode, resultMessage = self._processTasks(data['hostsType'])
    if not resultCode:
        return {"error": "An error occurred inserting the job. " + resultMessage}, 500
    try:
      self.validate_and_send_job(data["is_validated"])
    except:
      pass
    TaskModel.commit()
    JobModel.commit()
    return self.job.json(), 201

  @requires_permission('delete_job')
  def delete(self, id):
    job = JobModel.findById(id)
    if job:
      job.delete_from_db()
      return {'success': 'Job deleted'}, 202
    return {'error': 'Job not found'}, 404

  @requires_permission('update_job')
  def put(self,id):
    data = json.loads(request.data)
    job = JobModel.findById(id)
    if job:
      cipher_suite = Fernet(KEY)
      if data.get('login'):
        data['login'] = cipher_suite.encrypt(data.get('login').encode('ascii')).decode('ascii')
      if data.get('password'):
        data['password'] = cipher_suite.encrypt(data.get('password').encode('ascii')).decode('ascii')
      job.updateJob(**data)
    else:
      return {'error': 'Job not found'}, 404
    return job.json(), 201

class JobList(Resource):
  @requires_permission('get_jobs')
  def get(self):
    return {'jobs': list(map(lambda x: x.json(), JobModel.query.all()))}, 200
