from flask_restful import Resource, reqparse, request
from models.workflow import WorkflowModel
from models.job import JobModel
from models.device import DeviceModel
from models.link import LinkModel
from models.eval import EvalModel
from models.task import TaskModel
from models.workflow_composition import WorkflowCompositionModel
import json
from datetime import datetime, timedelta
import threading
from cryptography.fernet import Fernet
from resources.auth import requires_permission

KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="
cipher_suite = Fernet(KEY)

class Workflow(Resource):
  def __init__(self):
    '''
    '''
    self.first_job = None
    self.workflow = None
    self.elements = {}
    self._hosts = []
    self.data = {}
    
  @requires_permission('get_workflow')
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      workflow = WorkflowModel.findById(id)
      if workflow: return workflow.json(), 200
      else: return {'error': 'workflow not found'}, 404
    workflow = WorkflowModel.find(**queryData)
    return {'workflows': list(map(lambda x: x.json(), workflow))}, 200

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
    #self.job.device_count = len(self._hosts)
    return resultCode, resultMessage
    
  def _processDeviceFilterList(self, filterList):
    '''
    '''
    for filter in filterList:
      resultCode, resultMessage = self.getList(filter)
    # resultCode, resultMessage = True, ""
    return resultCode, resultMessage

  def _processDeviceList(self, deviceList):
    '''
    '''
    resultCode, resultMessage = True, ""
    for device_name in deviceList:      
      device = DeviceModel.find_by_name(device_name)
      if not device: 
        device = DeviceModel(device_name, deviceClass=1)
        try:
          device.save_to_db(commit=True)
        except:
          resultCode, resultMessage = False, "An error occurred inserting the device."
      self._hosts.append(device)
    return resultCode, resultMessage

  def _processHosts(self, hostType, hosts):
    resultCode, resultMessage = [True, '']
    if hostType == 'hostFilter':
        resultCode, resultMessage = self._processDeviceFilterList(hosts)
    elif hostType == 'hostList':
        resultCode, resultMessage = self._processDeviceList(hosts)
    return resultCode, resultMessage

  def _processTasks(self, job):
    '''
    '''
    resultCode, resultMessage = True, ""
    for device in self._hosts:
      task = TaskModel(job.id, device.id, "NEW", {})
      task.save_to_db(commit=False)
    return resultCode, resultMessage

  def sendFirstJob(self, job):    
    data = self.data
    resultCode, resultMessage = self._processHosts(data["hosts"]['hostsType'], data["hosts"]['host_list'])
    if not resultCode:
        return {"error": "An error occurred inserting the job. " + resultMessage}, 500
    resultCode, resultMessage = self._processTasks(job)
    if not resultCode:
        return {"error": "An error occurred inserting the job. " + resultMessage}, 500
    job.sendJob(job.id)

  def saveJobToDb(self, link, data, workflow_id):
    if link["uid"] in self.elements:
      node_id = link["uid"]
      link["uid"] = self.elements[link["uid"]]
    if link["uid"] == "success" or link["uid"] == "fail":
      return link
    else:
      if link["node_type"] == "job": 
        for job_node in data["job_list"]:
          if job_node == link["uid"]:
            if data["job_list"][job_node]["agent_type"] == "configuration_differ_postcheck" and "job" in data["job_list"][job_node]["parameters"]["jobID"]:
              try:
                data["job_list"][job_node]["parameters"]["jobID"] = self.elements[data["job_list"][job_node]["parameters"]["jobID"]]
              except:
                data["job_list"][job_node]["parameters"]["jobID"] = None
            if data["job_list"][job_node].get('login'):
              data["job_list"][job_node]['login'] = cipher_suite.encrypt(data["job_list"][job_node].get('login').encode('ascii')).decode('ascii')
            if data["job_list"][job_node].get('password'):
              data["job_list"][job_node]['password'] = cipher_suite.encrypt(data["job_list"][job_node].get('password').encode('ascii')).decode('ascii')
            job = JobModel(**data["job_list"][job_node])
            job.workflow_id = workflow_id
            try:
              job.save_to_db(commit=True)
            except:
              return {"error": "An error occurred creating the job."}, 500
            self.elements.update({'{}'.format(link["uid"]) : job.id})
            if link["uid"] == data["start"]:
              first_job = data["job_list"][job_node]
            link["uid"] = job.id
      elif link["node_type"] == "eval":
        for eval_node in data["eval_list"]:
          if eval_node == link["uid"]:
            eval = EvalModel(**data["eval_list"][eval_node])
            eval.workflow_id = workflow_id
            try:
              eval.save_to_db(commit=True)
            except:
              return {"error": "An error occurred creating the evaluation."}, 500
            self.elements.update({'{}'.format(link["uid"]) : eval.id})
            node_id = eval.id
            link["uid"] = eval.id
    return link
  
  def processLink(self, links, data, workflow_id):
    link_node = None
    for link in links:
      links[link]["src_node"] = self.saveJobToDb(links[link]["src_node"], data, workflow_id)
      links[link]["dst_node"] = self.saveJobToDb(links[link]["dst_node"], data, workflow_id)
      links[link]["link_type"] = links[link]["link_type"]
      links[link]["workflow_id"] = workflow_id
      link_node = LinkModel(**links[link])
      try:
        link_node.save_to_db(commit=True)
      except:
        return {"error": "An error occurred inserting the link."}, 500
    return link_node
    
  def sendScheduleJob(self):
    try:
      self.first_job.sendScheduleJob(self.first_job.id)
    except:
      self.sendFirstJob(JobModel.findById(self.elements[self.data["start"]]))
    return
  
  def scheduleJob(self):
    now = datetime.now()
    run_at = datetime.strptime(str(self.workflow.schedule_time), '%Y-%m-%d %H:%M:%S')
    delay = (run_at - now).total_seconds()
    threading.Timer(int(delay), self.sendScheduleJob).start()
    return

  def validate_and_send_workflow(self, validation):
    if validation == True:
      if self.workflow.is_scheduled == True:
        self.first_job = JobModel.findById(self.elements[self.data["start"]])
        data = self.data
        resultCode, resultMessage = self._processHosts(data["hosts"]['hostsType'], data["hosts"]['host_list'])
        if not resultCode:
          return {"error": "An error occurred inserting the job. " + resultMessage}, 500
        resultCode, resultMessage = self._processTasks(self.first_job)
        if not resultCode:
          return {"error": "An error occurred inserting the job. " + resultMessage}, 500
        self.scheduleJob()
      else:
        self.sendFirstJob(JobModel.findById(self.elements[self.data["start"]]))
      return True
    return False

  @requires_permission('add_workflow')  
  def post(self, **somedata):
    data = json.loads(request.data)
    if data.get('login'):
      data['login'] = cipher_suite.encrypt(data.get('login').encode('ascii')).decode('ascii')
    if data.get('password'):
      data['password'] = cipher_suite.encrypt(data.get('password').encode('ascii')).decode('ascii')
    self.data = data
    self.workflow = WorkflowModel(**data)
    try:
      self.workflow.save_to_db()
    except:
      return {"error": "An error occurred inserting the workflow."}, 500
    link = self.processLink(data["link_list"], data, self.workflow.id)
    try:
      workflow_composition_src = WorkflowCompositionModel(**{"workflow_id": self.workflow.id, 
                                                           "link_id": link.id, 
                                                           "{}_id".format(link.src_node["node_type"]): int(link.src_node["uid"]), 
                                                           "node_type": link.src_node["node_type"] })
    
      workflow_composition_dst = WorkflowCompositionModel(**{"workflow_id": self.workflow.id, 
                                                           "link_id": link.id, 
                                                           "{}_id".format(link.dst_node["node_type"]): int(link.dst_node["uid"]), 
                                                           "node_type": link.dst_node["node_type"] })
    except:
      workflow_composition_src = WorkflowCompositionModel(**{"workflow_id": self.workflow.id, 
                                                           })
    
      workflow_composition_dst = WorkflowCompositionModel(**{"workflow_id": self.workflow.id, 
                                                           })  
    workflow_composition_src.save_to_db()
    workflow_composition_dst.save_to_db()
    start_job = data["start"]
    #try:
    self.validate_and_send_workflow(self.workflow.is_validated)
    TaskModel.commit()
    #self.sendFirstJob(JobModel.findById(self.elements[self.data["start"]]))
    #except:
     # pass
    #except:
    #return {"message": "An error occurred creating the workflow."}, 500
    return self.workflow.json(), 201

  @requires_permission('update_workflow')  
  def put(self, id):
    return

  @requires_permission('delete_workflow')  
  def delete(self, id):
    workflow = WorkflowModel.findById(id)
    if workflow:
      workflow.delete_from_db()
    else:
      return {'error': 'Workflow not found'}, 404
    return {'success': 'Workflow deleted'}, 202
