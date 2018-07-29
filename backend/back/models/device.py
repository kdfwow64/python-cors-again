import sys
sys.path.insert(0, '/opt/optima/backend/back/')
from db import db
from sqlalchemy import desc
from datetime import datetime
from models.deviceClass import DeviceClassModel
from models.group import GroupModel
from models.location import LocationModel

class DeviceModel(db.Model):

  """
  the representation of the database .. device table
  """
  __tablename__ = 'devices'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  ipAddress = db.Column(db.String(15))
  category = db.Column(db.String(20))
  deviceClass = db.Column(db.Integer, db.ForeignKey('deviceClass.id', ondelete='CASCADE'))
  deviceClass_relation = db.relationship('DeviceClassModel')
  group = db.Column(db.Integer, db.ForeignKey('group.id', ondelete='CASCADE'))
  group_relation = db.relationship('GroupModel')
  location = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='CASCADE'))
  location_relation = db.relationship('LocationModel')
  SNMP_Community = db.Column(db.String(20))
  SNMP_Version = db.Column(db.String(20))
  login = db.Column(db.String(200))
  password = db.Column(db.String(200))
  use_enable_password = db.Column(db.Boolean)
  enable_pass = db.Column(db.String(80))
  insertion_time = db.Column(db.DateTime, default=datetime.now)
  last_update_time = db.Column(db.DateTime, default=datetime.now)
  
 
  def __init__(self, name, **data):
    self.name = name
    self.ipAddress = data.get('ipAddress')
    self.category = data.get('category')
    self.deviceClass = data.get('deviceClass')
    self.group = data.get('group')
    self.location = data.get('location')
    self.SNMP_Community = data.get('SNMP_Community')
    self.SNMP_Version = data.get('SNMP_Version')
    self.login = data.get('login')
    self.password = data.get('password')
    self.enable_pass = data.get('enable_pass')
    self.use_enable_password = data.get('use_enable_password')
    self.insertion_time = data.get('insertion_time')
    self.last_update_time = data.get('last_update_time')
   
  def json(self):
    """
    return a json representation of data prsented in the database
    """
    return {'id': self.id, 
            'name': self.name, 
            'ipAddress': self.ipAddress, 
            'category': self.category, 
            'deviceClass': self.deviceClass, 
            'group': self.group, 
            'location': self.location, 
            'SNMP_Community': self.SNMP_Community, 
            'SNMP_Version': self.SNMP_Version, 
            'login': self.login, 
            'password': self.password, 
            'enable_pass': self.enable_pass, 
            'insertion_time': self.insertion_time.isoformat(),
            'last_update_time': self.last_update_time.isoformat(),
            'use_enable_password': self.use_enable_password,
            }

  @classmethod
  def find_by_name(cls, devicename):
    return cls.query.filter_by(name=devicename).first()

  @classmethod
  def find_by_ipAddress(cls, ipaddress):
    return cls.query.filter_by(ipAddress=ipaddress).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
  
  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments).order_by(desc(cls.insertion_time)))

  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: self.commit()

  @classmethod
  def findById(cls, jobId):
    return cls.query.filter_by(id=jobId).first()

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()