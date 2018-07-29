import sys
sys.path.insert(0, '/opt/optima/backend/back/')
from kombu import Connection, Exchange, Producer, Queue
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from db import db
from uuid import uuid4
from sqlalchemy import desc
from datetime import datetime
import configparser
from models.user import UserModel 
from models.workflow_composition import WorkflowCompositionModel
from models.compliance_execution import ComplianceExecutionModel

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

STATUS_NEW = 'NEW'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_SCH = '%d %B %Y - %I:%M %p'

rabbit_url = "pyamqp://{0}:{1}@{2}/".format(parser.get('RABBITMQ_SECTION', 'USER'),
                                            parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                            parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),)
connection = Connection(rabbit_url)
channel = connection.channel()
exchange = Exchange("raw_jobs", type="direct")
producer = Producer(exchange=exchange, channel=channel, routing_key="raw_jobs", serializer='json')
notification_exchange = Exchange("notification", type="direct")
notification_producer = Producer(exchange=notification_exchange, channel=channel, routing_key="notification", serializer='json')

class JobModel(db.Model):
  """
  Representation of job model in database

  """
  __tablename__ = 'job'

  id = db.Column(db.Integer, primary_key=True)
  workflow_id = db.Column(db.Integer) #, db.ForeignKey('workflow.id'))
  name = db.Column(db.String(50))
  agent_type = db.Column(db.String(50))
  use_device_credentials = db.Column(db.Boolean)
  login = db.Column(db.String(200))
  password = db.Column(db.String(200))
  use_enable_password = db.Column(db.Boolean)
  enable_password = db.Column(db.String(50))
  send_date = db.Column(db.String(50))
  strict_matching = db.Column(db.Boolean)
  is_validated = db.Column(db.Boolean)
  parameters = db.Column(db.JSON)
  is_scheduled = db.Column(db.Boolean)
  schedule_time = db.Column(db.DateTime)
  is_sent = db.Column(db.Boolean)
  insertion_time = db.Column(db.DateTime, default=datetime.now)
  last_update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  status = db.Column(db.String(80))
  device_count = db.Column(db.Integer)
  description = db.Column(db.String(300))
  processing_start_time = db.Column(db.DateTime, default=datetime.now)
  processing_end_time = db.Column(db.DateTime, default=datetime.now)
  success_count = db.Column(db.Integer)
  failure_count = db.Column(db.Integer)
  workflow_composition_relation = db.relationship('WorkflowCompositionModel')
  user = db.Column(db.Integer, db.ForeignKey('user.id'))
  user_relation = db.relationship('UserModel')
  compliance_execution = db.relationship('ComplianceExecutionModel')
  compliance_execution_id = db.Column(db.Integer, db.ForeignKey('compliance_execution.id', ondelete='CASCADE'))
  
  def __init__(self, **data):
    self.workflow_id = data.get('workflow_id')
    self.name = data.get('name')
    self.agent_type = data.get('agent_type')
    self.use_device_credentials = data.get('use_device_credentials')
    self.login = data.get('login')
    self.password = data.get('password')
    self.use_enable_password = data.get('use_enable_password')
    self.enable_password = data.get('enable_password')
    self._host_list = data.get('hosts')
    #self._key_list = data.get('key_list')
    self.parameters = data.get('parameters', {})
    if data.get('schedule_time'):
      self.schedule_time = datetime.strptime(data.get('schedule_time'),DATE_FORMAT_SCH)
    else:
      self.schedule_time = None
    self.is_scheduled = data.get('is_scheduled') 
    self.is_validated = data.get('is_validated')
    self.is_sent = data.get('is_sent')
    self.insertion_time = data.get('insertion_time')
    self.last_update_time = data.get('last_update_time')
    self.status = STATUS_NEW
    if self.agent_type == "configuration_differ_postcheck":
      self.device_count = 0
    if self.agent_type == "configuration_sender" and self.parameters.get("hostsConfiguration"):
      self.device_count = len(self.parameters["hostsConfiguration"])
    elif data.get("hostsType") == 'hostList':
      self.device_count = len(data.get('hosts' , []))
    elif data.get("hostsType") == 'hostFilter':
      pass
    self.description = data.get('description')
    self.processing_start_time = None
    self.processing_end_time = None
    self.success_count = 0
    self.failure_count = 0
    self.compliance_execution_id = data.get('compliance_execution_id')
    

  def json(self):
    """
    return a json representation of data presented in the database

    """
    if (self.processing_start_time):
        processingStartTime = self.processing_start_time.strftime(DATE_FORMAT)
    else : 
        processingStartTime = None 
    if (self.processing_end_time): 
        processingEndTime = self.processing_end_time.strftime(DATE_FORMAT)
    else : 
        processingEndTime = None 
    return {'id': self.id,
            'name': self.name,
            'workflow_id': self.workflow_id,
            'use_device_credentials': self.use_device_credentials,
            'login':self.login,
            'password':self.password,
            'use_enable_password' :self.use_enable_password,
            'enable_password' :self.enable_password,
            'agent_type': self.agent_type,
            #'_host_list' :self._host_list,
            #'_key_list' :self._key_list,
            'parameters' :self.parameters,
            'schedule_time' :str(self.schedule_time),
            'is_scheduled':self.is_scheduled,
            'is_validated':self.is_validated,
            'is_sent':self.is_sent,
            'insertion_time': self.insertion_time.strftime(DATE_FORMAT),
            'last_update_time': self.last_update_time.strftime(DATE_FORMAT),
            'status': self.status,
            'device_count': self.device_count,
            'description': self.description,
            'processing_start_time': processingStartTime,
            'processing_end_time': processingEndTime,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'compliance_execution_id': self.compliance_execution_id,
           }


  @classmethod
  def findById(cls, jobId):
    return cls.query.filter_by(id=jobId).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments).order_by(desc(cls.insertion_time)))

  @classmethod
  def findOne(cls, **queryArguments):
    return cls.query.filter_by(**queryArguments).first()

  def update(self, id, param):
    job = JobModel.find_by_id(id)
    if job:
      db.update(job).values(**param)
    if param == true:
      result =self.checkValidationPermission()
      if not result:
        raise Exception("User unauthorized")
      self.SendJob(id)
  
  def updateJob(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  def sendJob(self, job_id, workflow_id = None):
      celeryTaskUuid = str(uuid4())
      producer.publish({"args":[],
                        "kwargs":{"job_id":job_id},
                        "task":"AbstractionLayer",
                        "id":celeryTaskUuid})
      notification_producer.publish({"args":[],
                        "kwargs":{"event_id":job_id,
                                  "event_type": "job",
                                  "column": "None",
                                  "value": "None"},
                        "task":"notification",
                        "id":str(uuid4())})
      return
  def sendScheduleJob(self, job, workflow_id = None):
      celeryTaskUuid = str(uuid4())   
      producer.publish({"args":[],
                        "kwargs":{"job_id":job.id},
                        "task":"AbstractionLayer",
                        "id":celeryTaskUuid})
      notification_producer.publish({"args":[],
                        "kwargs":{"event_id":job.id,
                                  "event_type": "job",
                                  "column": "None",
                                  "value": "None"},
                        "task":"notification",
                        "id":str(uuid4())})
      return

  def checkValidationPermission():
      return false
  
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: self.commit()
    
  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self, commit=True):
    db.session.delete(self)
    if commit: db.session.commit()
