from db import db
from datetime import datetime
from sqlalchemy import desc
import configparser

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
STATUS_NEW = 'NEW'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT_SCH = '%d %B %Y - %I:%M %p'

class WorkflowModel(db.Model):
  __tablename__ = 'workflow'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  status = db.Column(db.String(80))
  execution_time = db.Column(db.DateTime, default=datetime.now)
  insertion_time = db.Column(db.DateTime, default=datetime.now)
  use_device_credentials = db.Column(db.Boolean)
  login = db.Column(db.String(200))
  password = db.Column(db.String(200))
  use_enable_password = db.Column(db.Boolean)
  enable_password = db.Column(db.String(50))
  is_scheduled = db.Column(db.Boolean)
  schedule_time = db.Column(db.DateTime)
  is_validated = db.Column(db.Boolean)
  is_sent = db.Column(db.Boolean)
  parameters = db.Column(db.JSON)
  processing_start_time = db.Column(db.DateTime, default=datetime.now)
  processing_end_time = db.Column(db.DateTime, default=datetime.now)
  last_update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  description = db.Column(db.String(800))
  hosts = db.Column(db.JSON)
  workflow_composition_relation = db.relationship('WorkflowCompositionModel')
  
  def __init__(self, **data):
    
    self.name = data.get('name')
    self.status = data.get('status')
    self.execution_time = data.get('execution_time')
    self.is_scheduled = data.get('is_scheduled')
    if data.get('schedule_time'):
      self.schedule_time = datetime.strptime(str(data.get('schedule_time')),DATE_FORMAT_SCH)
    else:
      self.schedule_time = None
    self.is_validated = data.get('is_validated')
    self.hosts = data.get('hosts')
    self.use_device_credentials = data.get('use_device_credentials')
    self.login = data.get('login')
    self.password = data.get('password')
    self.use_enable_password = data.get('use_enable_password, False')
    self.enable_password = data.get('enable_password')
    self.processing_start_time = None
    self.processing_end_time = None
    self.is_sent = data.get('is_sent')
    self.last_update_time = data.get('last_update_time')
    self.description = data.get('description')
    self.parameters = data.get('parameters', {})
    self.hosts = data.get("hosts")


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
            'schedule_time' :str(self.schedule_time),
            'is_scheduled':self.is_scheduled,
            'is_validated':self.is_validated,
            'is_sent':self.is_sent,
            'use_device_credentials': self.use_device_credentials,
            'login':self.login,
            'password':self.password,
            'use_enable_password' :self.use_enable_password,
            'enable_password' :self.enable_password,
            'insertion_time': self.insertion_time.strftime(DATE_FORMAT),
            'last_update_time': self.last_update_time.strftime(DATE_FORMAT),
            'status': self.status,
            'description': self.description,
            'processing_start_time': processingStartTime,
            'processing_end_time': processingEndTime,
            'hosts': self.hosts,
            }

  @classmethod
  def findById(cls, workflowId):
    return cls.query.filter_by(id=workflowId).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments).order_by(desc(cls.insertion_time)))

  
  def find_by_id(cls, id):
    return cls.query.filter_by(id=id).first()

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: self.commit()

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self, commit=True):
    db.session.delete(self)
    if commit: db.session.commit()

