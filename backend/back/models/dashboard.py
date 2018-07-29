from flask_sqlalchemy import SQLAlchemy
from db import db
JOB_DASHBOARD = {"dashboardElements":["jobStat1",
                                      "jobStat2"]}
DEVICE_DASHBOARD = {"dashboardElements":["deviceStat1",
                                         "deviceStat1"]}


DASHBOARD_1 = {"dashboardElements":["ELEMENT_1",
                                    "ELEMENT_2",
                                    "ELEMENT_3",
                                    "ELEMENT_5",
                                    ]}

DASHBOARD_2 = {"dashboardElements":["ELEMENT_3",
                                    "ELEMENT_4"]}


DASHBOARDS = {"1":JOB_DASHBOARD, 
              "2":DEVICE_DASHBOARD,
              "3":DASHBOARD_1,
              "4":DASHBOARD_2}

class DashboardModel(db.Model):
  __tablename__ = 'dashboard'
  id = db.Column(db.Integer, primary_key=True)
  # user_id = db.Column(db.Integer) #, db.ForeignKey('user.id'))
  index = db.Column(db.Integer)
  name = db.Column(db.String(50))
  
  def __init__(self, **data):
    # user_id = db.Column(db.Integer) #, db.ForeignKey('user.id'))
    self.content = data

  @classmethod
  def findById(cls, id):
    print(id)
    # cls.query.filter_by(id=jobId).first()
    dashboardJson = DASHBOARDS.get(id)
    if not dashboardJson: return
    return cls(**dashboardJson)
    
  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  def json(self):
    """
    return a json representation of data presented in the database

    """
    return self.content
