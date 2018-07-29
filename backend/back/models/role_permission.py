from db import db

class RolePermissionModel(db.Model):
  __tablename__ = 'role_permission'
  id = db.Column(db.Integer, primary_key=True)
  permission_id = db.Column(db.Integer, db.ForeignKey('permission.id', ondelete='CASCADE'))
  role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
  
  def __init__(self, permission_id, role_id):
    self.permission_id = permission_id
    self.role_id = role_id
   
  def json(self):
    return {'id': self.id,
            'permission_id':self.permission_id,
            'role_id': self.role_id,
            }

  @classmethod
  def update(self, id, param):
    group_permission = cls.find({"id":id})
    if group_permission:
      db.update(group_permission).values(**param)

  '''
  @classmethod
  def find_by_permission_id(cls, permission_id):
    return cls.query.filter_by(permission_id=permission_id).first()
  '''
        
  @classmethod
  def findBypermission_id(cls, id):
    return cls.query.filter_by(permission_id=id).first()

  @classmethod
  def findById(cls, group_permission_id):
    return cls.query.filter_by(id=group_permission_id).first()

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
