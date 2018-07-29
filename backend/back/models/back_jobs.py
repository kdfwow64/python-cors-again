from db import db

class JobModel(db.Model):

  """

  Representation of job configuration parser model in database



  """

  __tablename__ = 'job'



  id = db.Column(db.Integer, primary_key=True)

  name = db.Column(db.String(50))

  agent_type = db.Column(db.String(50))

  use_device_credentials = db.Column(db.Boolean)

  login = db.Column(db.String(80))

  password = db.Column(db.String(15))

  use_enable_password = db.Column(db.Boolean)

  enable_password = db.Column(db.String(50))

  strict_matching = db.Column(db.Boolean)

  parameters = db.Column(db.JSON)

  schedule = db.Column(db.DateTime)

  def __init__(self, **data):

    self.name = data.get('name')

    self.agent_type = data.get('agent_type')

    self.use_device_credentials = data.get('use_device_credentials')

    self.login = data.get('login')

    self.password = data.get('password')

    self.use_enable_password = data.get('use_enable_password, False')

    self.enable_password = data.get('enable_password')

    self._host_list = data.get('host_list')

    self._key_list = data.get('key_list')

    self.parameters = data.get('parameters', {})

    self.schedule = data.get('schedule') 

  def json(self):

    """

    return a json representation of data presented in the database



    """

    return {'name': self.name,

        'use_device_credentials': self.use_device_credentials,

        'login':self.login,

        'password':self.password,

        'use_enable_password' :self.use_enable_password,

        'enable_password' :self.enable_password,

        '_host_list' :self._host_list,

        '_key_list' :self._key_list,

        'parameters' :self.parameters,

        'schedule' :self.schedule,

        }



  @classmethod

  def find_by_name(cls, name):

    return cls.query.filter_by(name=name).first()



  def save_to_db(self):

    db.session.add(self)

    db.session.commit()



  def delete_from_db(self):

    db.session.delete(self)

    db.session.commit()


