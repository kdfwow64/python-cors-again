from db import db
#from models.job import JobModel
from models.workflow import WorkflowModel
from models.link import LinkModel
from models.eval import EvalModel

class WorkflowCompositionModel(db.Model):
  __tablename__ = 'workflow_composition'
  id = db.Column(db.Integer, primary_key=True)
  job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
  job_relation = db.relationship('JobModel')
  workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id', ondelete='CASCADE'))
  workflow_relation = db.relationship('WorkflowModel')
  node_type = db.Column(db.String(80))
  link_id = db.Column(db.Integer, db.ForeignKey('link.id', ondelete='CASCADE'))
  link_relation = db.relationship('LinkModel')
  eval_id = db.Column(db.Integer, db.ForeignKey('eval.id', ondelete='CASCADE'))
  eval_relation = db.relationship('EvalModel')
  
  def __init__(self, **data):
    self.job_id = data.get('job_id')
    self.workflow_id = data.get('workflow_id')
    self.node_type = data.get('node_type')
    self.link_id = data.get('link_id')
    self.eval_id = data.get('eval_id')
  def json(self):
    return {'id': self.id,
            'job_id':self.job_id,
            'workflow_id': self.workflow_id,
            'node_type': self.node_type,
            'link_id': self.link_id,
            'eval_id': self.eval_id,
            }

        
  @classmethod
  def find_by_node_id(cls, id):
    return cls.query.filter_by(node_id=id).first()

  @classmethod
  def find_by_workflow_id(cls, id):
    return cls.query.filter_by(workflow_id=id).first()

  @classmethod
  def findById(cls, _id):
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  def save_to_db(self):
    db.session.add(self)
    self.commit()

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
