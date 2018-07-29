#!/usr/bin/python
import sys
sys.path.insert(0, '/opt/optima/configuration-image-loader/')
from AutomationTools.Tools.Consts import (RETURN_OK,
                                          RETURN_KO,
                                          CONFIGURATION_IMAGE_LOADER_CONFIG_FILE,
                                          CONFIGURATION_IMAGE_LOADER_LOG_FILE,
                                          CONFIGURATION_IMAGE_LOADER_RESULT_FOLDER,
                                          CONFIGURATION_IMAGE_LOADER_NAME,)
from AutomationTools.Process.AbstractAutomation import AbstractAutomation
from AutomationTools.Tools.Utils import checkPrompt

from celery import Celery
from AutomationTools.models.task import TaskModel
from AutomationTools.models.job import JobModel
from AutomationTools.models.device import DeviceModel
import random


# FNO
# import library used to calculate diff between configurations
import difflib

from datetime import datetime

# import configuration parser
import configparser
import re

import csv
# Json library
import json
# SSH and Telnet libraries
import paramiko
import telnetlib

# Logging library
import logging
from logging import handlers
# Sleep/wait function
from time import sleep

# Ordered Dict: Python(2.7) dictionary keys are not ordered.
from collections import OrderedDict
import json

# System objects access
import sys
import os
from ftplib import FTP
# pretty printing (used for testing)
from pprint import pprint

from kombu import Connection, Exchange, Producer
import uuid
from uuid import uuid4

END_OF_FILE = "End-Of-File"
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

# ExpectedTelnet login prompt
TELNET_READ_LOGIN = 'Username:'

# Logging levels
FILE_LOG_LEVEL = logging.DEBUG
STREAM_LOG_LEVEL = logging.INFO

# Columns' names
# No key matched
NO_MATCH_STRING = 'No Match'
# Configuration not available
UNAVAILABLE_CONF_STRING = 'Unavailable Configuration'

# Cisco Commands
# Avoid paging prompt
NO_PAGING_COMMAND = 'terminal length 0'

# Wait cycles for reading prompt
PROMPT_WAIT_CYCLES = 6

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
RABBIT_URI = "pyamqp://{0}:{1}@{2}/".format(parser.get('RABBITMQ_SECTION', 'USER'),
                                            parser.get('RABBITMQ_SECTION', 'PASSWORD'),
                                            parser.get('RABBITMQ_SECTION', 'RABBITMQ_HOST'),)
connection = Connection(RABBIT_URI)
channel = connection.channel()
notification_exchange = Exchange("notification", type="direct")
notification_producer = Producer(exchange=notification_exchange, channel=channel, routing_key="notification")

orchestrator_exchange = Exchange("orchestrator", type="direct")
orchestrator_producer = Producer(exchange=orchestrator_exchange, channel=channel, routing_key="orchestrator")

job_manager_exchange = Exchange("job_manager", type="direct")
job_manager_producer = Producer(exchange=job_manager_exchange, channel=channel, routing_key="job_manager")

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

app = Celery(CONFIGURATION_IMAGE_LOADER_NAME, broker=RABBIT_URI)
app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    task_protocol=1,
)
app.conf.task_default_queue = 'configuration_image_loader'

