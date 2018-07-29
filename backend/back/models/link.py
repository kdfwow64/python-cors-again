from db import db
#from models.workflow_composition import WorkflowCompositionModel

class LinkModel(db.Model):
  __tablename__ = 'link'
  id = db.Column(db.Integer, primary_key=True)
  workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id', ondelete='CASCADE'))
  workflow_relation = db.relationship('WorkflowModel')
  src_node = db.Column(db.JSON)
  dst_node = db.Column(db.JSON)
  link_type = db.Column(db.String(80))
  workflow_composition_relation = db.relationship('WorkflowCompositionModel')
  
  def __init__(self, **data):
    self.workflow_id = data.get('workflow_id')
    self.src_node = data.get('src_node')
    self.dst_node = data.get('dst_node')
    self.link_type = data.get('link_type')
    
  def json(self):
    return {'workflow_id': self.workflow_id, 
            'id': self.id,
            'src_node': self.src_node,
            'dst_node': self.dst_node,
            'link_type': self.link_type,
           }

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  @classmethod
  def find_by_workflow_id(cls, workflow_id):
    return cls.query.filter_by(id=workflow_id).first()
  
  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments).order_by(desc(cls.insertion_time)))

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: db.session.commit()
  
  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()