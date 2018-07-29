from db import db
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class TaskModel(db.Model):
  __tablename__ = 'task'
  id = db.Column(db.Integer, primary_key=True)
  job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
  device_id = db.Column(db.Integer, db.ForeignKey('devices.id', ondelete='CASCADE'))
  status = db.Column(db.String(80))
  parameters = db.Column(db.JSON)
  insertion_time = db.Column(db.DateTime, default=datetime.now)
  last_update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  result = db.Column(db.JSON)
  processing_start_time = db.Column(db.DateTime, default=datetime.now)
  processing_end_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
  changed = db.Column(db.Boolean)
  
  def __init__(self, job_id, device_id, status = 'NEW', parameters = {}):
    self.job_id = job_id
    self.device_id = device_id
    self.status = status
    self.parameters = parameters
    # FNO: Add insertion and last update date in parameters ?
    self.insertion_time = None
    self.last_update_time = None
    self.processing_start_time = None
    self.processing_end_time = None
    self.result = {}
    self.changed = False
    
  def json(self):
    if (self.processing_start_time):
        processingStartTime = self.processing_start_time.strftime(DATE_FORMAT)
    else : 
        processingStartTime = None 
    if (self.processing_end_time): 
        processingEndTime = self.processing_end_time.strftime(DATE_FORMAT)
    else : 
        processingEndTime = None 
    return {'id': self.id,
            'job_id':self.job_id,
            'device_id': self.device_id,
            'status': self.status,
            'parameters': self.parameters,
            'insertion_time': self.insertion_time.strftime(DATE_FORMAT),
            'last_update_time': self.last_update_time.strftime(DATE_FORMAT),
            'result':self.result,
            'processing_start_time': processingStartTime,
            'processing_end_time': processingEndTime,
            'changed' : self.changed
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
