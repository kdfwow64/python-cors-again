
from django.shortcuts import render
from django.template.loader import render_to_string
import requests
import json
import ast
import urllib
from collections import Counter
from front.common import authetication_required
import configparser
parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))

ELEMENT_TYPE_MAPPING = {"echart":"echart.html",
                        "donut":"donut.html",
                        "top":"top.html",
                        "bar":"bar.html",
                        "doughnut": "doughnut.html",
                        }

def formatValues(rows, dashboardElementType):
  if dashboardElementType == 'echart':
    rows.reverse()
    names = [row["name"] for row in rows]
    series = []
    if rows != []:
      keys = list(rows[0].keys())
      keys.remove('name')
    else : keys = []
    for k in keys:
      serie = {"name":k, 'data':[]}
      for row in rows:
        serie['data'].append(row[k])
      series.append(serie)
    return {"names":names, "series":series}
  elif dashboardElementType == 'top':
    i = 1
    for value in rows:
      row = {"row": i}
      value.update(row)
      i=i+1
    return rows
  else:
    return rows


@authetication_required()
def Dashboard(request):
  if(request.POST.get('logout')):
    del request.session['jwt_token']   
    return render(request, 'login.html')
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  statisticsResponse = requests.get(API_URI + '/dashboardElement/statistics', headers=headers)
  statistics = statisticsResponse.json()
  for k,v in statistics['data'][0].items():
    if isinstance(v, int): statistics['data'][0][k] = str(v)
    if isinstance(v, float): statistics['data'][0][k] = '{:.2f}'.format(v)
  dashboards = requests.get(API_URI + '/dashboard/3', headers=headers)
  elementsHtml = []
  for element in dashboards.json()["dashboardElements"]:
    elmnt = requests.get(API_URI + '/dashboardElement/{0}'.format(element), headers=headers)
    elementJson = elmnt.json()
    template = ELEMENT_TYPE_MAPPING.get(elementJson["type"])
    if not template: raise Exception('Template ' + elementJson["type"] + ' not found.')  
    values = elementJson["data"]

    formattedValues = formatValues(values, elementJson["type"])
    html = render_to_string(template, {'values': formattedValues,
                                                    'name': element,
                                                    'description':elementJson['description'],
                                                    })
    elementsHtml.append({"html": html, "id": element})
  return render(request, 'dashboard.html', {'dashboardElements': elementsHtml,
                                            'statistics': statistics,
                                            })

def DashboardElement(request):  
  id_ = request.GET.get('id')
  if not id_: return 'OOPS', 400
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  elmnt = requests.get(API_URI + '/dashboardElement/{0}'.format(id_), headers=headers)
  elementJson = elmnt.json()
  template = ELEMENT_TYPE_MAPPING.get(elementJson["type"])
  if not template: raise Exception('Template ' + elementJson["type"] + ' not found.')  
  values = elementJson["data"]
  formattedValues = formatValues(values, elementJson["type"])
  return render(request, template, {'values': formattedValues,
                                                    'name': id_,
                                                    'description':elementJson['description'],
                                                    })
# Create your views here.
