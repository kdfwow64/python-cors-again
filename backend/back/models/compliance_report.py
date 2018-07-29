from db import db
from datetime import datetime

class ComplianceReportModel(db.Model):
  __tablename__ = 'compliance_report'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  description = db.Column(db.String(200))
  login = db.Column(db.String(200))
  password = db.Column(db.String(200))
  use_enable_password = db.Column(db.Boolean)
  enable_password = db.Column(db.String(50))
  enable_password = db.Column(db.String(50))
  hostsType = db.Column(db.String(50))
  use_device_credentials = db.Column(db.String(50))
  is_validated = db.Column(db.Boolean)
  host_list = db.Column(db.JSON)
  creation_time = db.Column(db.DateTime, default=datetime.now)
  
  def __init__(self, **data):
    self.name = data.get('name')
    self.host_list = data.get('host_list')
    self.login = data.get('login')
    self.password = data.get('password')
    self.use_enable_password = data.get('use_enable_password')
    self.enable_password = data.get('enable_password')
    self.is_validated = data.get('is_validated')
    self.use_device_credentials = data.get('use_device_credentials')
    self.hostsType = data.get('hostsType')
    self.creation_time = data.get('creation_time')
    self.description = data.get('description')
    
  def json(self):
    return {'name': self.name, 
            'id': self.id,  
            'host_list': self.host_list,
            'login': self.login,
            'password': self.password,
            'use_enable_password': self.use_enable_password,
            'enable_password': self.enable_password,
            'is_validated': self.is_validated,
            'hostsType': self.hostsType,
            'use_device_credentials': self.use_device_credentials,
            'creation_time': str(self.creation_time),
            'description': self.description,
            }

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  @classmethod
  def findOne(cls, **queryArguments):
    return cls.query.filter_by(**queryArguments).first()

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

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()