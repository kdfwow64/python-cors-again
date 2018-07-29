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

class JobTemplateModel(db.Model):
  """
  Representation of job model in database

  """
  __tablename__ = 'job_template'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  agent_type = db.Column(db.String(50))
  parameters = db.Column(db.JSON)
  description = db.Column(db.String(300))
  compliance_element = db.relationship('ComplianceElementModel')
  compliance_element_id = db.Column(db.Integer, db.ForeignKey('compliance_element.id', ondelete='CASCADE'))
  compliance_id = db.Column(db.Integer)
  
  def __init__(self, **data):
    self.name = data.get('name')
    self.agent_type = data.get('agent_type')
    self.parameters = data.get('parameters', {})
    self.description = data.get('description')
    self.compliance_element_id = data.get('compliance_element_id')
    
  def json(self):
    """
    return a json representation of data presented in the database

    """
    return {'id': self.id,
            'name': self.name,
            'agent_type': self.agent_type,
            'parameters' :self.parameters,
            'description': self.description,
            'compliance_element_id': self.compliance_element_id,
           }

  @classmethod
  def findById(cls, jobId):
    return cls.query.filter_by(id=jobId).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

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
