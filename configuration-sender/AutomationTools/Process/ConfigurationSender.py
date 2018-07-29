#!/usr/bin/python
import sys
sys.path.insert(0, '/opt/optima/configuration-sender/')

from AutomationTools.Tools.Consts import (RETURN_OK,
                                          RETURN_KO, 
                                          CONFIGURATION_SENDER_NAME,
                                          CONFIGURATION_SENDER_CONFIG_FILE,
                                          CONFIGURATION_SENDER_LOG_FILE,
                                          CONFIGURATION_SENDER_RESULT_FOLDER)
from AutomationTools.Process.AbstractAutomation import AbstractAutomation
from AutomationTools.Tools.Utils import checkPrompt

import random
import json
# from openpyxl import load_workbook

# OS library
import os

# SSH and Telnet libraries
import paramiko
import telnetlib
# Logging library
import logging
from logging import handlers

# import configuration parser
import configparser

# Argument parser
from argparse import ArgumentParser

# Ordered Dict: Python(2.7) dictionary keys are not ordered.
from collections import OrderedDict

# System objects access
import sys
import re

# Sleep/wait function
from time import sleep

from datetime import datetime

# pretty printing (used for testing)
from pprint import pprint

from celery import Celery
from AutomationTools.models.task import TaskModel
from AutomationTools.models.job import JobModel
from AutomationTools.models.device import DeviceModel

from kombu import Connection, Exchange, Producer
import uuid
from uuid import uuid4


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
# Config file
CONFIG_FILE = 'configurationSender.cnf'
# Logging configuration
SCRIPT_LOG_FILE = "configurationSender.log"
SSH_LOG_FILE = "configurationSenderSshClient.log"

# Avoid paging prompt
NO_PAGING_COMMAND = 'terminal length 0'
TERMINAL_MONITOR_COMMAND = 'terminal monitor'

CONF_START_LINE = 'Enter configuration commands, one per line'
END_OF_FILE = "End-Of-File"
# Result files folder
RESULT_FOLDER = 'results'
PROMPT_WAIT_CYCLES = 6
# Logging levels
FILE_LOG_LEVEL = logging.DEBUG
STREAM_LOG_LEVEL = logging.INFO

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
RABBIT_URI = "pyamqp://{0}:{1}@{2}/".format(parser.get('RABBITMQ_SECTION', 'USER'),
                                            parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                            parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),)
app = Celery(CONFIGURATION_SENDER_NAME, broker=RABBIT_URI)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    task_protocol=1,
)
app.conf.task_default_queue = 'configuration_sender'
connection = Connection(RABBIT_URI)
channel = connection.channel()
notification_exchange = Exchange("notification", type="direct")
notification_producer = Producer(exchange=notification_exchange, channel=channel, routing_key="notification")

import pika
import pika_pool

rmq_usr = str(parser.get('RABBITMQ_SECTION', 'USER'))
rmq_pass = str(parser.get('RABBITMQ_SECTION', 'PASSWORD'))

credentials = pika.PlainCredentials(rmq_usr, rmq_pass)
pool = pika_pool.QueuedPool(
create=lambda: pika.BlockingConnection(pika.ConnectionParameters(parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),
                                                               5672,
                                                               '/',
                                                               credentials)),
     max_size=10,
     max_overflow=10,
     timeout=10,
     recycle=3600,
     stale=45,
 )

orchestrator_exchange = Exchange("orchestrator", type="direct")
orchestrator_producer = Producer(exchange=orchestrator_exchange, channel=channel, routing_key="orchestrator")
job_manager_exchange = Exchange("job_manager", type="direct")
job_manager_producer = Producer(exchange=job_manager_exchange, channel=channel, routing_key="job_manager")

