from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.compliance_report import ComplianceReportModel
import json
from datetime import datetime
import ast
import threading
from cryptography.fernet import Fernet
from models.job import JobModel
from models.eval import EvalModel
from models.task import TaskModel
from models.device import DeviceModel
from models.user import UserModel
from models.job_template import JobTemplateModel
from models.check import CheckModel
from models.compliance_element import ComplianceElementModel
from resources.auth import requires_permission

KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="

class ComplianceReport(Resource):
  
  def __init__(self):
    '''
    '''
    self.job = None
    self._hosts = []
  
  @requires_permission('get_compliance_report')  
  def get(self, id=None):    
    queryData = request.args.to_dict()
    if id:
      compliance_report = ComplianceReportModel.find_by_id(id)
      if compliance_report: return compliance_report.json(), 200
      else: return {'error': 'compliance report not found'}, 404
    compliance_reports = ComplianceReportModel.find(**queryData)
    return {'compliance_reports': list(map(lambda x: x.json(), compliance_reports))}, 200
  
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
  
  def ProcessEval(self, eval_list, compliance_id):
    for eval_element in eval_list:
      eval = EvalModel(**eval_element)
      eval.compliance_id = compliance_id
      try:
        eval.save_to_db(commit=True)
        print(eval)
        print(eval.json())
      except:
        return {"error": "An error occurred creating the evaluation."}, 500
    return 
  
  def validate_and_send_job(self, validation):
    if validation == True:
      if self.job.is_scheduled == True:
        self.scheduleJob()
      else:
        self.job.sendJob(self.job.id)
      return True
    return False
  
  @requires_permission('add_compliance_report')
  def post(self, **somedata):
    data = json.loads(request.data)
    cipher_suite = Fernet(KEY)
    if data.get('login'):
      data['login'] = cipher_suite.encrypt(data.get('login').encode('ascii')).decode('ascii')
    if data.get('password'):
      data['password'] = cipher_suite.encrypt(data.get('password').encode('ascii')).decode('ascii')
    compliance_report = ComplianceReportModel(**data)
    compliance_report.save_to_db(commit=False)
    ComplianceReportModel.commit()
    for element in data["elements"]:
      compliance_element = ComplianceElementModel(compliance_report.id)
      compliance_element.save_to_db(commit=False)
      ComplianceElementModel.commit()
      job_template = JobTemplateModel(**element["job"])
      job_template.compliance_element_id = compliance_element.id
      job_template.save_to_db(commit=False)
      for check in element["checks"]:
        check = CheckModel(**element["checks"][check])
        check.compliance_element_id = compliance_element.id
        check.compliance_id = compliance_report.id
        check.save_to_db(commit=False)
    JobTemplateModel.commit()
    CheckModel.commit()
    return compliance_report.json(), 201
    """try:
      self.job.save_to_db(commit=False)
    except:
      return {"error": "An error occurred inserting the job."}, 500
    resultCode, resultMessage = self._processHosts(data["job"]['hostsType'], data["job"]['hosts'])
    if not resultCode:
        return {"error": "An error occurred inserting the job. " + resultMessage}, 500
    resultCode, resultMessage = self._processTasks(data["job"]['hostsType'])
    if not resultCode:
        return {"error": "An error occurred inserting the job. " + resultMessage}, 500
    try:
      self.validate_and_send_job(data["job"]["is_validated"])
    except:
      pass
    TaskModel.commit()
    JobModel.commit()
    compliance_report = ComplianceReportModel(data["name"], self.job.id)
    try:
      compliance_report.save_to_db(commit=True)
    except:
      return {"error": "An error occurred inserting the compliance report."}, 500
    compliance_id = compliance_report.id
    self.ProcessEval(data["eval_list"], compliance_id)
    return compliance_report.json(), 201"""
    
  @requires_permission('delete_compliance_report')
  def delete(self, id): 
    compliance_report = ComplianceReportModel.find_by_id(id)
    if compliance_report:
      compliance_report.delete_from_db()
    else:
      return {'error': 'compliance_report not found'}, 404
    return {'success': 'compliance_report deleted'}, 202
 
  @requires_permission('update_compliance_report')  
  def put(self, id):
    data = json.loads(request.data)
    compliance_report = ComplianceReportModel.find_by_id(id) 
    if compliance_report:
      compliance_report.update(**data)
    else: 
      return {'error': 'compliance_report not found'}, 404
    return compliance_report.json(), 201
