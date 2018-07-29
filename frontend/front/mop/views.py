# Create your views here.
from django.shortcuts import render
import requests
import json
import ast
import urllib
from front.common import authetication_required
import configparser
import csv

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
code_list = [404, 401, 402, 500, 400]
API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))
global_data = ['name',
               'description',
               'login',
               'password',
               'useDeviceCredentials',
               'useEnablePassword',
                      ]
BOOLEAN_FIELDS = ['use_device_credentials',
                  'use_enable_password',
                  'is_validated']
HOSTS = ['element',
         'value',
         'device',
    ]
def convertCsvToArray(fileString):
        '''Converts a CSV string to an array'''
        string = fileString.decode('utf-8')
        unformattedDevices = list(csv.reader(str(string).split('\n'), delimiter=','))
        if not unformattedDevices[-1]: del unformattedDevices[-1]
        return unformattedDevices    

@authetication_required()
def workflowList(request, response = {}):
  url = API_URI + '/workflow'
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: workflowListData = r.json()
  else: workflowListData = {}
  if(request.GET.get('delete_workflow')):
    data = request.GET
    url = API_URI + '/workflow/{0}'.format(data["delete_workflow"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.delete(url, headers=headers)
    response = r.text
  url = API_URI + '/workflow'
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: workflowListData = r.json()
  else: workflowListData = {}
  return render(request, 'workflow/workflow.html', {'workflowListData': workflowListData,
                                            'response': response})

@authetication_required()
def workflowDelete(request):
  if(request.POST.get('logout')):
    del request.session['jwt_token']
    return render(request, 'login.html')
  if(request.GET.get('delete_workflow')):
    data = request.GET
    url = API_URI + '/workflow/{0}'.format(data["delete_workflow"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.delete(url, headers=headers)
    response = r.text
  return render(request, 'workflow/workflow.html', {'response': 'workflow deleted'})

@authetication_required()
def workflowEdit(request):
  if(request.POST.get('logout')):
    del request.session['jwt_token']
    return render(request, 'login.html')
  response = {}
  url = API_URI + '/job'
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  get_location = requests.get(API_URI + '/locations', headers=headers)
  localisation = get_location.json()

  get_group = requests.get(API_URI + '/groups', headers=headers)
  group = get_group.json()

  get_deviceClass = requests.get(API_URI + '/deviceClasses', headers=headers)
  deviceClass = get_deviceClass.json() 
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jobListData = r.json()
  else: jobListData = {}
  precheck_list = []
  for precheck in jobListData["jobs"]:
    if precheck["agent_type"] == "configuration_differ_precheck":
      precheck_list.append(precheck)
  if request.POST.get("workflow_data"):
    workflow_data = request.POST.get("workflow_data")
    hostList = request.POST.get('host_list')
    hostFilter= request.POST.get('hostFilter')
    data = ast.literal_eval(workflow_data)
    data["hosts"] = {}
    data["hosts"]["host_list"] = []    
    if hostList:
      data["hosts"]["hostsType"] = "hostList"
      host_list = hostList.split("\r\n")
      for host in host_list: 
        if host != '':
          data["hosts"]["host_list"].append(host)
    else:
      data["hosts"]["hostsType"] = "hostFilter"
      data['hosts']["host_list"] = [{"element":data["element"],
                                   "value":data["value"],
                                   "device":data["device"],}]
    if data.get("job_list") and data.get("job_list") != []:
      for job in data["job_list"]:
        if job == data["start"]:
          data["job_list"][job]["parameters"]["first_in_workflow"] = True
        if data["job_list"][job]["agent_type"] == "configuration_parser":
          data["job_list"][job]["parameters"]["keyList"] = data["job_list"][job]["parameters"]["keyList"].split(",")
        if data["job_list"][job]["agent_type"] == "configuration_sender":
          data["job_list"][job]["parameters"]["remoteCommand"] = data["job_list"][job]["parameters"]["remoteCommands"]
        data["job_list"][job]["login"] = data["login"]
        data["job_list"][job]["password"] = data["password"]
        data["job_list"][job]["hostsType"] = data["hosts"]["hostsType"]
        data["job_list"][job]["hosts"] = data["hosts"]["host_list"]
    
      url = API_URI + '/workflow'
      headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
      r = requests.post(url, data=json.dumps(data), headers=headers)
      if r.status_code == 201: response = "Workflow Created"
      elif r.status_code in code_list: response = r.text
      else: response = "Unknown Error"
    else: response = "Can not create the workflow, missing data"
    return workflowList(request, response)
  
  if request.POST.get("send_workflow"):
    data = request.POST
    url = API_URI + '/workflow'
    headers = {'Content-Type' : 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Workflow Created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
  return render(request, 'workflow/new_workflow.html', {'response': response,
                                                        'deviceClass': deviceClass,
                                                        'localisation': localisation,
                                                        'group': group,
                                                        'precheck_list': json.dumps(precheck_list)})

