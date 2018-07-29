from db import db
from models.permission import PermissionModel

roles_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')))

class RoleModel(db.Model):
  __tablename__ = 'role'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  permissions = db.relationship(
    'PermissionModel', secondary=roles_permissions,
    backref=db.backref('roles', lazy='dynamic'))
  
  def __init__(self, **data):
    self.name = data.get('name')
    if data.get('permissions'):
      self.set_permissions(data.get('permissions'))

  def json(self):
    return {'name': self.name, 
            'id': self.id, 
           }

  @classmethod
  def find_all(cls):
    return cls.query.all()

  @classmethod
  def find_by_name(cls, name):
    return cls.query.filter_by(name=name).first()

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

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
    self.permissions = []
    db.session.delete(self)
    db.session.commit()

  def get_permissions_name(self):
    permission_name = []
    for permission in self.permissions:
      permission_name.append(permission.name)
    return permission_name

  def get_permissions_id(self):
    permission_id = []
    for permission in self.permissions:
      permission_id.append(permission.id)
    return permission_id

  def set_permissions(self, data):
    self.permissions = []
    for permission in data:
      permission_obj = PermissionModel.find_by_id(permission["id"])
      if permission_obj:
        self.permissions.append(permission_obj)

  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      if attr == "permissions":
        self.set_permissions(value)
      else:
        setattr(self, attr, value)
    return commit and self.save_to_db() or self