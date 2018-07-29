from db import db
#from models.workflow_composition import WorkflowCompositionModel

class EvalModel(db.Model):
  __tablename__ = 'eval'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  rules = db.Column(db.JSON)
  status = db.Column(db.String(30))
  workflow_id = db.Column(db.Integer)
  compliance_id = db.Column(db.Integer)
  workflow_composition_relation = db.relationship('WorkflowCompositionModel')
  
  def __init__(self, **data):
    self.name = data.get("name")
    self.rules = data.get("rules")
    self.status = data.get('status')
    self.workflow_id = data.get('workflow_id')
    self.compliance_id = data.get('compliance_id')
    
  def json(self):
    return {
            'id': self.id,
            'name': self.name,
            'rules': self.rules,
            'status': self.status,
            'workflow_id': self.workflow_id,
            'compliance_id': self.compliance_id,
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