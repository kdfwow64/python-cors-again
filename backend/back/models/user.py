from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from models.user_group import UserGroupModel
from models.role import RoleModel
import json

SECRET_KEY = 'jose'

class UserModel(db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80))
  password = db.Column(db.String(280))
  email = db.Column(db.String(80))
  phone_number = db.Column(db.String(80))
  user_group = db.Column(db.Integer, db.ForeignKey('user_group.id'))
  #user_group_relation = db.relationship('UserGroupModel')
  
  def __init__(self, username, **data):
    self.username = username
    self.hash_password(data.get("password"))
    self.email = data.get("email")
    self.phone_number = data.get("phone_number")

    user_group_param = data.get("user_group")
    #user_group = UserGroupModel.find_by_id(user_group_param)
    if user_group_param:
      self.user_group = user_group_param
  
  def json(self):
    user_group = UserGroupModel.find_by_id(self.user_group)
    return {'username': self.username, 
            'id': self.id, 
            'password': self.password,
            'email': self.email,
            'phone_number': self.phone_number,
            'user_group': user_group.json() if user_group else None,
            }
    
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def find_all(cls):
    return cls.query.all()

  @classmethod
  def find_by_username(cls, username):
    return cls.query.filter_by(username=username).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  @classmethod
  def find_by_id(cls, _id):
    return cls.query.filter_by(id=_id).first()

  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()

  def update(self, commit=True, **kwargs):
    for attr, value in kwargs.items():
      setattr(self, attr, value)
    return commit and self.save_to_db() or self

  @classmethod
  def get_user_roles(self):
    user_group = UserGroupModel.find_by_id(self.user_group)
    return RoleModel.find_by_id(user_group.roles)

  def get_user_permissions(self):
    user_permissions = []

    if self.user_group:
      user_group = UserGroupModel.find_by_id(self.user_group)
      if user_group:
        user_roles = user_group.roles
        for role in user_roles:
          permissions = role.permissions
          user_permissions.extend(permissions)
    return user_permissions

  def hash_password(self, password):
    self.password = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(password, self.password)

  def generate_auth_token(self, expiration=86400):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps({'id': self.id})

  @staticmethod
  def verify_auth_token(token):
    s = Serializer(SECRET_KEY)
    try:
      data = s.loads(token)
    except SignatureExpired:
      return None
    except BadSignature:
      return None
    user = UserModel.find_by_id(data['id'])
    return user