from celery import Celery
from models.job import JobModel
from models.task import TaskModel
from models.workflow import WorkflowModel
from models.device import DeviceModel
from models.link import LinkModel
from models.eval import EvalModel
import logging
from logging import handlers
from datetime import datetime
import configparser
import json
parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

RABBIT_URI = 'pyamqp://{0}:{1}@{2}'.format(parser.get('RABBITMQ_SECTION', 'USER'),
                                           parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                           parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),
                                           )

app = Celery('orchestrator', broker=RABBIT_URI)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    task_protocol=1,
)
app.conf.task_default_queue = 'orchestrator'
FILE_LOG_LEVEL = logging.DEBUG
ORCHESTRATOR_LOG_FILE = '/opt/optima-orchestrator.log'

class Orchestrator():
  def __init__(self, element_id, workflow_id, element_type, status):
    '''
  Object constructor
    '''
    
    self.element_id = element_id
    self.workflow_id = workflow_id
    self.element_type = element_type
    self.status = status
    self.rootLogger = self.setLogger()
    
  def setLogger(self):
    # Log entry format
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    syslogFormatter = logging.Formatter('{{"logger":"optima-logging", "text":"%(message)s", "workflow_id":"{}", "element_id":"{}", "element_type":"{}"}}'.format(
                                        self.workflow_id,
                                        self.element_id,
                                        self.element_type,
                                        ))
    # Logger object
    rootLogger = logging.getLogger('orchestrator')
    # Logging level at logger level. Set to debug to avoid filtering logs out
    rootLogger.setLevel(logging.DEBUG)
    # Creating handler to write logs on file
    fileHandler = logging.FileHandler(ORCHESTRATOR_LOG_FILE)
    # Adding handler to logger
    fileHandler.setFormatter(logFormatter)
    # Setting file minimal log level for handler
    fileHandler.setLevel(FILE_LOG_LEVEL)
    # STDERR log handler creation, level configuration...
    rootLogger.handlers = []
    # Adding file handler to logger
    rootLogger.addHandler(fileHandler)
    # Appending STDERR log handler to logger
    # rootLogger.addHandler(streamHandler)
    syslogHandler = handlers.SysLogHandler('/dev/log')
    syslogHandler.setFormatter(syslogFormatter)
    fileHandler.setLevel(FILE_LOG_LEVEL)
    rootLogger.addHandler(syslogHandler)
    return rootLogger
  
  def _processTasks(self, job_id, hosts):
    '''
    '''
    resultCode, resultMessage = True, ""
    for deviceName in hosts:
      device = DeviceModel.find_by_name(deviceName)
      task = TaskModel(job_id, device.id)
      task.save_to_db(commit=True)
    return resultCode, resultMessage

  def sendJob(self, job_id, host_list):
    resultCode, resultMessage = self._processTasks(job_id, host_list)
    if not resultCode:
        return {"message": "An error occurred inserting the job. " + resultMessage}, 500
    job = JobModel.findById(job_id)
    job.sendJob(job_id)
    self.rootLogger.info('Sent to next job.'.format(job_id))

    
  def comparison(self, key, value, operation):
    if operation == "equal":
      if key == value:
        return 1
    if operation == "not equal":
      if key != value:
        return 1
    if operation == "contains":
      if value in key:
        return 1 
    if operation == "not contains":
      if not value in key:
        return 1 
    return 0
  
  def rulesatisfied(self, eval, task):
    count = 0
    for rule in eval.rules:
        try:
            result_value = task.result["configurations"][eval.rules[rule]["key"]]["output"]
        except:
            self.rootLogger.error('Key not exist')
            break
        if self.comparison(result_value, eval.rules[rule]["value"], eval.rules[rule]["operator"]) == 1:
            count += 1
        else: return 0
    return count 

  
  def evaluation(self, eval):
    total = 0
    inc = 0
    task_list = TaskModel.find(**{"job_id": self.element_id})
    for task in task_list:
        count = self.rulesatisfied(eval, task)
        if count == len(eval.rules):
          inc += 1
        if inc == len(task_list):
          return True
    return False

  def evalApplication(self, eval_id):
    eval = EvalModel.find_by_id(eval_id)
    total = self.evaluation(eval)
    if total:
      self.rootLogger.debug('Rules for the evaluation {} are satisfied'.format(eval.id))
      eval.status = "SUCCESSFUL"
            
    if not total:
      self.rootLogger.debug('Rules for the evaluation {} are not satisfied'.format(eval.id))
      eval.status = "FAILED"
    EvalModel.commit()
    return eval

  def sendEval(self, eval_id):
    """
    """
    eval = self.evalApplication(eval_id)
    links = LinkModel.find(**{"workflow_id":self.workflow_id,
                              "link_type" : eval.status,
                              })
    for link in links:
      if link.src_node["uid"] == eval.id and link.src_node["node_type"] == "eval":
        if link.dst_node["node_type"] == "job":
          next_node_type = link.dst_node["node_type"]
          next_node_id = link.dst_node["uid"]
          next_node_type = link.dst_node["node_type"] 
          workflow = WorkflowModel.findById(self.workflow_id)
          self.sendNode(next_node_id, next_node_type, workflow.hosts["host_list"])
    return

  def manualAction(self, node_id, workflow_id, element_type, status):
    self.sendToNextNode(node_id, workflow_id, element_type, status)
    return

  def sendNode(self, node_id, type, host_list = []):
    if type == "job":
      self.sendJob(node_id, host_list)
    if type == "eval":
      self.sendEval(node_id)
    if type == "manual action":
      self.manualAction(node_id)
    return
      
  def sendToNextNode(self, element_id, workflow_id, element_type, status):
    workflow = WorkflowModel.findById(workflow_id)
    links = LinkModel.find(**{"workflow_id":workflow_id,
                              "link_type" : status,})
    if element_type == "job":
      self.rootLogger.debug('Searching for the next node for the job {0}.'.format(element_id))
      for link in links:
        if link.src_node["uid"] == element_id and link.src_node["node_type"] == element_type and link.link_type == status:
          next_node_id = link.dst_node["uid"]
          next_node_type = link.dst_node["node_type"]
        
          if link.dst_node["uid"] == "success":
            self.rootLogger.info('Setting the job on SUCCESSFUL.')
            workflow.status = "SUCCESSFUL"
            return
        
          if link.dst_node["uid"] == "fail":
            self.rootLogger.info('Setting the job on FAILED.')
            workflow.status = "FAILED"
            return
        
          if link.dst_node["node_type"] == "job": 
            self.sendNode(next_node_id, next_node_type, workflow.hosts["host_list"])
          
          if link.dst_node["node_type"] == "eval":
            self.sendNode(next_node_id, next_node_type)
            
          if link.dst_node == "manual action":
            return
          self.rootLogger.info('Sending to next node')
    
    if element_type == "manual action":
      self.manualAction(element_id, workflow_id, element_type, status)
      self.rootLogger.info('The workflow is waiting for a manual action from the user.')
      return
  
    if element_type == "eval":
      return
    return
    
@app.task(serializer='json', name='orchestrator')
def orchestatorProcess(element_id, workflow_id, element_type, status):
  orchestrator = Orchestrator(element_id, workflow_id, element_type, status)
  orchestrator.sendToNextNode(element_id, workflow_id, element_type, status)      
        