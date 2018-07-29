from db import db
from models.compliance_element import ComplianceElementModel

class CheckModel(db.Model):
  __tablename__ = 'check'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  rules = db.Column(db.JSON)
  compliance_element_id = db.Column(db.Integer, db.ForeignKey('compliance_element.id', ondelete='CASCADE'))
  compliance_element = db.relationship('ComplianceElementModel')
  compliance_id = db.Column(db.Integer)
  
  def __init__(self, **data):
    self.name = data.get("name")
    self.rules = data.get("rules")
    self.compliance_id = data.get('compliance_id')
    self.compliance_element_id = data.get('compliance_element_id')
    
  def json(self):
    return {
            'id': self.id,
            'name': self.name,
            'rules': self.rules,
            'compliance_id': self.compliance_id,
            'compliance_element_id': self.compliance_element_id,
           }

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()
  
  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: db.session.commit()
  
  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()