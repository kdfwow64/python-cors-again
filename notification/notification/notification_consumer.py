from celery import Celery
from models.trigger import TriggerModel 
from models.job import JobModel
from models.task import TaskModel
from models.user import UserModel
from models.notification import NotificationModel
from models.subscriber import SubscriberModel
from models.device import DeviceModel
import logging
from logging import handlers
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
import requests
import os

parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

RABBIT_URI = 'pyamqp://{0}:{1}@{2}'.format(parser.get('RABBITMQ_SECTION', 'USER'),
                                           parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                           parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),
                                           )

app = Celery('notification', broker=RABBIT_URI)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    task_protocol=1,
)
app.conf.task_default_queue = 'notification'
FILE_LOG_LEVEL = logging.DEBUG
NOTIFICATION_LOG_FILE = '/opt/optima-notification.log'


class NotificationConsumer():
  def __init__(self, event_id, event_type, trigger):
    '''
  Object constructor
    '''
    if NotificationModel.findOne(**{"trigger_id": trigger.id}) == None:
      self.notification_id = 0
    else:
      self.notification_id = NotificationModel.findOne(**{"trigger_id": trigger.id}).id
    self.event_id = event_id
    self.event_type = event_type
    self.rootLogger = self.setLogger()
    
  def setLogger(self):
    # Log entry format
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    syslogFormatter = logging.Formatter('{{"logger":"optima-logging", "text":"%(message)s", "notification_id":"{}", "event_id":"{}", "event_type":"{}"}}'.format(
                                        self.notification_id,
                                        self.event_id,
                                        self.event_type,
                                        ))
    # Logger object
    rootLogger = logging.getLogger('notification')
    # Logging level at logger level. Set to debug to avoid filtering logs out
    rootLogger.setLevel(logging.DEBUG)
    # Creating handler to write logs on file
    fileHandler = logging.FileHandler(NOTIFICATION_LOG_FILE)
    # Adding handler to logger
    fileHandler.setFormatter(logFormatter)
    # Setting file minimal log level for handler
    fileHandler.setLevel(FILE_LOG_LEVEL)
    # STDERR log handler creation, level configuration...
    rootLogger.handlers = []
    # Adding file handler to logger
    rootLogger.addHandler(fileHandler)
    # Appending STDERR log handler to logger
    # rootLogger.addHandler(streamHandler)
    syslogHandler = handlers.SysLogHandler('/dev/log')
    syslogHandler.setFormatter(syslogFormatter)
    fileHandler.setLevel(FILE_LOG_LEVEL)
    rootLogger.addHandler(syslogHandler)
    return rootLogger

  def processTrigger(self, trigger):
    #trigger = TriggerModel.find_by_id(trigger_id)
    rule_list = trigger.rules
    #trigger_id = trigger.id
    try: notification = NotificationModel.findOne(**{"enable":"true","trigger_id": trigger.id})
    except: return rule_list, None
    result = rule_list, notification 
    return result
  
  def comparison(self, column, value, operation):
    if operation == "equals":
      if column == value:
        return 1
      return 0
    if operation == "greater than":
      if column > value:
        return 1
      return 0
    if operation == "less than":
      if column < value:
        return 1
      return 0
    if operation == "not equals":
      if column != value:
        return 1
    if operation == "contains":
      if value in column:
        return 1
    if operation == "not contains":
      if not value in column:
        return 1 
    return 0

  
  def RuleSatisfied(self, event_id, event_type, column, value, rule):
    result = 0
    if rule["element"] == "job":
      rule_column = rule["column"]
      rule_operation = rule["operation"]
      rule_value = rule["value"]
      job_id = event_id
      try: get_job = JobModel.findById(job_id)
      except : return result, None, None, None
      job = get_job.__dict__
      if rule_column == "status":
        event_value = value
      else:
        event_value = job[rule_column]
      job_name = get_job.name
      result = self.comparison(event_value, rule_value, rule_operation)
      return result, job_name, rule_column, rule_value
    return result, None, None, None

  def RuleTask(self, task_id, event_type, column, value, rule):
    result = 0
    if rule["element"] == "task":
      rule_value = rule["value"]
      if rule.get("device") and rule.get("device") != 'None':
        rule_element = "device"
      if rule.get("deviceClass") and rule.get("deviceClass") != 'None':
        rule_element = "deviceClass"
      if rule.get("group") and rule.get("group") != 'None':
        rule_element = "group "
      if rule.get("location") and rule.get("location") != 'None':
        rule_element = "location"
      get_task = TaskModel.findById(task_id)
      task = get_task.__dict__
      get_device = DeviceModel.find_by_id(get_task.device_id)
      device = get_device.__dict__
      if device[rule_element] == rule.get(rule_element) and rule_value == value:
        result = 1
      return result, device[rule_element], "status", rule_value

    if rule["element"] == "device":
      rule_column = rule["column"]
      rule_operation = rule["operation"]
      rule_value = rule["value"]
      get_task = TaskModel.findById(task_id)
      task = get_task.__dict__
      get_device = DeviceModel.find_by_id(get_task.device_id)
      device_name = get_device.name
      device = get_device.__dict__
      try : element_column = device[rule_column]
      except : return result, None, None, None
      result = self.comparison(element_column, rule_value, rule_operation)
      return result, device_name, rule_column, rule_value
    return result, None, None, None

  def sendEmailNotification(self, notification, informations):
    try: subscribers = SubscriberModel.find(**{"notification_id":notification.id})
    except: 
      self.rootLogger.error("No subscriber for notification with id : {}".format(notification.id))
      return 
    for subscriber in subscribers:
      mail_destination = subscriber.email
      message_content = notification.text
      fromaddr = "{0}".format(parser.get('SMTP_SECTION', 'USER'))
      password = "{0}".format(parser.get('SMTP_SECTION', 'PASSWORD'))
      toaddr = mail_destination
      msg = MIMEMultipart()
      msg['From'] = fromaddr
      msg['To'] = toaddr
      msg['Subject'] = "Optima Notification"
      element = informations["element"]
      name = informations["name"]
      id = informations["id"]
      value = informations["value"]
      column = informations["column"]
      text = message_content.format(element = element, element_id = id, element_name = name, element_value = value, element_column = column)
      msg.attach(MIMEText(text, 'html'))
    #body = message_content
    #msg.attach(MIMEText(body, 'plain'))
      server = smtplib.SMTP('{0}'.format(parser.get('SMTP_SECTION', 'SMTP_SERVER')), parser.get('SMTP_SECTION', 'SMTP_PORT'))
      server.starttls()
      server.login(fromaddr, password)
      text = msg.as_string()
      try:
        server.sendmail(fromaddr, toaddr, msg.as_string())
      except:
        self.rootLogger.error("An error occurred sending the notification")
        return {"message": "An error occurred sending the notification."}, 500
      try:
        server.quit()
      except:
        self.rootLogger.error("An error occurred closing the notification server")
        return {"message": "An error occurred closing the notification server"}, 501
      self.rootLogger.debug("notification sent successfully to {0} and with a mail address: {1}".format(subscriber.subscribername, mail_destination))
      return {"message": "notification sent successfully to {0}".format(mail_destination)}
    
  def sendAPINotification(self, notification, informations):
    element = informations["element"]
    name = informations["name"]
    id = informations["id"]
    value = informations["value"]
    column = informations["column"]
    url = notification.url
    data = {
        "notification_name": notification.name,
        "notification_text": notification.text.format(element = element, element_id = id, element_name = name, element_value = value, element_column = column)
        }
    if notification.method == 'POST':
      r = requests.post(url, data = data)
    if notification.method == 'GET':
      r = requests.get(url, params = data)
    self.rootLogger.debug("response from the API url : {0} {1}".format(r.status_code, r.reason))
    return

  def sendCommandNotification(self, notification, informations):
    element = informations["element"]
    name = informations["name"]
    id = informations["id"]
    value = informations["value"]
    column = informations["column"]
    os.system(notification.command.format(notification_text = notification.text.format(element = element, element_id = id, element_name = name, element_value = value, element_column = column), notification_name = notification.name ))
    self.rootLogger.debug("Command executed")
    return
  
  def sendNotification(self, notification, informations):
  #notification = NotificationModel.find_by_id(notification_id)
    if notification == None: return
    if notification.action == 'email':
      self.sendEmailNotification(notification, informations)
    if notification.action == 'API':
      self.sendAPINotification(notification, informations)
    if notification.action == 'command':
      self.sendCommandNotification(notification, informations)
    return 

  def processTriggerAndRule(self, event_id, event_type, column, value, trigger):
      if self.notification_id == 0: 
        return
      if event_type == "job":
        self.job = JobModel.findById(event_id)
      total = 0
      rule_list, notification = self.processTrigger(trigger)
      for rule in rule_list: 
        if event_type == "job":
          job_id = event_id
          count, rule_name, rule_column, rule_value = self.RuleSatisfied(job_id, event_type, column, value, rule)
          if count == 0:
            self.rootLogger.info("Rule not attained")
            return
          if rule_name == None: 
            self.rootLogger.info("Event not found")
            return
          self.rootLogger.info("Rule attained")
          total = total + count
          informations = {"element": event_type, "id": job_id, "name": rule_name, "value": rule_value, "column": rule_column}
      
        if event_type == "task":
          task_id = event_id
          count, rule_name, rule_column, rule_value = self.RuleTask(task_id, event_type, column, value, rule)
          if count == 0:
            self.rootLogger.info("Rule not attained")
            return 
          if rule_name == None:
            self.rootLogger.info("Rule attained")
            return
          total = total + count
          informations = {"element": event_type, "id": task_id, "name": rule_name, "value": rule_value, "column": rule_column}

      length = len(rule_list)
    
      if trigger.relation == "all":
        if total == length:
          self.rootLogger.debug("trigger fired")
          self.sendNotification(notification, informations)
        
      if trigger.relation == "any":
        if total > 0:
          self.rootLogger.debug("trigger fired")
          self.sendNotification(notification, informations)
      self.rootLogger.info("trigger not fired")

@app.task(serializer='json', name='notification')
def processRule(event_id, event_type, column, value):
  trigger_list = TriggerModel.find(**{"enabled":"true"})
  for trigger in trigger_list:
    notification_consumer = NotificationConsumer(event_id, event_type, trigger)
    notification_consumer.processTriggerAndRule(event_id, event_type, column, value, trigger)      
        