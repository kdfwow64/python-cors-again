from db import db
from models.job_template import JobTemplateModel

class ComplianceElementModel(db.Model):
  __tablename__ = 'compliance_element'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  compliance_id = db.Column(db.Integer)
  checks = db.relationship('CheckModel', lazy='dynamic')
  job_templates = db.relationship('JobTemplateModel', lazy='dynamic')
  
  def __init__(self, compliance_id, **data):
    self.name = data.get('name')
    self.compliance_id = compliance_id
    
  def json(self):
    return {'compliance_id': self.compliance_id, 
            'id': self.id,
            'name': self.name,
            'checks': [check.json() for check in self.checks.all()],
            'job_templates': [job_template.json() for job_template in self.job_templates.all()]
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