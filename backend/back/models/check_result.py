from db import db
from datetime import datetime
from models.device import DeviceModel
from models.task import TaskModel

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class CheckResultModel(db.Model):
  __tablename__ = 'check_result'
  id = db.Column(db.Integer, primary_key=True)
  check_id = db.Column(db.Integer, db.ForeignKey('check.id', ondelete='CASCADE'))
  task_id = db.Column(db.Integer, db.ForeignKey('task.id', ondelete='CASCADE'))
  check_name = db.Column(db.String(80))
  compliance_execution_id = db.Column(db.Integer, db.ForeignKey('compliance_execution.id', ondelete='CASCADE'))
  status = db.Column(db.String(80))
  device_name = db.Column(db.String(80))
  parameters = db.Column(db.JSON)
  
  def __init__(self, check_id, check_name, device_name, task_id, compliance_execution_id, status = 'NEW', parameters = {}):
    self.check_id = check_id
    self.task_id = task_id
    self.check_name = check_name
    self.compliance_execution_id = compliance_execution_id
    self.status = status
    self.parameters = parameters
    self.device_name = device_name
    # FNO: Add insertion and last update date in parameters ?
    
  def json(self): 
    return {'id': self.id,
            'check_id':self.check_id,
            'task_id': self.task_id,
            'status': self.status,
            'check_name': self.check_name,
            'parameters': self.parameters,
            'compliance_execution_id': self.compliance_execution_id,
            'device_name': self.device_name,
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
  def findById(cls, task_id):
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
