from db import db
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class ComplianceExecutionModel(db.Model):
  __tablename__ = 'compliance_execution'
  id = db.Column(db.Integer, primary_key=True)
  compliance_id = db.Column(db.Integer, db.ForeignKey('compliance_report.id', ondelete='CASCADE'))
  execution_time = db.Column(db.DateTime, default=datetime.now)
  jobs = db.relationship('JobModel', lazy='dynamic')
  
  def __init__(self, compliance_id, **data):
    self.compliance_id = compliance_id
    self.execution_time = data.get('insertion_time')
    
  def json(self): 
    return {'id': self.id,
            'compliance_id':self.compliance_id,
            'jobs':[job.json() for job in self.jobs.all()],
            'execution_time': str(self.execution_time),
            }

  @classmethod
  def update(self, id, param):
    task = cls.find({"id":id})
    if task:
      db.update(task).values(**param)

  '''
  @classmethod
  def find_by_job_id(cls, job_id):
    return cls.query.filter_by(job_id=job_id).first()
  '''
        
  @classmethod
  def findByJob_Id(cls, id):
      return cls.query.filter_by(job_id=id).first()

  @classmethod
  def find_by_id(cls, task_id):
    return cls.query.filter_by(id=task_id).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  @classmethod
  def findOne(cls, **queryArguments):
    return cls.query.filter_by(**queryArguments).first()

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: self.commit()

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
