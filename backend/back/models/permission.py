from db import db

class PermissionModel(db.Model):

  """
  the representation of the database .. permission tbale
  
  """
  __tablename__ = 'permission'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  value = db.Column(db.String(80))
  object = db.Column(db.String(80))
  
  def __init__(self, **data):
    self.name = data.get('name')
    self.value = data.get('value')
    self.object = data.get('object')
    
   
  def json(self):
    """
    return a json representation of data prsented in the database
    """
    return {'id': self.id, 
            'name': self.name, 
            'value': self.value,
            'object': self.object,
            }

  @classmethod
  def find_all(cls):
    return cls.query.all()

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  def save_to_db(self, commit=True):
    db.session.add(self)
    if commit: self.commit()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  @staticmethod
  def commit():
    db.session.commit()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()

  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self