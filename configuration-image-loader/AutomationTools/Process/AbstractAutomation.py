#!/usr/bin/env python

from AutomationTools.models.device import DeviceModel
from cryptography.fernet import Fernet

KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="

class AbstractAutomation(object):

  def __init__(self, job, task):
    self.device = DeviceModel.findById(task.device_id)
    cipher_suite = Fernet(KEY) 
    if job.use_device_credentials == True:
      try:
        self.login = cipher_suite.decrypt(job.login.encode('ascii')).decode('ascii')
      except:
        self.login = ""
      try:
        self.password = cipher_suite.decrypt(job.password.encode('ascii')).decode('ascii')
      except:
        self.password = ""
      if self.device.use_enable_password:
        try:
          self.enablePassword = cipher_suite.decrypt(job.enable_password.encode('ascii')).decode('ascii')
        except:
          self.enablePassword = ""
      self.enableFlag = self.device.use_enable_password
    else:
      try:
        self.login = cipher_suite.decrypt(job.login.encode('ascii')).decode('ascii')
      except:
        self.login = ""
      try:
        self.password = cipher_suite.decrypt(job.password.encode('ascii')).decode('ascii')
      except:
        self.password = ""
      if job.use_enable_password:
        try:
          self.enablePassword = cipher_suite.decrypt(job.enable_password.encode('ascii')).decode('ascii')
        except:
          self.enablePassword = ""
      self.enableFlag = job.use_enable_password
    self.job = job
    self.task = task