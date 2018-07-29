from django.shortcuts import render
import requests
import json
import ast
import urllib
import csv
from django.http import HttpResponse
from front.common import authetication_required
import configparser
from cryptography.fernet import Fernet
KEY = "inpJc86QUnMxANQl8iKfmRS8iAruYOK4Pm--Qz_UpYE="
response = ''
code_list = [404, 401, 402, 500, 400]
BASIC_FIELDS = [ 'name',
                 'ipAddress',
                 'category',
                 'SNMP_Community',
                 'SNMP_Version',
                 'login',
                 'password',
                 'enable_pass',
                 ]
INT_FIELDS = ['deviceClass',
              'location',
              'group',
             ]
BOOLEAN_FIELDS = ['use_enable_password',]

FILTER_FIELDS = ["name", "parent_id"]

DEVICE_FIELDS = BASIC_FIELDS + INT_FIELDS + BOOLEAN_FIELDS
parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))

KIBANA_URL = parser.get('ELK_STACK_SECTION', 'KIBANA_HOST')
KIBANA_PORT = parser.get('ELK_STACK_SECTION', 'KIBANA_PORT')
KIBANA_URL_SUFFIX = parser.get('ELK_STACK_SECTION', 'KIBANA_URL_SUFFIX')
def Login(request):
  message = ""
  if(request.POST.get('login_form')):
    data = request.POST
    d={}
    d.update({"username": data["username"], "password": data["password"]})
    url = API_URI +'/auth'
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(d), headers=headers)
    response = r.json()
    if response.get("access_token"):
      request.session['jwt_token'] = response["access_token"]
      host = request.META.get('HTTP_HOST', 'localhost')
      hostname = host.split(':')[0]
      kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT + KIBANA_URL_SUFFIX
      return render(request, 'home.html', {'kibana_host':kibanaHost})
    else: 
      message = "The username or password that you've entered are not correct."
      return render(request, 'login.html',{'message': message})
  return render(request, 'login.html',{'message': message})

def TaskReportList(request):
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT + KIBANA_URL_SUFFIX
  device_id = request.GET.get('device_id')
  url = API_URI + '/task?device_id=' + device_id
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  task_result = requests.get(url, headers=headers)
  if task_result.status_code == 200: jsonData = task_result.json()
  else: jsonData = {}

  job_url = API_URI + '/job/' + jobId
  job_result = requests.get(job_url, headers=headers)
  if job_result.status_code == 200:
    job_jsonData = job_result.json()
  else:
    job_jsonData = {}

  jsonData = get_tasks_info(jsonData, headers)

  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT
  return render(request, 'reports/task_reports.html', {'tasks': jsonData,
                                                       'job_id': jobId,
                                                       'job': job_jsonData,
                                                       'kibana_host':kibanaHost,
                                                       'message': task_result.text})
@authetication_required()
def Index(request):
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT + KIBANA_URL_SUFFIX
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT + KIBANA_URL_SUFFIX
  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')
  return render(request, 'home.html',{'kibana_host':kibanaHost})


