
from db import db

class DeviceClassModel(db.Model):
  __tablename__ = 'deviceClass'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  parent_id = db.Column(db.Integer, db.ForeignKey('deviceClass.id', ondelete='CASCADE'))
  devices = db.relationship('DeviceModel')
  children = db.relationship('DeviceClassModel', lazy="dynamic")
  

  def __init__(self, name, **data):
    self.name = name
    self.parent_id = data.get('parent_id')

  def json(self):
    return {'name': self.name, 'id': self.id, 'parent_id': self.parent_id, 'subdeviceClasses': [child.json() for child in self.children.all()]}

  def deviceindeviceClass(self):
    return {'devices': [device.json() for device in self.devices.all()]}

  def childindeviceClass(self):
    return {'subdeviceClasses': [child.json() for child in self.children.all()]}

  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: self.commit()

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
