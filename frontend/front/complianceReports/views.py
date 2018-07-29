from django.shortcuts import render
import json
from front.common import authetication_required
import requests
import configparser
import logging
import ast
import csv

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
code_list = [404, 401, 402, 500, 400]
API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))

global_data = ['name',
               'login',
               'password',
                      ]
BOOLEAN_FIELDS = ['use_device_credentials',
                  'use_enable_password',
                  'is_validated']

def convertCsvToArray(fileString):
    '''Converts a CSV string to an array'''
    string = fileString.decode('utf-8')
    unformattedDevices = list(csv.reader(str(string).split('\n'), delimiter=','))
    if not unformattedDevices[-1]: del unformattedDevices[-1]
    return unformattedDevices

def complianceReportsList(request):
  response = ""
  data = {}
  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')
  url = API_URI + '/compliance_report'
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jsondata = r.json()
  else: jsondata = {}
  if(request.GET.get('execute_compliance')):
    url = API_URI + '/compliance_execution'
    data["compliance_id"] = int(request.GET.get('execute_compliance'))
    r = requests.post(url, data=json.dumps(data), headers=headers)
  if(request.GET.get('delete_compliance')):
    url = API_URI + '/compliance_report/' + str(request.GET.get('delete_compliance'))
    r = requests.delete(url, headers=headers)
    if r.status_code == 202: response = "Report Deleted"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
  url = API_URI + '/compliance_report'
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jsondata = r.json()
  else: jsondata = {}
  return render(request, 'complianceReports/complianceReports.html', {'jsondata': jsondata,
                                                      'message': API_URI,
                                                      'response': response})
  
  
  

@authetication_required()   
def complianceReportsCreate(request):
  response = ""
  if(request.POST.get('logout')):
      del request.session['jwt_token']   
      return render(request, 'login.html')
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  get_location = requests.get(API_URI + '/locations', headers=headers)
  localisation = get_location.json()

  get_group = requests.get(API_URI + '/groups', headers=headers)
  group = get_group.json()
  get_deviceClass = requests.get(API_URI + '/deviceClasses', headers=headers)
  deviceClass = get_deviceClass.json()
  
  if(request.GET.get('execute_compliance')):
    url = API_URI + '/compliance_execution'
    data["compliance_id"] = int(request.GET.get('execute_compliance'))
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return complianceReportsList(request)
  if request.POST:
    data = request.POST
    jsondata = {}
    jsondata["elements"] = []
    jsondata['name'] = request.POST.get("global_name")
    jsondata['description'] = request.POST.get("global_description")
    jsondata['login'] = request.POST.get("global_login")
    jsondata['password'] = request.POST.get("global_password")
    for element in ast.literal_eval(request.POST.get("element_list_data")):
      jsondata["elements"].append(element)
    """except:
      jsondata["elements"] = []"""
    jsondata['use_device_credentials'] = request.POST.get("use_device_credentials")
    jsondata['use_enable_password'] = request.POST.get("use_enable_password")
    jsondata['is_validated'] = request.POST.get("is_validated")
    hostList = request.FILES.get('hostFile')
    if hostList:
      jsondata['hostsType'] = 'hostList'
      jsondata['host_list'] = [h[0] for h in convertCsvToArray(hostList.read())]
      
    elif request.POST.get('hostsType') == "hostFilter":
      if "deviceClass" in request.POST.get('element'):
        element = "deviceClass"
      if "group" in request.POST.get('element'):
        element = "group"
      if "location" in request.POST.get('element'):
        element = "location"
      data['hosts'] = [{"element":element,
                      "value":request.POST.get('value'),
                      "device":request.POST.get('device'),}]
    url_compliance = API_URI + '/compliance_report'
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.post(url_compliance, data=json.dumps(jsondata), headers=headers)
    if r.status_code == 201: response = "Report Created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    return complianceReportsList(request)
  return render(request, 'complianceReports/ComplianceReportsCreate.html', {
                                            'deviceClass': deviceClass,
                                            'localisation': localisation,
                                            'group': group,
                                            'response': response,
                                            }
                                            )

