from flask_sqlalchemy import SQLAlchemy
from db import db
STATUS_NEW = 'NEW'
STATUS_QUEUED = 'QUEUED'
STATUS_ONGOING = 'ONGOING'
STATUS_SUCCESSFUL = 'SUCCESSFUL'
STATUS_FAILED = 'FAILED'
STATUSES = [STATUS_NEW,
            STATUS_QUEUED,
            STATUS_ONGOING,
            STATUS_SUCCESSFUL,
            STATUS_FAILED]
COALESCE_STATEMENTS = ['coalesce({0}, 0) as {0}'.format(status.lower(), status) for status in STATUSES]
STATUSES_VALUES = ["('%s')" %status for status in STATUSES]
STATUSES_RECORD_IDS = ['"%s" int' %status.lower() for status in STATUSES]
JOB_TASK_STATUSES_QUERY = '''
select name, {0}
from ( 
  select *
    from crosstab('
     select  job.id, job.name, task.status, count(*) as ct 
     from task, job 
     where job.id=task.job_id 
     group by task.status, job.id, job.insertion_time 
     order by job.insertion_time desc, job.name 
     limit 7;',$$VALUES {1}$$)
  as ct("id" bigint,
      "name" text ,
      {2}
  )
) as t;
'''.format(', '.join(COALESCE_STATEMENTS),
           ', '.join(STATUSES_VALUES),
           ', '.join(STATUSES_RECORD_IDS))

STATISTICS_QUERY = '''
select 
  (select count(*) from devices) as devices, 
  (select count(*) from job) as jobs,
  (select count(*) from task) as tasks,
  (select count(*) from workflow) as workflows,
  (select  extract(epoch from avg(processing_end_time - processing_start_time))
  from task where processing_start_time is not null and processing_end_time is not null) as average_process_duration,
  (select (100.0*sum(case when status = 'SUCCESSFUL' then 1 else 0 end)/sum(case when status in ('SUCCESSFUL', 'FAILED') then 1 else 0 end))::float
  from task) as task_success_kpi;'''
   
DASHBOARD_ELEMENTS = {'jobStat1':{'v1':'a1'},
                      'jobStat2':{'v2':'a2'},
                      'deviceStat1':{'v3':'a3'},
                      'deviceStat2':{'v4':'a4'},
                      
                      'ELEMENT_1' :{"type":"donut",
                                    "query":"""select * from(
    select 'SUCCESSFUL' as status, coalesce(count(*), 0) as count from task where status = 'SUCCESSFUL' and processing_start_time >= date_trunc('week', CURRENT_TIMESTAMP - interval '1 week')
       
    UNION  select 'FAILED' as status, coalesce(count(*), 0) as count from task where status = 'FAILED'
    UNION  select 'QUEUED' as status, coalesce(count(*), 0) as count from task where status = 'QUEUED'
    UNION  select 'ONGOING' as status, coalesce(count(*), 0) as count from task where status = 'ONGOING'
    UNION  select 'NEW' as status, coalesce(count(*), 0) as count from task where status = 'NEW'
) as t order by status;""",
                                    "description":"Last Task Statuses Overview",
                                    "parameters":{}
                                    },
                      'ELEMENT_2' : {"type":"echart",
                                    "query":JOB_TASK_STATUSES_QUERY,
                                    "description":"Last 7 Jobs Detailed Statuses",
                                    "parameters":{}
                                    },
                      'ELEMENT_3' : {"type":"top",
                                     "query":"""select device_id, count(*), devices.name 
                                     from task, devices 
                                     where task.device_id = devices.id 
                                     group by device_id, devices.name 
                                     order by count desc 
                                     limit 5;""",
                                     "description":"Top Device Update",
                                     "parameters":{}
                                     },
                      'ELEMENT_4' : {"type":"bar",
                                     "query":"""select device_id, count(*), devices.name 
                                     from task, devices 
                                     where task.device_id = devices.id 
                                     group by device_id, devices.name order by count desc 
                                     limit 5;""",
                                     "description":"some",
                                     "parameters":{}
                                     },
                      'ELEMENT_5' : {"type":"top",
                                     "query":"""select agent_type as name, count(*) 
                                     from job 
                                     group by job.agent_type 
                                     order by count desc limit 5;""",
                                     "description":"Top Agents Usage",
                                     "parameters":{}
                                     },
                      
                      'statistics' : {"type":"statistics",
                                     "query":STATISTICS_QUERY,
                                     "description":"statistics",
                                     "parameters":{}
                                     },
                      'ELEMENT_6' : {"type":"bar",
                                     "query":"""select job_id, count(*) as count, job.name 
                                     from task, job 
                                     where task.job_id=job.id 
                                     group by job_id, job.name 
                                     order by count desc limit 5;""",
                                     "description":"Number of Device in The Last Jobs ",
                                     "parameters":{}
                                     },
                      }



class DashboardElementModel(db.Model):
  __tablename__ = 'dashboardElement'
  id = db.Column(db.Integer, primary_key=True)
  # user_id = db.Column(db.Integer) #, db.ForeignKey('user.id'))   
  def __init__(self, **data):
    # user_id = db.Column(db.Integer) #, db.ForeignKey('user.id'))
    self.type = data["type"]
    self.query = data["query"]
    self.parameters = data["parameters"]
    self.description = data['description']

  @classmethod
  def findById(cls, id_):
    # cls.query.filter_by(id=jobId).first()
    if id_ == 1:
      # jobs
      return ELEMENT_1
    elif id_ == 2:
      # devices
      return {"id":2}

  @classmethod
  def findByName(cls, name):
    '''Temp method'''
    #cls.query.filter_by(id=jobId).first()
    dashboardElementJson = DASHBOARD_ELEMENTS.get(name)
    if not dashboardElementJson: return
    return cls(**dashboardElementJson)
    #return ELEMENT_1
    
  @classmethod
  def find(cls, **queryArguments):
    return list(cls.query.filter_by(**queryArguments))

  def json(self):
    """
    return a json representation of data presented in the database
    """
    return {'type': self.type,
            'query': self.query,
            'parameters': self.parameters,
            'description':self.description,}

  def get_values(self):
    result = db.engine.execute(self.query)
    columns = result.keys()
    return [dict(zip(columns,list(row))) for row in result.fetchall()]
