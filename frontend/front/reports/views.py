
# Create your views here.

from django.shortcuts import render
import requests
from datetime import datetime
from front.common import authetication_required

from front.configuration import *
import json
import csv
from django.http.response import HttpResponse 
import unicodecsv

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
KIBANA_PORT = '5601'


@authetication_required()
def JobReportList(request):
  url = API_URI + '/job'
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jsondata = r.json()
  else: jsondata = {}
  """for job in jsondata["jobs"]:
    if not job.get('compliance_execution_id') or not job.get('workflow_id'):
      jsondata["jobs"].remove(job)"""
  host = request.META.get('HTTP_HOST', 'localhost')
  hostname = host.split(':')[0]
  kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT
  return render(request, 'reports/job_reports.html', {'jsondata': jsondata,
                                                      'kibana_host':kibanaHost,
                                                      'message': API_URI})


def get_tasks_info(jsonData, headers):
    for task in jsonData.get('tasks', []):
        r = requests.get(API_URI + '/device?id={}'.format(task['device_id']), headers=headers)
        if r.status_code != 200 or r.json()['devices'] == []:
            task['device_name'] = 'unknown({})'.format(task['device_id'])
        else:
            task['device_name'] = r.json()['devices'][0]['name']
        del task['device_id']
        if task['processing_start_time'] and task['processing_end_time']:
            startTime = datetime.strptime(task['processing_start_time'], DATE_FORMAT)
            endTime = datetime.strptime(task['processing_end_time'], DATE_FORMAT)
            task['duration'] = int((endTime - startTime).total_seconds())
        else:
            task['duration'] = -1
    return jsonData


@authetication_required()
def TaskReportList(request):
  jobId = request.GET.get('job_id')
  url = API_URI + '/task?job_id=' + jobId
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
def exportCSVResult(request, job_id):
  url = API_URI + '/task?job_id=' + job_id
  headers = {'Authorization': 'JWT {0}'.format(request.session['jwt_token'])}
  task_result = requests.get(url, headers=headers)
  if task_result.status_code == 200:
    jsonData = task_result.json()
  else:
    jsonData = {}

  jsonData = get_tasks_info(jsonData, headers)

  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition'] = 'attachment; filename="job_%s.csv"' % job_id
  csv_writer = unicodecsv.writer(response, delimiter=';')
  csv_writer.writerow(['Device', 'Insertion Time', 'Processing Start Time', 'Duration (s)', 'Status', 'Result'])
  for task in jsonData.get('tasks', []):
    csv_writer.writerow([task['device_name'],
                         task['insertion_time'],
                         task['processing_start_time'],
                         task['duration'],
                         task['status'],
                         task['result']])

  return response

