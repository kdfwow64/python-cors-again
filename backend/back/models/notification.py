from db import db
from sqlalchemy.dialects.mysql import TEXT

class NotificationModel(db.Model):
  __tablename__ = 'notification'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  trigger_id = db.Column(db.Integer, db.ForeignKey('trigger.id', ondelete='CASCADE'))
  trigger_relation = db.relationship('TriggerModel')
  action = db.Column(db.String(80))
  command = db.Column(db.TEXT())
  url = db.Column(db.String(80))
  method = db.Column(db.String(8))
  text = db.Column(db.TEXT())
  enable = db.Column(db.Boolean)
  
  def __init__(self, **data):
    self.name = data.get("name")
    self.trigger_id = data.get("trigger_id")
    self.subscribers = data.get("subscribers")
    self.action = data.get("action")
    self.command = data.get("command")
    self.url = data.get("url")
    self.method = data.get("method")
    self.text = data.get("text")
    self.enable = data.get("enable")
  
  def json(self):
    return {'name': self.name,
            'id': self.id,
            'trigger_id': self.trigger_id,
            #'subscribers': self.subscribers,
            'action': self.action,
            'text': self.text,
            'enable': self.enable,
            'command': self.command,
            'url': self.url,
            'method': self.method,
            }
    
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_by_trigger_id(cls, id):
    return cls.query.filter_by(trigger_id=id).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
  
  @classmethod
  def findOne(cls, **queryArguments):
    return cls.query.filter_by(**queryArguments).first()
  
  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()