@authetication_required()   
def complianceExecutionList(request):
  response = ""
  jsonData = {}
  data = {}
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  compliance_id = request.GET.get('compliance_id')
  if(request.GET.get('execute_compliance')):
    url = API_URI + '/compliance_execution'
    data["compliance_id"] = int(request.GET.get('execute_compliance'))
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Report Executed"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
    compliance_id = str(request.GET.get('execute_compliance'))
  if(request.GET.get('delete_compliance_execution')):
    url = API_URI + '/compliance_execution/' + str(request.GET.get('delete_compliance_execution'))
    r = requests.delete(url, headers=headers)
    compliance_id = request.GET.get('compliance_id')
    if r.status_code == 202: response = "Report Execution Deleted"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error"
  url_compliance_execution = API_URI + '/compliance_execution?compliance_id=' + compliance_id
  compliance_execution_list = requests.get(url_compliance_execution, headers=headers)
  jsonData["execution_list"] = compliance_execution_list.json()["compliance_executions"]
  return render(request, 'complianceReports/complianceExecutionList.html', {'jsondata': jsonData,
                                                                            'compliance_id': compliance_id,
                                                                            'response':response,
                                                                            })
@authetication_required()   
def complianceReportView(request):
  jsonData = {}
  compliance_execution_id = request.GET.get('compliance_execution_id')
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  url_compliance_execution = API_URI + '/compliance_execution/' + compliance_execution_id
  global_compliance_execution = requests.get(url_compliance_execution, headers=headers)
  compliance_id = global_compliance_execution.json()["compliance_id"]
  url_compliance = API_URI + '/compliance_report/' + str(compliance_id)
  global_compliance = requests.get(url_compliance, headers=headers)
  jsonData["global_compliance"] = global_compliance.json()
  url_element = API_URI + '/compliance_element?compliance_id=' + str(compliance_id)
  element_list = requests.get(url_element, headers=headers)
  jsonData["elements"] = []
  if element_list.status_code == 200:
    for element in element_list.json()["compliance_elements"]:
      url_check = API_URI + '/check?compliance_element_id=' + str(element["id"])
      check_list = requests.get(url_check, headers=headers)
      #for check in check_list.json()["checks"]:
      check_result_url = API_URI + '/check_result?compliance_execution_id=' + str(compliance_execution_id)
      check_result_list = requests.get(check_result_url, headers=headers)
      #for check_result in check_result_list.json()["check_results"]:
      #check_result_id = check_result["id"]
      rule_list = []
      for check in element["checks"]:
        check["failed_result_list"] = []
        check["successful_result_list"] = []
        failed_result = 0
        successful_result = 0
        for check_result in check_result_list.json()["check_results"]:
          if check_result["check_id"] == check["id"]:
            if check_result["status"] == "FAILED":
              if check_result["device_name"] not in check["failed_result_list"]:
                check["failed_result_list"].append(check_result["device_name"])
            elif check_result["status"] == "SUCCESSFUL":
              if check_result["device_name"] not in check["successful_result_list"]:
                check["successful_result_list"].append(check_result["device_name"])
        check["successful_result"] = len(check["successful_result_list"])
        check["failed_result"] = len(check["failed_result_list"])
        check["rule_list"] = []
        for rule in check["rules"]:
          check["rules"][rule]["id"] = rule
          check["rule_list"].append(check["rules"][rule])
      jsonData["elements"].append({"element_information": element, "check_results": check_result_list.json()["check_results"]})
  else:
    jsonData["elements"] = {}
  """if check_list.status_code == 200:
    jsonData["check_list"] = check_list.json()
  else:
    jsonData["check_list"] = {}
  if job_result.status_code == 200:
    job_jsonData = job_result.json()
  else:
    job_jsonData = {}"""
  #jsonData = get_tasks_info(jsonData, headers)
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  return render(request, 'complianceReports/complianceReportView.html', {'jsondata': jsonData,
                                                      })
  