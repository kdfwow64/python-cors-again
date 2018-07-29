from db import db

class RuleModel(db.Model):
  __tablename__ = 'rule'

  id = db.Column(db.Integer, primary_key=True)
  element = db.Column(db.String(80))
  column = db.Column(db.String(80))
  operation = db.Column(db.String(80))
  value = db.Column(db.String(80))

  def __init__(self, **data):
    self.element = data.get("element")
    self.column = data.get('column')
    self.operation = data.get('operation')
    self.value = data.get('value')
    
  def json(self):
    return {'element': self.element, 
            'id': self.id, 
            'column': self.column, 
            'operation': self.operation,
            'value': self.value,}

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
  
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