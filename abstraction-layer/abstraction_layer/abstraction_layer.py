from celery import Celery
from models.task import TaskModel
from models.job import JobModel
from models.device import DeviceModel
from models.deviceClass import DeviceClassModel
from models.location import LocationModel
from models.group import GroupModel
from uuid import uuid4
from kombu import Connection, Exchange, Producer, binding, Queue
import configparser

parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

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


AGENT_EXCHANGE = 'agent_exchange'
RABBIT_URI = 'amqp://{0}:{1}@{2}'.format(parser.get('RABBITMQ_SECTION', 'USER'),
                                           parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                          parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),)
app = Celery('AbstractionLayer', broker=RABBIT_URI)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    task_protocol=1,
)
#app.conf.task_routes = {'feed.tasks.*':{'queue':'raw_jobs'}}
app.conf.task_default_queue = 'raw_jobs'
agents_exchange = Exchange(AGENT_EXCHANGE, type="direct")
connection = Connection(RABBIT_URI)
channel = connection.channel()
"""app.conf.task_queues = (
    Queue('configuration_parser', agents_exchange, routing_key='configuration_parser'),
    Queue('configuration_sender', agents_exchange, routing_key='configuration_sender'),
    Queue('configuration_differ_precheck', agents_exchange, routing_key='configuration_differ_precheck'),
    Queue('configuration_differ_postcheck', agents_exchange, routing_key='configuration_differ_postcheck'),
    Queue('configuration_image_loader', agents_exchange, routing_key='configuration_image_loader'),
)"""
notification_exchange = Exchange("notification", type="direct")
notification_producer = Producer(exchange=notification_exchange, channel=channel, routing_key="notification")
   
def applyAbstraction(taskList):
  return

def extractTasks(job_id):
  print(job_id)
  job = JobModel.findById(job_id)
  taskList = TaskModel.find(**{"job_id": job_id})
  print(taskList)
  applyAbstraction(taskList)
  return job, taskList

def sendTasks(job, taskList):
  
  producer = Producer(exchange=agents_exchange, channel=channel, routing_key=job.agent_type)
  for task in taskList:
    task_id = task.id
    if task == taskList[-1]:
      celeryTask = {"args":[],
                    "kwargs":{"task_id":task_id,},
                    "task":job.agent_type,
                    "id":str(uuid4().hex)}
    else:
      celeryTask = {"args":[],
                    "kwargs":{"task_id":task_id,},
                    "task":job.agent_type,
                    "id":str(uuid4().hex)}
    producer.publish(celeryTask)
    task.status = STATUS_QUEUED
    task.commit()
    
    print("sent task " + str(celeryTask) + ". Routing key: " + str(job.agent_type))

@app.task(serializer='json', name='AbstractionLayer')
def processTask(job_id):
  job, taskList = extractTasks(job_id)
  sendTasks(job, taskList)
  return "processed job {} ({})".format(job.name, job_id)

