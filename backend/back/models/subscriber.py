from db import db
from models.user import UserModel

class SubscriberModel(db.Model):
  __tablename__ = 'subscriber'
  id = db.Column(db.Integer, primary_key=True)
  subscriber_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
  notification_id = db.Column(db.Integer, db.ForeignKey('notification.id', ondelete='CASCADE'))
  subscribername = db.Column(db.String(80))
  email = db.Column(db.String(80))
  
  def __init__(self, notification_id, subscribername = None):
    print(subscribername)
    user = UserModel.find_by_username(str(subscribername))
    #self.subscriber_id = subscriber_id       
    self.notification_id = notification_id   
    if subscribername == None:
        self.subscribername = user.username
    else:
        self.subscribername= subscribername
    self.email = user.email  
   
  def json(self):
    return {'id': self.id,
            'subscriber_id':self.subscriber_id,
            'notification_id': self.notification_id,
            'subscribername': self.subscribername,
            'email': self.email
            }

  @classmethod
  def update(self, id, param):
    group_subscriber = cls.find({"id":id})
    if group_subscriber:
      db.update(group_subscriber).values(**param)

  '''
  @classmethod
  def find_by_subscriber_id(cls, subscriber_id):
    return cls.query.filter_by(subscriber_id=subscriber_id).first()
  '''
        
  @classmethod
  def find_by_notification_id(cls, id):
    return cls.query.filter_by(notification_id=id).first()

  @classmethod
  def findById(cls, group_subscriber_id):
    return cls.query.filter_by(id=group_subscriber_id).first()

  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  @classmethod
  def findOne(cls, **queryArguments):
    return cls.query.filter_by(**queryArguments).first()

  def save_to_db(self):
    db.session.add(self)
    self.commit()

  @staticmethod
  def commit():
    db.session.commit()
    
  def delete_from_db(self):
    db.session.delete(self)
    db.session.commit()