@authetication_required()
def Device(request):
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT + KIBANA_URL_SUFFIX
  """global section"""
  response = ''
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  devices = requests.get(API_URI +'/devices', headers=headers)
  device_list = devices.json()
  if device_list.get('devices'):
    for device in device_list.get('devices'):
      cipher_suite = Fernet(KEY)
      if device.get('login'):
        device['login'] = cipher_suite.decrypt(device['login'].encode('ascii')).decode('ascii')
      if device.get('password'):
        device['password'] = cipher_suite.decrypt(device['password'].encode('ascii')).decode('ascii')
  get_location = requests.get(API_URI +'/locations', headers=headers)
  location_list = get_location.json()

  get_group = requests.get(API_URI +'/groups', headers=headers)
  group_list = get_group.json()

  get_deviceClass = requests.get(API_URI +'/deviceClasses', headers=headers)
  deviceClass_list = get_deviceClass.json()  

  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')

  """device section"""
  
  if(request.GET.get('delete_device')):
    data = request.GET
    url = API_URI +'/device/{0}'.format(data["delete_device"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.delete(url, headers=headers)
    response = r.text
    
  if(request.POST.get('new_device')):
    data = {k:request.POST.get(k) for k in DEVICE_FIELDS}
    for f in INT_FIELDS:
        try:
          data[f] = int(data[f])
        except:
          del(data[f])
    for b in BOOLEAN_FIELDS:
      if b in data:
        try:
          data[b] = True if data[b].lower() == 'true' else False
        except: pass
    url = API_URI +'/device/{0}'.format(data["name"]) 
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Device created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    return render(request, 'devices.html', {'response': response,
                                            'deviceClass_list': deviceClass_list,
                                            'location_list': location_list,
                                            'group_list': group_list,
                                            'devices': device_list,
                                            'kibana_host':kibanaHost,})
    
  
  if(request.GET.get('edit_device')):
    data = {k:request.GET.get(k) for k in DEVICE_FIELDS}
    for f in INT_FIELDS:
      try:
        data[f] = int(data[f])
      except:
        del(data[f])
    for b in BOOLEAN_FIELDS:
      if b in data:
        try:
          data[b] = True if data[b].lower() == 'true' else False
        except: pass
    url = API_URI +'/device/{0}'.format(data["name"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Device edited"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    return render(request, 'devices.html', {'response': response,
                                            'deviceClass_list': deviceClass_list,
                                            'location_list': location_list,
                                            'group_list': group_list,
                                            'devices': device_list,
                                            'kibana_host':kibanaHost,})
    
  """for dev in device_list["devices"]: 
    if(request.GET.get(dev["name"])):
      url = API_URI +'/device/{0}'.format(dev["name"])
      headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
      r = requests.delete(url, headers=headers)
      response = r.text
      return render(request, 'devices.html', {'response': response,
                                            'deviceClass_list': deviceClass_list,
                                            'location_list': location_list,
                                            'group_list': group_list,
                                            'devices': device_list,
                                            'kibana_host':kibanaHost,})"""

  """group section"""
  
  if(request.POST.get('new_group')):
    data = {k:request.POST.get(k) for k in FILTER_FIELDS}
    try:
      data['parent_id'] = int(data['parent_id'])
    except:
      del(data['parent_id'])
    url = API_URI +'/group/{0}'.format(data["name"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Group with name {} created".format(data["name"])
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  if(request.GET.get('edit_group')):
    data = {k:request.POST.get(k) for k in FILTER_FIELDS}
    try:
      data['parent_id'] = int(data['parent_id'])
    except:
      data['parent_id'] == None
    url = API_URI +'/group/{0}'.format(data["edit_group"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Group created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  if(request.GET.get('delete_device_from_group')):
    data = request.GET
    name = data["delete_device_from_group"]
    url = API_URI +'/device/{0}'.format(name)
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    
    
  if(request.GET.get('delete_group')):
    data = request.GET
    name=data["delete_group"]
    url = API_URI +'/group/{0}'.format(name)
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.delete(url, data=json.dumps(data), headers=headers)

  for grp in group_list["groups"]:
    if(request.GET.get(grp["name"])):
      
      click_group = grp["name"]
      render(request, 'devices.html', {'location_list': location_list,
                                       'group_list': group_list,
                                       'devices': device_list,
                                       'click_group': click_group,
                                       'kibana_host':kibanaHost,
                                          })
      return render(request, 'group_block.html', {
                                                 'group_list': group_list,
                                                 'location_list': location_list,
                                                 'deviceClass_list': deviceClass_list,
                                                 'click_group': click_group,
                                                 'devices': device_list,
                                                 'kibana_host':kibanaHost,
                                                 })
      
  """location section"""
  
  if(request.POST.get('new_location')):
    data = {k:request.POST.get(k) for k in FILTER_FIELDS}
    try:
      data['parent_id'] = int(data['parent_id'])
    except:
      del(data['parent_id'])
    url = API_URI +'/location/{0}'.format(data["name"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Location with name {} created".format(data["name"])
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  if(request.GET.get('edit_location')):
    data = {k:request.POST.get(k) for k in FILTER_FIELDS}
    try:
      data['parent_id'] = int(data['parent_id'])
    except:
      data['parent_id'] == None
    url = API_URI +'/location/{0}'.format(data["edit_location"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Location with name {} created".format(data["name"])
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  if(request.GET.get('delete_device_from_location')):
    data = request.GET
    name = data["delete_device_from_location"]
    url = API_URI +'/device/{0}'.format(data["delete_device_from_location"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    
    
  if(request.GET.get('delete_location')):
    data = request.GET
    name=data["delete_location"]
    url = API_URI +'/location/{0}'.format(name)
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    
    
  if(request.GET.get('delete_device_from_location')):
    data = request.GET
    name = data["delete_device_from_location"]
    url = API_URI +'/device/{0}'.format(name)
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    
    
  for loc in location_list["locations"]:
    if(request.GET.get(loc["name"])):
      click_location = loc["name"]
      render(request, 'devices.html', {'location_list': location_list,
                                          'location_list': location_list,
                                          'devices': device_list,
                                          'click_location': click_location,
                                          'kibana_host':kibanaHost,
                                          })
      return render(request, 'location_block.html', {
                                                 'group_list': group_list,
                                                 'location_list': location_list,
                                                 'deviceClass_list': deviceClass_list,
                                                 'click_location': click_location,
                                                 'devices': device_list,
                                                 'kibana_host':kibanaHost,
                                                 })

  """deviceClass section"""
  
  if(request.POST.get('new_deviceClass')):
    data = {k:request.POST.get(k) for k in FILTER_FIELDS}
    try:
      data['parent_id'] = int(data['parent_id'])
    except:
      del(data['parent_id'])
    url = API_URI +'/deviceClass/{0}'.format(data["name"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Device Class with name {} created".format(data["name"])
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  if(request.GET.get('edit_deviceClass')):
    data = request.GET
    url = API_URI +'/deviceClass/{0}'.format(data["edit_deviceClass"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Device Class with name {} created".format(data["name"])
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  if(request.GET.get('delete_device_from_deviceClass')):
    data = request.GET
    value = {"deviceClass": ""}
    name = data["delete_device_from_deviceClass"]
    url = API_URI +'/device/{0}'.format(data["delete_device_from_deviceClass"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=value["deviceClass"], headers=headers)
    
    
  if(request.GET.get('delete_deviceClass')):
    data = request.GET
    name=data["delete_deviceClass"]
    url = API_URI +'/deviceClass/{0}'.format(name)
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    
    
  if(request.GET.get('delete_device_from_deviceClass')):
    data = request.GET
    name = data["delete_device_from_deviceClass"]
    url = API_URI +'/device/{0}'.format(name)
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    
    
  for devclass in deviceClass_list["deviceClasses"]:
    if(request.GET.get(devclass["name"])):
      click_deviceClass = devclass["name"]
      render(request, 'devices.html', {'location_list': location_list,
                                          'deviceClass_list': deviceClass_list,
                                          'devices': device_list,
                                          'group_list': group_list,
                                          'click_deviceClass': click_deviceClass,
                                          'kibana_host':kibanaHost,
                                          })
      return render(request, 'deviceClass_block.html', {
                                                 'deviceClass_list': deviceClass_list,
                                                 'location_list': location_list,
                                                 'group_list': group_list,
                                                 'devices': device_list,
                                                 'click_deviceClass': click_deviceClass,
                                                 'kibana_host':kibanaHost,
                                                 })
  
  if(request.GET.get('delete_from_tree')):
    data = request.GET
    name=data["delete_from_tree"]
    if data["type"] == 'group':
      url = API_URI +'/group/{0}'.format(name)
    if data["type"] == 'location':
      url = API_URI +'/location/{0}'.format(name)
    if data["type"] == 'deviceClass':
      url = API_URI +'/deviceClass/{0}'.format(name)
    
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.delete(url, data=json.dumps(data), headers=headers)
    if r.status_code == 202: response = "Group with name {} deleted".format(name)
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"

  if(request.GET.get('edit_from_tree')):
    data = request.GET
    name=data["edit_from_tree"]
    if data["type"] == 'group':
      url = API_URI +'/group/{0}'.format(name)
    if data["type"] == 'location':
      url = API_URI +'/location/{0}'.format(name)
    if data["type"] == 'deviceClass':
      url = API_URI +'/deviceClass/{0}'.format(name)
      
    headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Group with name {} edited".format(name)
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}  
  devices = requests.get(API_URI +'/devices', headers=headers)
  device_list = devices.json()

  get_location = requests.get(API_URI +'/locations', headers=headers)
  location_list = get_location.json()

  get_group = requests.get(API_URI +'/groups', headers=headers)
  group_list = get_group.json()


  get_deviceClass = requests.get(API_URI +'/deviceClasses')
  deviceClass_list = get_deviceClass.json()
  return render(request, 'devices.html', {'response': response,
                                          'location_list': location_list,
                                          'group_list': group_list,
                                          'devices': device_list,
                                          'deviceClass_list': deviceClass_list,
                                          'kibana_host':kibanaHost,
                                          })
  
  
  
  
@authetication_required()
def DeviceReport(request):
  deviceId = request.GET.get('device_id')
  job_list = []
  url = API_URI + '/task?device_id=' + deviceId
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  task_result = requests.get(url, headers=headers)
  if task_result.status_code == 200: jsonData = task_result.json()
  else: jsonData = {}
  job_url = API_URI + '/job'
  job_result = requests.get(job_url, headers=headers)
  if job_result.status_code == 200:
    job_jsonData = job_result.json()
  else:
    job_jsonData = {}
  for task in jsonData["tasks"]:
    for job in job_jsonData["jobs"]:
      if job["id"] == task["job_id"]:
        job["task_status"] = task["status"]
        job["result"] = task["result"]
        job_list.append(job)

  #job_id = jsonData["tasks"][0]["job_id"]
  
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT
  return render(request, 'device_reports.html', {'tasks': jsonData,
                                                 'response': response,
                                                       'device_id': deviceId,
                                                       'jobs': job_list,
                                                       'kibana_host':kibanaHost,
                                                       'message': task_result.text})
  