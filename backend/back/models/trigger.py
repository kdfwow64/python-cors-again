from db import db

class TriggerModel(db.Model):
  __tablename__ = 'trigger'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  relation = db.Column(db.String(80))
  notification = db.relationship('NotificationModel')
  rules = db.Column(db.JSON)
  enabled = db.Column(db.Boolean)

  def __init__(self, **data):
    self.name = data.get('name')
    self.rules = data.get('rules')
    self.enabled = data.get('enabled')
    self.relation=data.get('relation')
    
  def json(self):
    return {'name': self.name, 
            'id': self.id,  
            'rules': self.rules, 
            'enabled': self.enabled,
            'relation': self.relation}

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

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