
# Create your views here.
from django.shortcuts import render
import requests
import json
import ast
import urllib
from datetime import datetime
from front.common import authetication_required

from front.configuration import *

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
KIBANA_PORT = '5601'


@authetication_required()
def workflowReportList(request):
  url = API_URI + '/workflow'
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: workflowListData = r.json()
  else: workflowListData = {}
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT
  return render(request, 'workflowReports/workflowReports.html', {'workflowListData': workflowListData,
                                                      'kibana_host':kibanaHost,
                                                      'message': API_URI})



@authetication_required()
def JobReportList(request):
  workflow_id = request.GET.get('workflow_id')
  url = API_URI + '/job?workflow_id=' + workflow_id
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: job_list = r.json()["jobs"]
  for job in job_list:
    if job['parameters'].get('first_in_workflow') == True:
      first_job = job["id"]
  url = API_URI + '/link?workflow_id=' + workflow_id
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: link_list = r.json()["links"]
  url = API_URI + '/eval?workflow_id=' + workflow_id
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: eval_list = r.json()["evals"]
  for eval in eval_list:
    if eval["status"] == None:
        eval["status"] = "NEW"
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT
  return render(request, 'workflowReports/workflowStaticReports.html', {'job_list': json.dumps(job_list),
                                                                        'first_job': first_job,
                                                                        'workflow_id': workflow_id,
                                                                        'eval_list': json.dumps(eval_list),
                                                                        'link_list': json.dumps(link_list),
                                                                        'kibana_host':kibanaHost,
                                                                        'message': API_URI})


