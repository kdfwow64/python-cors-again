from celery import Celery
from models.job import JobModel
from models.task import TaskModel
from models.workflow import WorkflowModel
from models.device import DeviceModel
from models.link import LinkModel
from models.eval import EvalModel
from models.compliance_report import ComplianceReportModel
from models.compliance_execution import ComplianceExecutionModel
from models.check import CheckModel
from models.check_result import CheckResultModel
import logging
from logging import handlers
from datetime import datetime
import configparser
import json
from kombu import Connection, Exchange, Producer
from uuid import uuid4
from models import comparison
import re

parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

RABBIT_URI = 'pyamqp://{0}:{1}@{2}'.format(parser.get('RABBITMQ_SECTION', 'USER'),
                                           parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                           parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),
                                           )

app = Celery('job_manager', broker=RABBIT_URI)
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    task_protocol=1,
)
app.conf.task_default_queue = 'job_manager'
FILE_LOG_LEVEL = logging.DEBUG
job_manager_LOG_FILE = '/opt/optima-job-manager.log'
connection = Connection(RABBIT_URI)
channel = connection.channel()
notification_exchange = Exchange("notification", type="direct")
notification_producer = Producer(exchange=notification_exchange, channel=channel, routing_key="notification")

orchestrator_exchange = Exchange("orchestrator", type="direct")
orchestrator_producer = Producer(exchange=orchestrator_exchange, channel=channel, routing_key="orchestrator")

class JobManager():
  def __init__(self, task, status):
    '''
  Object constructor
    '''
    self.task = task
    self.job = JobModel.findById(task.job_id)
    
    
  def setLogger(self):
    # Log entry format
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    syslogFormatter = logging.Formatter('{{"logger":"optima-logging", "text":"%(message)s", "workflow_id":"{}", "element_id":"{}", "element_type":"{}"}}'.format(
                                        
                                        ))
    # Logger object
    rootLogger = logging.getLogger('job_manager')
    # Logging level at logger level. Set to debug to avoid filtering logs out
    rootLogger.setLevel(logging.DEBUG)
    # Creating handler to write logs on file
    fileHandler = logging.FileHandler(job_manager_LOG_FILE)
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
   
  def ApplyChecks(self, task, check):
    count = 0
    rules_result = {}
    for rule in check.rules:
      if check.rules[rule]["type"] == "not_depend":
        comp = getattr(comparison, check.rules[rule]["operator"])
        total, match_lines = comp(task.result["configurations"]["output"].split("\r\n"), check.rules[rule]['value'])
        rules_result[rule] = match_lines
      elif check.rules[rule]["type"] == "depend":
        if rules_result[check.rules[rule]["depend_on"]] != None:
          comp = getattr(comparison, check.rules[rule]["operator"])
          total, match_lines = comp(rules_result[check.rules[rule]["depend_on"]], check.rules[rule]['value'])
          rules_result[rule] = match_lines
        else:
          total, match_lines = 0, None
          rules_result[rule] = match_lines
      count = count + total
    return count, rules_result

  def ProcessCompliance(self, status):
    compliance_execution = ComplianceExecutionModel.find_by_id(self.job.compliance_execution_id)
    check_list = CheckModel.find(**{"compliance_id": compliance_execution.compliance_id})
    device_name = DeviceModel.find_by_id(TaskModel.findById(self.task.id).device_id).name
    if status == "SUCCESSFUL":
      total = 0
      for check in check_list:
        check_result = CheckResultModel(check.id, check.name, device_name, self.task.id, self.job.compliance_execution_id, status = 'NEW', parameters = {})
        check_result.save_to_db(commit=False)
        total, result_lines = self.ApplyChecks(self.task, check)
        if total == len(check.rules):
          check_result.status = "SUCCESSFUL"
          check_result.parameters["result"] = result_lines
        else:
          check_result.status = "FAILED"
          check_result.parameters["result"] = result_lines
        check_result.commit()
    elif status == "FAILED":
      for check in check_list:
        check_result = CheckResultModel(check.id, check.name, device_name, self.task.id, self.job.compliance_execution_id, status = 'NEW', parameters = {})
        check_result.save_to_db(commit=False)
        check_result.status = "FAILED"
        check_result.commit()
    return

  def sendToQueue(self, producer, task, data):
    producer.publish({"args":[],
                      "kwargs":data,
                      "task":task,
                      "id":str(uuid4())})
    
  def send_notification_and_workflow(self, status):
    data = {"event_id":self.job.id,
            "event_type": "job",
            "column": "status",
            "value": status}
    self.sendToQueue(notification_producer, "notification", data)
    
    if self.job.workflow_id:
      data = {"element_id": self.job.id,
              "element_type": "job",
              "status": status,
              "workflow_id": self.job.workflow_id}
      self.sendToQueue(orchestrator_producer, "orchestrator", data)
      
    return
  
  def process_status(self, status):
    if status == "SUCCESSFUL":
      if self.job.compliance_execution_id:
        self.ProcessCompliance(status)
      self.task.commit()
      self.job.success_count += 1
    if status == "FAILED":
      if self.job.compliance_execution_id:
        self.ProcessCompliance(status)
      self.job.failure_count += 1
    if self.job.agent_type == "configuration_differ_postcheck":
      self.job.device_count = len(TaskModel.find(**{"job_id": self.job.id}))
    if self.job.success_count + self.job.failure_count == self.job.device_count:
      if self.job.success_count == self.job.device_count:
        self.job.status = "SUCCESSFUL"
        self.job.processing_end_time = datetime.now().strftime(DATE_FORMAT)
        self.send_notification_and_workflow("SUCCESSFUL")
        self.job.commit()
      if self.job.failure_count > 0:
        self.job.status = "FAILED"
        self.send_notification_and_workflow("FAILED")
        self.job.commit()
    return
    
@app.task(serializer='json', name='job_manager')
def JobManagerProcess(element_id, status):
  task = TaskModel.findById(element_id)
  notification_producer.publish({"args":[],
                        "kwargs":{"event_id":element_id,
                                  "event_type": "task",
                                  "column": "status",
                                  "value": status},
                        "task":"notification",
                        "id":str(uuid4().hex)})
  
  job_manager = JobManager(task, status)
  job_manager.process_status(status)      
        