class ConfigurationImageLoader(AbstractAutomation):

  def __init__(self, job, task):
    '''
Object constructor
    '''
    AbstractAutomation.__init__(self, job, task)
    self.ftpServer = job.parameters.get('ftpServer')
    self.ftpPort = job.parameters.get('ftpPort', 21)
    self.ftpUser = job.parameters.get('ftpUser')
    self.ftpPassword = job.parameters.get('ftpPassword')
    self.ftpImage = job.parameters.get('ftpImage')
    self.ftpProtocol = job.parameters.get('ftpProtocol')
    self.imageFile = self.ftpImage.split('/')[-1]
    self.deviceStorage = job.parameters.get('deviceStorage')
    self.enablePassword = job.enable_password
    if self.enablePassword:
      job.enableFlag = True
    self.imageSize = -1
    self.ftpCommand = ''
    self.config = self.getConfig()
    self.rootLogger = self.setLogger()
    self.job = job
    self.task = task

  def getConfig(self):
    # Parser
    configuration = {}
    parser = configparser.ConfigParser()
    
    parser.read('{}'.format(CONFIGURATION_IMAGE_LOADER_CONFIG_FILE))
    configuration = {
              'MAX_THREADS'       :parser.getint('GLOBAL', 'MAX_THREADS'),
              # SSH
              'SSH_TIMEOUT'       :parser.getint('SSH', 'SSH_TIMEOUT'),
              'SHELL_TIMEOUT'     :parser.getint('SSH', 'SHELL_TIMEOUT'),
              'OUTPUT_WAIT_CYCLES':parser.getint('SSH', 'OUTPUT_WAIT_CYCLES'), # x 0.5seconds
              'READ_SIZE'         :parser.getint('SSH', 'READ_SIZE'),
              # TELNET
              'TELNET_TIMEOUT'     :parser.getint('TELNET', 'TELNET_TIMEOUT'),
              'TELNET_READ_TIMEOUT'     :parser.getint('TELNET', 'TELNET_READ_TIMEOUT'),
              'TELNET_READ_CONFIG_TIMEOUT'     :parser.getint('TELNET', 'TELNET_READ_CONFIG_TIMEOUT'),
    }
    return configuration

  def setLogger(self):
    agent_name = CONFIGURATION_IMAGE_LOADER_NAME.lower()
    # Log entry format
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    syslogFormatter = logging.Formatter('{{"logger":"optima-logging", "text":"%(message)s", "agent_type":"{}","device_name":"{}","task_id":"{}","job_id":"{}",       "job_name":"{}"}}'''.format(
                                 agent_name,
                                 self.device.name,
                                 self.task.id,
                                 self.job.id,
                                 self.job.name))
    # Logger object
    rootLogger = logging.getLogger(CONFIGURATION_IMAGE_LOADER_NAME)
    # Logging level at logger level. Set to debug to avoid filtering logs out
    rootLogger.setLevel(logging.DEBUG)
    # Creating handler to write logs on file
    fileHandler = logging.FileHandler(CONFIGURATION_IMAGE_LOADER_NAME)
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
    
  def getImageSize(self):
    '''
Gets image size from FTP server
    '''
    if self.ftpProtocol == "ftp":
      ftp = FTP()
      try:
        ftp.connect(self.ftpServer, int(self.ftpPort))
      except Exception as e:
        self.rootLogger.error('Could not connect to FTP server from this device: {0}.'.format(str(e)))
        return RETURN_KO
      try:
        ftp.login(self.ftpUser, self.ftpPassword)
      except Exception as e:
        self.rootLogger.error('Could not login into FTP server from this device: {0}.'.format(str(e)))
        return RETURN_KO
      try:
        self.imageSize = ftp.size(self.ftpImage)
      except Exception as e:
        self.rootLogger.error('Could not get image file size from FTP server: {0}.'.format(str(e)))
        return RETURN_KO
      return RETURN_OK
    return RETURN_OK

  def checkDeviceUsable(self, shell, host, type):
    '''
Check if enough space on device before copying file
    '''
    enoughSpace = True
    imageInexistent = True
    command = 'dir ' + self.deviceStorage + '\n'
    #try : 
    if type == "SSH":
      shell.send(command)
    #except: return 
      sleep(3)
      dirOutput = shell.recv(10000)
    if type == "TELNET":
      shell.write(command.encode("ascii"))
    #except: return 
      sleep(3)
      dirOutput = shell.read_all()
      
    expectedRegex = re.compile(b'\((\d+) bytes free\)')
    match = expectedRegex.findall(dirOutput)
    self.rootLogger.debug('Dir command output: \n{0}'.format(dirOutput))
    if not match:
      self.rootLogger.error('Could not find device size for host: {0}. Dir command output: \n{1}'.format(host, dirOutput))
    elif self.imageSize < int(match[0]):
      enoughSpace = True
    if self.imageFile in str(dirOutput):
       self.rootLogger.error('Image file already exists.')
       imageInexistent = False
    return enoughSpace and imageInexistent, dirOutput

  def copyImage(self, shell, host, type):
    '''
    Initiates copy command and watches transfer
    '''
    if type == "SSH":
      shell.send('\n\n')
    if type == "TELNET":
      shell.write(b'\n\n')
      sleep(0.3)
    output = b''
    for i in range(0, PROMPT_WAIT_CYCLES):
      sleep(.5)
      if type == "SSH":
        output += shell.recv(300)
      if type == "TELNET":
        output = shell.read_all()
      if b'#' in output or b'$' in output: break
    
    prompt = output.split(b'#')[0].strip()
    # FNO: support $ prompt, too
    prompt = prompt.split(b'$')[0].strip()
    # prompt = host + "#"
    success = False
    copyEnded = False
    data = b''
    if type == "SSH":
      shell.send(self.ftpCommand + '\n')
      sleep(0.5)
      shell.send('\n')
    if type == "TELNET":
      shell.write((self.ftpCommand + '\n').encode("ascii"))
      sleep(0.5)
      shell.write(b'\n')
    '''
    sleep(0.5)
    data += shell.recv(READ_SIZE)
    if '? [confirm]' in data:
      self.rootLogger.error('Image file already exists in device on {0}'.format(host))
      return success
    '''
  # Read data in chunks as long as it's available
    """i = 0
    while i <= self.config.get('OUTPUT_WAIT_CYCLES'):
      if shell.recv_ready():
        data += shell.recv(self.config.get('READ_SIZE'))
        if checkPrompt(prompt, data):
          copyEnded = True
          break
        else:
          i = 0
      else:
        # Nothing to read
        i += 1
        sleep(1)
    if not copyEnded:
      self.rootLogger.error('Copy not fully done for host {0}. Output:\n{1}'.format(host, data))
      success = False
      return success"""
    
    self.rootLogger.info('Successfully copied image to host {0}'.format(host))
    self.rootLogger.debug('Copy output from host {0}:\n{1}'.format(host, data))
    success = True
    return success, output
     
  def verifyCopy(self, shell, type):
    '''
Check if file has been copied correctly to device
    '''
    success = False
    command = 'dir ' + self.deviceStorage + '\n'
    if type == "SSH":
      shell.send(command)
      sleep(2)
      dirOutput = shell.recv(10000)
    if type == "TELNET":
      shell.writ(command.encode('ascii'))
      sleep(2)
      dirOutput = shell.read_all()
    self.rootLogger.debug('Checking for image file existence. Dir command output: \n{0}'.format(dirOutput))
    if self.imageFile in str(dirOutput):
      success = True
    return success, dirOutput

  def buildFtpCommand(self):
    '''
Building FTP command using CLI arguments
    '''
    commandTemplate = ''
    if self.ftpProtocol == "ftp":
      commandTemplate = 'copy ftp://{0}:{1}@{2}:{3}/{4} {5}'
      self.ftpCommand = commandTemplate.format(self.ftpUser, self.ftpPassword, self.ftpServer, self.ftpPort, self.ftpImage, self.deviceStorage)
    elif self.ftpProtocol == "sftp":
      commandTemplate = 'copy scp://{0}:{1}@{2}:{3}/{4} {5}'
      self.ftpCommand = commandTemplate.format(self.ftpUser, self.ftpPassword, self.ftpServer, self.ftpPort, self.ftpImage, self.deviceStorage)
    elif self.ftpProtocol == "tftp":
      commandTemplate = 'copy tftp://{0}:{1}/{2} {3}'
      self.ftpCommand = commandTemplate.format(self.ftpServer, self.ftpPort, self.ftpImage, self.deviceStorage)
    
  def formatHostResults(self, hostResults):
    '''
Format host results
    '''
    n = datetime.now().strftime('%Y%m%d_%H%M%S')
    fileName = 'copy_result_{0}_{1}'.format(self.imageFile, n) + '.csv'
    filePath = os.path.join(IMAGE_LOADER_RESULT_FOLDER, fileName)
    try:
      resultFile = open(filePath, 'w')
    except Exception as e:
      self.rootLogger.error('Could not open result file: {0}.'.format(str(e)))
      raise
    # Writing CSV header 
    resultFile.write('"host","success","description"\n')
    # Looping on keys and writing their values
    map(lambda x: resultFile.write('"{0}","{1}","{2}"\n'.format(x[0], x[1][0], x[1][1])), hostResults.items())
    # CSV file written. Time to close it
    try:
      resultFile.close()
    except Exception as e:
      self.rootLogger.error('Could not result file: {0}.'.format(str(e)))
      raise
    self.rootLogger.info('Result file {0} written.'.format(fileName))
    return

  def getConfUsingSSH(self, host):
    '''
Connect to host and extract configuration using SSH1.99 or SSH2
    '''
    # config and connected flag initialization
    config = None
    connected = False
    shell = None
    returnCode = False
    # SSH client creation
    sshClient = paramiko.SSHClient()
    # Automatically add host keys
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      # Try connecting to host before timeout expiration
      sshClient.connect(host, username=self.login, password=self.password, look_for_keys=False, allow_agent=False, timeout=self.config.get('SSH_TIMEOUT'))
    except Exception as e:
      self.rootLogger.warning("Could not connect to host {0} using SSH. Error: {1}".format(host, str(e)))
      return connected, returnCode, shell, output
    # Connection established. Set flag to true
    connected = True
    self.rootLogger.debug("Connected to host {0} using SSH.".format(host))
    try:
      # Invoking shell for further command execution
      shell = sshClient.invoke_shell()
    except:
      self.rootLogger.error("Could not get shell for host {0}. Probably lost the SSH connection".format(host))
      sshClient.close()
      return connected, returnCode, shell, output
    # Setting shell timeout
    shell.settimeout(self.config.get('SHELL_TIMEOUT'))
    # Disabling paging
    shell.send('{0}\n'.format(NO_PAGING_COMMAND))
    if self.enableFlag:
      shell.send('enable\n')
      shell.send(self.enablePassword + '\n')
    if self.device.use_enable_password:
      shell.send(b'enable\n')
      shell.send(enable_pass + '\n')
    sleep(1)
    # Read banner, prompts... and do nothing with them
    shell.recv(10000)
    # Reading returned configuration
    returnCode = self.getImageSize()
    
    #sshClient.close()
    return connected, returnCode, shell

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
    try:
      telnetClient.write((self.login + "\n").encode('ascii'))
    except:
      pass
    telnetClient.write((self.password + "\n").encode('ascii'))
    self.rootLogger.debug("Connected to host {0} using Telnet.".format(host)) 
    #telnetClient.write(str('{0}\n{1}\n'.format(str(self.login), str(self.password))))
    # Reading what's available without blocking
    # TODO: Remove below
    # telnetClient.write('enable\n{0}\n'.format(ENABLE_PASS))
    # telnetClient.read_lazy()
    # Sending command to avoid paging then remote command
    telnetClient.write((NO_PAGING_COMMAND + "\n").encode('ascii'))
    sleep(1)
    telnetClient.write(b'\n\n')
    sleep(0.3)
    if self.enableFlag:
      telnetClient.write(b'enable\n')
      telnetClient.write((self.enablePassword + '\n').encode('ascii'))
    if self.device.use_enable_password:
      telnetClient.write(b'enable\n')
      telnetClient.write((enable_pass + '\n').encode('ascii'))
    output = telnetClient.read_lazy()
    prompt = output.split(b'#')[0].strip()
    # FNO: Support $ prompt, too
    prompt = prompt.split(b'$')[0].strip()
    telnetClient.read_lazy()
    telnetClient.write((self.ftpCommand + '\n').encode('ascii'))
    telnetClient.write(('\n').encode('ascii'))
    if self.ftpProtocol == "ftp":
      telnetClient.write(('\n').encode('ascii'))
      telnetClient.write(('\n').encode('ascii'))
    telnetClient.write(("End-Of-File").encode('ascii'))
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
    returnCode = self.getImageSize()
    return connected, returnCode, telnetClient

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
   
  def installImage(self, shell):
    successInstall = False
    try:
      command = 'boot system ' + self.deviceStorage + self.imageFile +'\n'
      shell.send('configure terminal\n')
      shell.send('no boot system\n')
      shell.send(command)
      shell.send('exit\n')
      shell.send('write memory\n')
      shell.send('reload\n')
      sleep(2)
      self.rootLogger.debug("image installed successfully")
      successInstall = True
      
    except: 
      successInstall = False
    
    #dirOutput = shell.recv(10000)
    #self.rootLogger.debug('Checking for image file existence. Dir command output: \n{0}'.format(dirOutput))
    #if self.imageFile in str(dirOutput):
      #success = True
      
    return successInstall
   
  def processDevice(self):
    '''
    Thread function. Used to process hosts: configuration collection and key matching
    '''
    type = "SSH"
    result= {}
    self.updateTaskStatus(STATUS_ONGOING, setStartTime=True, setEndTime=False)
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
      result.update({"status": STATUS_FAILED, "configurations":"Could not find device"})
      self.task.result = result 
      return
    self.buildFtpCommand()
    host = device.name
    # Starting host processing for host
    self.rootLogger.debug("Processing device {0}.".format(device.name))
    # Get configuration using SSH
    connected, returnCode, shell = self.getConfUsingSSH(device.name)
    # if not connected:
      # Could not connect using SSH, fallback on Telnet
    #   connected, config = self.getConfUsingTelnet(host)
    if not connected:
      # Still could not connect using the fallback protocol. Log it as an error
      connected, returnCode, shell = self.getConfUsingTelnet(device.name)
      type = "TELNET"
      if not connected:
      # Still could not connect using the fallback protocol. Log it as an error
        self.rootLogger.error('Could not connect to to device {0} with any transport mechanism.'.format(device.name))
        self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
        data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
        self.sendToQueue(job_manager_producer, "job_manager", data)
        result.update({"status": STATUS_FAILED, "configurations":"NOT CONNECTED"})
        return
    usable, useoutput = self.checkDeviceUsable(shell, host, type)
    success, copyoutput = self.copyImage(shell, host, type)
    if not usable:
      self.rootLogger.error('Stopped processing for host {0}. Device is not usable.'.format(host))
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      result.update({"status": STATUS_FAILED, "configurations":useoutput})
      self.task.result = result 
      return
    if not success:
      self.rootLogger.error('Copy failed for host {0}'.format(host))
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      result.update({"status": STATUS_FAILED, "configurations":copyoutput})
      self.task.result = result 
      return
    copy, verifyoutput = self.verifyCopy(shell, type)
    if not copy:
      self.rootLogger.error('Image file not found on device for host {0}'.format(host))
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      result.update({"status": STATUS_FAILED, "configurations":verifyoutput})
      self.task.result = result 
      return
    if not returnCode:
      self.rootLogger.info('END: Script ended.')
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      result.update({"status": STATUS_FAILED, "configurations":"END: Script ended."})
      self.task.result = result
      return
    #successInstall = self.installImage(shell)
    """if not successInstall:
      self.rootLogger.error('installation failed'.format(host))
      self.updateTaskStatus(STATUS_FAILED, setEndTime=True)
      data = {"element_id":self.task.id,
              "status": STATUS_FAILED}
      self.sendToQueue(job_manager_producer, "job_manager", data)
      result.update({"status": STATUS_FAILED, "configurations":"installation failed."})
      return"""
    result.update({"status": STATUS_SUCCESSFUL, "configurations":"{}\n{}\n{}".format(useoutput,copyoutput,verifyoutput)})
    # Configuration collected ! Matching it with keys
    self.task.result = result 
    self.rootLogger.debug('Configuration for device {0}: \n'.format(device.name))
    self.rootLogger.debug("Extracted and saved configuration for device {0}.".format(device.name))
    # Out of while loop. Exiting thread
    self.updateTaskStatus(STATUS_SUCCESSFUL, setEndTime=True)
    data = {"element_id":self.task.id,
              "status": STATUS_SUCCESSFUL}
    self.sendToQueue(job_manager_producer, "job_manager", data)
    #self.processResult(matchedHosts)

@app.task(serializer='json', name=CONFIGURATION_IMAGE_LOADER_NAME)
def main_task(task_id):
  # Point of entry of the script.
  # Call the main function for the whole processing
  task = TaskModel.findById(task_id)
  job = JobModel.findById(task.job_id)
  configurationImageLoader = ConfigurationImageLoader(job, task)
  configurationImageLoader.processDevice()
