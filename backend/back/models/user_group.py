from db import db
from models.role import RoleModel


user_group_roles = db.Table(
    'user_group_roles',
    db.Column('user_group_id', db.Integer, db.ForeignKey('user_group.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class UserGroupModel(db.Model):
  __tablename__ = 'user_group'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  # role = db.Column(db.Integer, db.ForeignKey('role.id'))

  # roles = db.relationship('RoleModel')

  roles = db.relationship(
    'RoleModel', secondary=user_group_roles,
    backref=db.backref('user_groups', lazy='dynamic'))

  def __init__(self, **data):
    self.name = data.get('name')

    self.set_roles(data.get('roles'))

    # role_param = data.get('role')
    # role = RoleModel.find_by_id(role_param)
    # if role:
    #   self.role = role_param

  def json(self):
    return {'id': self.id,
            'name': self.name,
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
    db.session.delete(self)
    db.session.commit()

  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      if attr == "roles":
        self.set_roles(value)
      else:
        setattr(self, attr, value)
    return commit and self.save_to_db() or self

  def get_roles_id(self):
    roles_id = []
    for role in self.roles:
      roles_id.append(role.id)
    return roles_id

  def set_roles(self, data):
    self.roles = []
    for role in data:
      role_obj = RoleModel.find_by_id(role["id"])
      if role_obj:
        self.roles.append(role_obj)