from django.shortcuts import render
import requests
import json
import ast
import urllib
import logging
import csv
from front.common import authetication_required
import configparser
import codecs 
from io import TextIOWrapper
from io import StringIO
from cryptography.fernet import Fernet

KEY = '8DtOqWlTkPPWN9lDKPVoyX4GsOM_dwpfXlHu-1mErrE='
code_list = [404, 401, 402, 500, 400]
parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))

def convertCsvToArray(fileString):
    '''Converts a CSV string to an array'''
    string = fileString.decode('utf-8')
    unformattedDevices = list(csv.reader(str(string).split('\n'), delimiter=','))
    if not unformattedDevices[-1]: del unformattedDevices[-1]
    return unformattedDevices

def convertCsvToJson(fileString):
    '''Converts a CSV string to a JSON'''
    jsonobj = {}
    f = TextIOWrapper(fileString.file)
    st = fileString.read()
    string = st.decode('utf-8')
    dlm = string[5]
    #list = string.split("\r\n")
    """for element in list:
      element2 = element.split(",")
      list2.append(element2)
    for ele in list2:
      for i in range(1,len(list2[0])):
        #jsonobj.update({list2[i][0]:{element2[i][0]:element2[i][0]}})  
        jsonobj.update({ele[0]:{element2[0][i]:ele[i]}})"""
    #dialect = csv.Sniffer().sniff(codecs.EncodedFile(fileString, "utf-8").read(1024))
    reader = csv.DictReader(StringIO(string),delimiter=dlm)
    for row in reader:
      element = {}
      element.update(row)
      first_element = next(iter(dict(row)))
      del(element[first_element])
      jsonobj.update({dict(row)[first_element]:element})
    return jsonobj

COMMON_AGENT_FIELDS = ['name',
                       'description',
                       'agent_type',
                       'login',
                       'password',
                       'enable_password',
                       'hostsType',
                       'use_device_credentials',
                       'use_enable_password',
                       'is_scheduled',
                       'schedule_time',
                       'is_validated',
                      ]
CONFIGURATION_PARSER_FIELDS = ['remoteCommand',
                               'strictMatching',
                               'keyList'
                                ]

CONFIGURATION_SENDER_FIELDS = ['remoteCommand'
                            # 'remoteCommand' as array (split)
                               ]
DIFFER_POSTCHECK_FIELDS = ['jobID'
                           ]
CONFIGURATION_DIFFER_PRECHECK_FIELDS = ['remoteCommand',
                          'strictMatching',
                          'keyList'
                          ]
IMAGE_LOADER_FIELDS = ['deviceStorage',
                       'ftpServer',
                       'ftpProtocol',
                       'ftpPort',
                       'ftpUser',
                       'ftpPassword',
                       'ftpImage'
                       ]

BOOLEAN_FIELDS = ['use_device_credentials',
                  'use_enable_password',
                  'is_scheduled',
                  'is_validated',
                  ]
HOSTS = ['element',
         'value',
         'device',
         ]

AGENT_FIELDS = {'configuration_parser':[COMMON_AGENT_FIELDS, CONFIGURATION_PARSER_FIELDS, BOOLEAN_FIELDS, HOSTS],
                'configuration_sender':[COMMON_AGENT_FIELDS, CONFIGURATION_SENDER_FIELDS, BOOLEAN_FIELDS, HOSTS],
                'configuration_differ_postcheck':[COMMON_AGENT_FIELDS, DIFFER_POSTCHECK_FIELDS, BOOLEAN_FIELDS, HOSTS],
                'configuration_differ_precheck':[COMMON_AGENT_FIELDS, CONFIGURATION_DIFFER_PRECHECK_FIELDS, BOOLEAN_FIELDS, HOSTS],
                'configuration_image_loader':[COMMON_AGENT_FIELDS, IMAGE_LOADER_FIELDS, BOOLEAN_FIELDS, HOSTS]
                }