class ConfigurationSender(AbstractAutomation):

  def __init__(self, job, task):
    '''
Object constructor
    '''
    AbstractAutomation.__init__(self, job, task)
    self.config = self.getConfig()
    self.rootLogger = self.setLogger()
    self.commandlist = []
    self.enablePassword = job.enable_password
    if self.enablePassword:
      self.enableFlag = True
    #self.configurationTuples = self.buildConfiguration(arguments)
    self.remoteCommand = job.parameters['remoteCommand']

  def getConfig(self):
    # Parser
    configuration = {}
    parser = configparser.ConfigParser()
    
    parser.read('{}'.format(CONFIGURATION_SENDER_CONFIG_FILE))
    configuration = {
              'MAX_THREADS'       :parser.getint('GLOBAL', 'MAX_THREADS'),
              # SSH
              'SSH_TIMEOUT'       :parser.getint('SSH', 'SSH_TIMEOUT'),
              'SHELL_TIMEOUT'     :parser.getint('SSH', 'SHELL_TIMEOUT'),
              'OUTPUT_WAIT_CYCLES':parser.getint('SSH', 'OUTPUT_WAIT_CYCLES'), # x 0.5seconds
              'READ_SIZE'         :parser.getint('SSH', 'READ_SIZE'),
              # TELNET
              
    }
    return configuration

  def setLogger(self):
    agent_name = CONFIGURATION_SENDER_NAME.lower()
    # Log entry format
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    syslogFormatter = logging.Formatter('{{"logger":"optima-logging", "text":"%(message)s", "agent_type":"{}","device_name":"{}","task_id":"{}","job_id":"{}",       "job_name":"{}"}}'''.format(
                                 agent_name,
                                 self.device.name,
                                 self.task.id,
                                 self.job.id,
                                 self.job.name))
    # Logger object
    rootLogger = logging.getLogger(CONFIGURATION_SENDER_NAME)
    # Logging level at logger level. Set to debug to avoid filtering logs out
    rootLogger.setLevel(logging.DEBUG)
    # Creating handler to write logs on file
    fileHandler = logging.FileHandler(CONFIGURATION_SENDER_NAME)
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

  def sendToQueue(self, producer, task, data):
    with pool.acquire() as cxn:
     cxn.channel.basic_publish(
         body=json.dumps({"args":[],
                   "kwargs":data,
                    "task":task,
                    "id":str(uuid4())}),
         exchange=task,
         routing_key=task,
         properties=pika.BasicProperties(
             content_type='application/json',
             content_encoding='utf-8',
             delivery_mode=2,
         )
     )

  def readConfig(self, shell, host):
    '''
This function is used by SSH connections to read the remote command's output
    '''
    shell.send('\n\n')
    # FNO: waiting for prompt. we could make the wait more strict and wait till a # is seen
    sleep(1)
    output = b''
    for i in range(0, PROMPT_WAIT_CYCLES):
      sleep(.5)
      output += shell.recv(300)
      if b'#' in output or b'$' in output: break
    # output = shell.recv('300')
    prompt = output.split(b'#')[0].strip()
    # FNO: support $ prompt, too
    prompt = prompt.split(b'$')[0].strip()
    initialWait = 3
    fullyRead = False
    # Initialization of read data
    data = b''
    # Execution of remote command
    self.commandlist = self.task.parameters.get('command', self.remoteCommand).split("\r\n")
    for command in self.commandlist:
      #if not command.strip(): continue
      shell.send(str(command) + '\n')
    sleep(initialWait)
    shell.send(END_OF_FILE*3)
    # sprompt = host + '#'
    # Read data in chunks as long as it's available
    for i in range(0, self.config.get('OUTPUT_WAIT_CYCLES')):
      sleep(.5)
      if not shell.recv_ready(): continue
      while shell.recv_ready():
        data += shell.recv(self.config.get('READ_SIZE'))
      if checkPrompt(data):
        fullyRead = True
        break
    if not fullyRead:
      self.rootLogger.debug('Configuration not fully read for host {0} (prompt is "{1}". Configuration: \n{2}'.format(host, prompt, data))
      data = None
    # Return data
    self.rootLogger.debug('Configuration took {0} to be read on host {1}'.format(str(initialWait + .5*(i+1)), host))
    return data

  def getConfUsingSSH(self, host):
    '''
Connect to host and extract configuration using SSH1.99 or SSH2
    '''
    # config and connected flag initialization
    config = None
    connected = False
    # SSH client creation
    sshClient = paramiko.SSHClient()
    # Automatically add host keys
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      # Try connecting to host before timeout expiration
      sshClient.connect(host, username=self.login, password=self.password, look_for_keys=False, allow_agent=False, timeout=self.config.get('SSH_TIMEOUT'))
    except Exception as e:
      self.rootLogger.warning("Could not connect to host {0} using SSH. Error: {1}".format(host, str(e)))
      return connected, config
    # Connection established. Set flag to true
    connected = True
    self.rootLogger.debug("Connected to host {0} using SSH.".format(host))
    try:
      # Invoking shell for further command execution
      shell = sshClient.invoke_shell()
    except:
      self.rootLogger.error("Could not get shell for host {0}. Probably lost the SSH connection".format(host))
      sshClient.close()
      return connected, config
    # Setting shell timeout
    shell.settimeout(self.config.get('SHELL_TIMEOUT'))
    # Disabling paging
    shell.send('{0}\n'.format(NO_PAGING_COMMAND))
    if self.enableFlag:
      shell.send('enable\n')
      shell.send(self.enablePassword + '\n')
    if self.device.use_enable_password:
      shell.send('enable\n')
      shell.send(device.enable_pass + '\n')
    sleep(1)
    # Read banner, prompts... and do nothing with them
    shell.recv(10000)
    # Reading returned configuration
    config = self.readConfig(shell, host)
    sshClient.close()
    return connected, config

  def getConfUsingTelnet(self, host):
    '''
Connect to host and extract configuration using Telnet
    '''
    # config and connected flag initialization
    config = None
    connected = False
    # Telnet client creation
    try:
      telnetClient = telnetlib.Telnet(host, timeout=self.config.get('TELNET_TIMEOUT'))
    except Exception as e:
      self.rootLogger.warning("Could not connect to host {0} using Telnet. Error: {1}".format(host, str(e))) 
      return connected, config
    # Connection established. Flag set to true
    connected = True
    # Reading until finding TELNET READ LOGIN prompt but avoid going over read timeout value
    """banner = telnetClient.read_until(TELNET_READ_LOGIN, self.config.get('TELNET_READ_TIMEOUT'))
      
    if not TELNET_READ_LOGIN in banner: 
      self.rootLogger.warning('Could not get "{0}" prompt for telnet connection on host {1}'.format(TELNET_READ_LOGIN, host))
      return connected, config"""
    # Sending login and password
    telnetClient.write((self.login + "\n").encode('ascii'))
    sleep(0.5)
    telnetClient.write((self.password + "\n").encode('ascii'))
    sleep(0.5)
    self.rootLogger.debug("Connected to host {0} using Telnet.".format(host)) 
    #telnetClient.write(str('{0}\n{1}\n'.format(str(self.login), str(self.password))))
    # Reading what's available without blocking
    # TODO: Remove below
    # telnetClient.write('enable\n{0}\n'.format(ENABLE_PASS))
    # telnetClient.read_lazy()
    # Sending command to avoid paging then remote command
    #telnetClient.write((NO_PAGING_COMMAND + "\n").encode('ascii'))
    sleep(1)
    telnetClient.write(b'\n\n')
    sleep(0.3)
    if self.device.use_enable_password:
      telnetClient.write(b'enable\n')
      telnetClient.write((device.enable_pass + '\n').encode('ascii'))
    if self.enableFlag:
      telnetClient.write(b'enable\n')
      telnetClient.write((self.enablePassword + '\n').encode('ascii'))
    output = telnetClient.read_lazy()
    prompt = output.split(b'#')[0].strip()
    # FNO: Support $ prompt, too
    prompt = prompt.split(b'$')[0].strip()
    telnetClient.read_lazy()
    telnetClient.write((NO_PAGING_COMMAND + "\n").encode('ascii'))
    self.commandlist = self.task.parameters.get('command', self.remoteCommand).split("\r\n")
    for command in self.commandlist:
       telnetClient.write((command + '\n').encode('ascii'))
    sleep(2)
    telnetClient.write((END_OF_FILE*3).encode('ascii'))
    # Read until end of config is found or timeout expired
    # prompt = host + '#'
    #try:
    config = telnetClient.read_until(END_OF_FILE.encode('ascii'), self.config.get('TELNET_READ_TIMEOUT')).decode("ascii")
    try:
      config = config.split(NO_PAGING_COMMAND)[1]
    except:
      self.rootLogger.error('Could not get full configuration for {0}, the configuration is : {0}'.format(host, config))
      return connected, None
    # Checking if configuration was fully recovered
    if END_OF_FILE not in config:
      self.rootLogger.error('Could not get full configuration for {0}'.format(host))
      # Configuration not entirely recovered. Return None for config
      return connected, None
      # All good
    self.rootLogger.debug('Extracted configuration for host {0}:\n{1}'.format(host, config))
    return connected, config

  
  def updateTaskStatus(self, status, setStartTime=False, setEndTime=False):
    '''Can be moved to Abstract module'''
    self.task.status = status
    now = datetime.now()
    if setStartTime: self.task.processing_start_time = now
    if setEndTime: self.task.processing_end_time = now
    message = 'Setting task status to ' + status
    if status == STATUS_FAILED:
        self.rootLogger.error(message)
    if status == STATUS_ONGOING:
        if self.job.status == STATUS_NEW: 
          self.job.status = status
    else:
        self.rootLogger.info(message)
    self.task.commit()
    
  def processDevice(self):
    '''
Thread function. Used to process hosts: configuration collection and key matching
    '''
    result= {}
    self.updateTaskStatus(STATUS_ONGOING, setStartTime=True, setEndTime=False)
    #result = {k:False for k in self.keyList}
    # Get host without waiting
    try:
      device = DeviceModel.findById(self.task.device_id)
    except Exception as e:
      # No host left. Just exit the thread
      self.rootLogger.error("Could not find device with device id {}. Error: {}".format(task.device_id, str(e)))
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      return
    host = device.name
    # Starting host processing for host
    self.rootLogger.debug("Processing device {0}.".format(device.name))
    # Get configuration using SSH
    connected, config = self.getConfUsingSSH(device.name)
    # if not connected:
      # Could not connect using SSH, fallback on Telnet
    #  connected, config = self.getConfUsingTelnet(host)
    if not connected:
      # Still could not connect using the fallback protocol. Log it as an error
      connected, config = self.getConfUsingTelnet(device.name)
      if not connected:
      # Still could not connect using the fallback protocol. Log it as an error
        self.rootLogger.error('Could not connect to to device {0} with any transport mechanism.'.format(device.name))
        self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
        data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
        self.sendToQueue(job_manager_producer, "job_manager", data)
        result.update({"status": STATUS_FAILED, "configurations":"NOT CONNECTED"})
        return
    if not config:
      # Configuration not extracted for diverse reasons. Update dictionary and start processing another host
      self.rootLogger.error('Empty configuration for device {0}'.format(device.name))
      #TODO update result...
      #matchedHosts.update({host:[False, set()]})
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      result.update({"status": STATUS_FAILED, "configurations":"NO CONFIGURATION"})
      return
    # Configuration collected ! Matching it with keys
    buff = []
    """for c in self.remoteCommand:
      if c == '\r\n':
        self.commandlist.append(''.join(buff))
        buff = []
      else:
        buff.append(c)
    else:
      if buff:
        self.commandlist.append(''.join(buff))"""
    try:
      conf = config.decode('utf-8')
    except:
      conf = config
    for command in self.commandlist:
      conf = re.sub('{}'.format(command), '', conf)
    conf = re.sub('{}'.format(END_OF_FILE), '', conf)
    if conf.startswith("\r"):
      conf = conf[1:]
    if conf.startswith("\n"):
      conf = conf[1:]
    self.rootLogger.debug('Configuration for device {0}: \n{1}'.format(device.name, conf))
    #keys = set(self.keyRegex.findall(config.decode('utf-8')))
    #keys = [k.strip() for k in keys]
    result.update({"status": STATUS_SUCCESSFUL, "configurations":{}})
    result["configurations"].update({"output":conf})
    self.task.result = result
    #TODO update result
    # matchedHosts.update({host:result})
    self.rootLogger.info("Extracted and parsed configuration for device {0}.".format(device.name)) 
    # Out of while loop. Exiting thread
    self.updateTaskStatus(STATUS_SUCCESSFUL, setEndTime=True)
    data = {"element_id":self.task.id,
              "status": STATUS_SUCCESSFUL}
    self.sendToQueue(job_manager_producer, "job_manager", data)
    self.rootLogger.info('Finished processing device {0}.'.format(device.name))
    
@app.task(serializer='json', name=CONFIGURATION_SENDER_NAME)
def main_task(task_id):
  # Point of entry of the script.
  # Call the main function for the whole processing
  task = TaskModel.findById(task_id)
  job = JobModel.findById(task.job_id)
  configurationSender = ConfigurationSender(job, task)
  configurationSender.processDevice()
