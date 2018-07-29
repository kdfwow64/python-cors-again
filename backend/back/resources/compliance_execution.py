from flask_restful import Resource, reqparse, request
from models.compliance_execution import ComplianceExecutionModel
from models.compliance_element import ComplianceElementModel
from models.job import JobModel
from models.compliance_report import ComplianceReportModel
from models.device import DeviceModel
from models.task import TaskModel
import json
from cryptography.fernet import Fernet

KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="

class ComplianceExecution(Resource):

  def __init__(self):
    '''
    '''
    self._hosts = []
    
  def get(self, id=None):
    queryData = request.args.to_dict()
    if id:
      compliance_execution = ComplianceExecutionModel.find_by_id(id)
      if compliance_execution:
        return compliance_execution.json(), 200
      else:
        return {'error': 'compliance_execution not found'}, 404
    compliance_executions = ComplianceExecutionModel.find(**queryData)
    return {'compliance_executions': list(map(lambda x: x.json(), compliance_executions))}, 200
  
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
    self._hosts = []
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

  def _processPostcheck(self, parameters, job):
    '''
    '''
    resultCode, resultMessage = True, ""
    precheck_id = parameters["jobID"]
    taskList = TaskModel.find(**{"job_id": precheck_id})
    job.device_count = len(taskList)
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

  def buildCommand(self, job):
    for deviceName in job.parameters["hostsConfiguration"]:
        device = DeviceModel.find_by_name(deviceName)
        if not device: 
          device = DeviceModel(deviceName, deviceClass=1)
          try:
            device.save_to_db(commit=False)
          except:
            resultCode, resultMessage = False, "An error occurred inserting the device."
        command = Environment().from_string(job.parameters["remoteCommand"]).render(job.parameters["hostsConfiguration"][deviceName])
        task = TaskModel(job.id, device.id)
        task.parameters["command"] = command
        task.save_to_db(commit=False)
    return command

  def _processTasks(self, hostsType, job):
    '''
    '''
    resultCode, resultMessage = True, ""
    for device in self._hosts:
        task = TaskModel(job.id, device.id, "NEW", {})
        task.save_to_db(commit=False)
    return resultCode, resultMessage
  
  def sendScheduleJob(self, job):
    try:
      job.sendScheduleJob(job)
    except:
      job.sendJob(job.id)
    return
  
  def scheduleJob(self, job):
    now = datetime.now()
    run_at = datetime.strptime(job.schedule_time, '%Y-%m-%d %H:%M:%S')
    delay = (run_at - now).total_seconds()
    threading.Timer(int(delay), self.sendScheduleJob).start()
    return
  
  def validate_and_send_job(self, validation, job):
    if validation == True:
      if job.is_scheduled == True:
        self.scheduleJob()
      else:
        job.sendJob(job.id)
      return True
    return False

  def post(self, name=None):
    data = json.loads(request.data)
    compliance_execution = ComplianceExecutionModel(data.get("compliance_id"))
    compliance_element_list = ComplianceElementModel.find(**{"compliance_id": data.get("compliance_id")})
    compliance = ComplianceReportModel.find_by_id(data.get("compliance_id"))
    try:
      compliance_execution.save_to_db()
    except:
      return {"error": "An error occurred creating the compliance_execution."}, 500
    for element in compliance_element_list:
      for job in element.job_templates:
        job_dict = job.json()
        del job_dict["id"]
        cipher_suite = Fernet(KEY)
        job = JobModel(**job_dict)
        job.compliance_execution_id = compliance_execution.id
        job.login = compliance.login
        job.password = compliance.password
        job.use_enable_password = compliance.use_enable_password
        job.enable_password = compliance.enable_password
        job.is_validated = compliance.is_validated
        job.use_device_credentials = compliance.use_device_credentials
        job.device_count = len(compliance.host_list)
        job.save_to_db()
        print(data.get("compliance_id"))
        print(compliance.host_list)
        resultCode, resultMessage = self._processHosts(compliance.hostsType, compliance.host_list)
        if not resultCode:
          return {"error": "An error occurred inserting the job. " + resultMessage}, 500
        resultCode, resultMessage = self._processTasks(compliance.host_list, job)
        if not resultCode:
          return {"error": "An error occurred inserting the job. " + resultMessage}, 500
        TaskModel.commit()
        JobModel.commit()
        job.sendJob(job.id)
        
        print('job sent')
        print(job.id)
        
    return compliance_execution.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    compliance_execution = ComplianceExecutionModel.find_by_name(name)
    if compliance_execution:
      compliance_execution.update(**data)
    else:
      return {'error': 'compliance_execution not found'}, 404
    compliance_execution.save_to_db(commit=True)
    return compliance_execution.json(), 201

  def delete(self, id):
    compliance_execution = ComplianceExecutionModel.find_by_id(id)
    if compliance_execution:
      compliance_execution.delete_from_db()
    else:
      return {'error': 'compliance_execution not found'}, 404
    return {'success': 'compliance_execution deleted'}, 202