@authetication_required()
def JobList(request, res=None):
  response={}
  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')
  url = API_URI + '/job'
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}

  r = requests.get(url, headers=headers)
  if r.status_code == 200: jobListData = r.json()
  else: jobListData = {}
  if(request.GET.get('delete_job')):
    data = request.GET
    url = API_URI + '/job/{0}'.format(data["delete_job"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.delete(url, headers=headers)
    response = r.text
    url = API_URI + '/job'
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jobListData = r.json()
  else: jobListData = {}
  """for job in jobListData["jobs"]:
    if job.get('compliance_execution_id') or job.get('workflow_id'):
      jobListData["jobs"].remove(job)"""
  if res:
    response = res
  return render(request, 'jobs/jobs.html', {'jobListData': jobListData,
                                            'response': response})

@authetication_required()
def JobDelete(request):
  response = {}
  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')
  if(request.GET.get('delete_job')):
    data = request.GET
    url = API_URI + '/job/{0}'.format(data["delete_job"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.delete(url, headers=headers)
    response = r.text
  return JobList(request, response)
"""
def JobEdit(request):
  response = {}
  if request.method == 'POST':
    data = request.POST
    url = API_URI + '/job/'
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 200: response = r.json()
    else: response = r.text
  return render(request, 'jobs/new_job.html', {'response': response})
"""

@authetication_required()
def JobEdit(request):
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    get_location = requests.get(API_URI + '/locations', headers=headers)
    localisation = get_location.json()

    get_group = requests.get(API_URI + '/groups', headers=headers)
    group = get_group.json()

    get_deviceClass = requests.get(API_URI + '/deviceClasses', headers=headers)
    deviceClass = get_deviceClass.json()  
    url = API_URI + '/job'
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.get(url, headers=headers)
    if r.status_code == 200: jobListData = r.json()
    else: jobListData = {}
    if(request.POST.get('logout')):
      del request.session['jwt_token']   
      return render(request, 'login.html')
    return render(request, 'jobs/new_job.html', {
                                            'deviceClass': deviceClass,
                                            'localisation': localisation,
                                            'group': group,
                                            'jsondata': jobListData})

def getAgentParameters(request, outputData):
    if request.POST.get('agent_type') == 'configuration_parser':
      outputData['parameters']['keyList'] = outputData['parameters']['keyList'].split(",")
    
@authetication_required()   
def JobCreate(request):
  response = {}
  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')
  agent_type = request.POST.get('agent_type')
  try:
    agentFields = AGENT_FIELDS[agent_type]
    data = {k:request.POST.get(k) for k in agentFields[0]}
    if data["use_enable_password"] == None:
      data["use_enable_password"] = 'false'
    data['parameters'] = {k:request.POST.get(k) for k in agentFields[1]}
    getAgentParameters(request, data)
    hostList = request.FILES.get('hostFile')
    hostsConfiguration = request.FILES.get('hostCommandFile')
    hostFilter = request.POST.get('hostFilter')
    data["schedule_time"]=str(data["schedule_time"])
    if hostList:
      data['hostsType'] = 'hostList'
      data['hosts'] = [h[0] for h in convertCsvToArray(hostList.read())]
      data["parameters"]['remoteCommand'] = request.POST.get('remoteCommand')
    elif hostsConfiguration:
      data['hostsType'] = 'hostsConfiguration'
      data["parameters"]['hostsConfiguration'] = convertCsvToJson(hostsConfiguration)
      data["parameters"]['remoteCommand'] = request.POST.get('templateCommands')
    elif data['hostsType'] == "hostFilter":
      if "deviceClass" in request.POST.get('element'):
        element = "deviceClass"
      if "group" in request.POST.get('element'):
        element = "group"
      if "location" in request.POST.get('element'):
        element = "location"
      data['hosts'] = [{"element":element,
                      "value":request.POST.get('value'),
                      "device":request.POST.get('device'),}]
      data["parameters"]['remoteCommand'] = request.POST.get('remoteCommand')
    for b in BOOLEAN_FIELDS:
      if b in data:
        try:
          data[b] = True if data[b].lower() == 'true' else False
        except: pass
    url = API_URI + '/job'
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Job created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
  except: pass
  return JobList(request, response)
