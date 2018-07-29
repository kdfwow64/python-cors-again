from django.shortcuts import render
import json
from front.common import authetication_required
import requests
import configparser
import logging
import ast
parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')
code_list = [404, 401, 402, 500, 400]
API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))


"""notification"""

NOTIFICATION_FIELDS = ['name',
                       'trigger_id',
                       'enable',
                       'action',
                       'command',
                       'method',
                       'text',
                       'url',
                       'subscriber_list',
                      ]
TRIGGER_FIELDS = ['name',
                  'enabled',
                  'relation',
    ]
                    
def Notification(request):
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  
  notifications = requests.get(API_URI + '/notification', headers=headers)
  notification_list = notifications.json()
  
  subscribers = requests.get(API_URI + '/subscriber', headers=headers)
  subscriber_list = subscribers.json()
  
  triggers = requests.get(API_URI + '/trigger', headers=headers)
  trigger_list = triggers.json()  
  
  users = requests.get(API_URI + '/user', headers=headers)
  user_list = users.json()
  
  if(request.POST.get('new_notification')):      
    data = {k:request.POST.get(k) for k in NOTIFICATION_FIELDS}
    data["subscriber_list"] = data["subscriber_list"].split(',')

    #print(data["subscribers"])
    url = API_URI +'/notification' 
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Notification Created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error" 
    notifications = requests.get(API_URI + '/notification', headers=headers)
    notification_list = notifications.json()
         
    triggers = requests.get(API_URI + '/trigger', headers=headers)
    trigger_list = triggers.json()
    
    users = requests.get(API_URI + '/user', headers=headers)
    user_list = users.json()
    
    subscribers = requests.get(API_URI + '/subscriber', headers=headers)
    subscriber_list = subscribers.json()
         
                 
    return render(request, 'notifications.html',{'notification_list': notification_list,
                                                 'trigger_list': trigger_list,
                                                 'user_list': user_list,
                                                 'subscriber_list':subscriber_list,
                                                 'response': response,                                      
                                                 })
                       
  if(request.GET.get('delete_notification')):             
    data = request.GET
    url = API_URI + '/notification/{0}'.format(data["delete_notification"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.delete(url, headers=headers)
    if r.status_code == 202: response = "Notification Deleted"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error" 
    notifications = requests.get(API_URI + '/notification', headers=headers)
    notification_list = notifications.json()         
  
    triggers = requests.get(API_URI + '/trigger', headers=headers)
    trigger_list = triggers.json()  
  
    users = requests.get(API_URI + '/user', headers=headers)
    user_list = users.json()
    
    subscribers = requests.get(API_URI + '/subscriber', headers=headers)
    subscriber_list = subscribers.json()
          
    return render(request, 'notifications.html', {'response': 'notification deleted',
                                                  'notification_list': notification_list,
                                                  'trigger_list': trigger_list,
                                                  'user_list': user_list,
                                                  'subscriber_list':subscriber_list,
                                                  'response': response,
                                                  })
    
    
  if(request.GET.get('edit_notification')):  
    data= request.GET                         
    subscribers = request.GET.get('subscribers')
                                                            
    data = data.copy()                        
    #print(dict(data)["subscribers"])                 
    #data["subscribers"] = list(map(str, dict(data)["subscribers"]))         
         
    url = API_URI + '/notification/{0}'.format(data["notification_id"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.put(url, data=json.dumps(data), headers=headers)
  
    notifications = requests.get(API_URI + '/notification', headers=headers)
    notification_list = notifications.json()
  
    triggers = requests.get(API_URI + '/trigger', headers=headers)
    trigger_list = triggers.json()   

    users = requests.get(API_URI + '/user', headers=headers)    
    user_list = users.json()
            
    subscribers = requests.get(API_URI + '/subscriber', headers=headers)
    subscriber_list = subscribers.json()                    
                                     
    return render(request, 'notifications.html',{'notification_list': notification_list,
                                                 'trigger_list': trigger_list,
                                                 'user_list': user_list,
                                                 'subscriber_list':subscriber_list })
 
  return render(request, 'notifications.html',{ 'notification_list': notification_list,
                                                'trigger_list': trigger_list,
                                                'user_list': user_list,
                                                'subscriber_list':subscriber_list })

"""trigger"""
  
 
def Trigger(request):
  headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
  
  notifications = requests.get(API_URI + '/notification', headers=headers)
  notification_list = notifications.json()
  
  triggers = requests.get(API_URI + '/trigger', headers=headers)
  trigger_list = triggers.json()
  
  get_devices = requests.get(API_URI + '/devices', headers=headers)
  devices = get_devices.json()
  devicesHtml = get_devices.json()['devices']  

  
  users = requests.get(API_URI + '/user', headers=headers)
  user_list = users.json()
  
  get_location = requests.get(API_URI + '/locations', headers=headers)
  location = get_location.json()
  locationHtml = get_location.json()['locations']  

  get_group = requests.get(API_URI + '/groups', headers=headers)
  group = get_group.json()
  groupHtml = get_group.json()['groups']  

  get_deviceClass = requests.get(API_URI + '/deviceClasses', headers=headers)
  deviceClass = get_deviceClass.json()
  deviceClassHtml = get_deviceClass.json()['deviceClasses']  
  


  
  get_groupDevices = requests.get(API_URI + '/devices', headers=headers)
  groupDevices = get_groupDevices.json()

  if(request.POST.get('new_trigger')):
    data = {k:request.POST.get(k) for k in TRIGGER_FIELDS}
    
    rule_list = str(request.POST.get('rules'))
    data["rules"] = ast.literal_eval(rule_list)
    
    
#     data["rules"]['element'] = request.POST.get('element')
#     data["rules"]['deviceClass'] = request.POST.get('deviceClass')
#     data["rules"]['location'] = request.POST.get('location')
#     data["rules"]['group'] = request.POST.get('group')
#     data["rules"]['device'] = request.POST.get('device')
#     data["rules"]['column'] = request.POST.get('column')
#     if (data["rules"]['element']=='job'):
#       data["rules"]['operation'] = request.POST.get('operationJob')
#     else:
#       data["rules"]['operation'] = request.POST.get('operationTask')
#     if (data["rules"]['element']=="job"):
#       if (data["rules"]['column']=="name"):
#         data["rules"]['value'] = request.POST.get('valueJobName')
#       elif (data["rules"]['column']=="status"):
#         data["rules"]['value'] = request.POST.get('valueJobStatus')
#       elif (data["rules"]['column']=="agent_type"):
#         data["rules"]['value'] = request.POST.get('valueJobAgentType')
#       elif (data["rules"]['column']=="is_validate"):
#         data["rules"]['value'] = request.POST.get('valueJobIsValide')
#     else:
#       data["rules"]['value'] = request.POST.get('valueTask')

    

    #     print(data) 
#     print(data["rules"])
#     for rule in ast.literal_eval(data["rules"]): 
#         rul=rule
#         print(rul)  
#         for r in rule:
#             print(r) 
#     print(type(data["rules"]))
#     json_rules = json.dumps(rules) 
#     print(json_rules)  
  
    url = API_URI +'/trigger' 
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code == 201: response = "Trigger Created"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error" 
    notifications = requests.get(API_URI + '/notification', headers=headers)
    notification_list = notifications.json()
    
    triggers = requests.get(API_URI + '/trigger', headers=headers)
    trigger_list = triggers.json()
    
    return render(request, 'triggers.html',{'notification_list': notification_list,
                                            'trigger_list': trigger_list,
                                            'deviceClassHtml':json.dumps(deviceClassHtml),
                                            'locationHtml':json.dumps(locationHtml),
                                            'groupHtml':json.dumps(groupHtml),
                                            'devicesHtml':json.dumps(devicesHtml),
                                            'groupDevices': groupDevices,
                                            'response': response,
                                            })      
  
  
  if(request.GET.get('delete_trigger')):
    data = request.GET       
    url = API_URI + '/trigger/{0}'.format(data["delete_trigger"])
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.delete(url, headers=headers)
    if r.status_code == 202: response = "Trigger Deleted"
    elif r.status_code in code_list: response = r.text
    else: response = "Unknown Error" 
    notifications = requests.get(API_URI + '/notification', headers=headers)
    notification_list = notifications.json()
  
    triggers = requests.get(API_URI + '/trigger', headers=headers)
    trigger_list = triggers.json()  
    
    return render(request, 'triggers.html', {'notification_list': notification_list,
                                             'trigger_list': trigger_list,
                                             'deviceClassHtml':json.dumps(deviceClassHtml),
                                             'locationHtml':json.dumps(locationHtml),
                                             'groupHtml':json.dumps(groupHtml),
                                             'devicesHtml':json.dumps(devicesHtml),
                                             'groupDevices': groupDevices,
                                             'response': response,
                                            })
    
  if(request.GET.get('edit_trigger')): 
    data = request.GET
    url = API_URI + '/trigger/{0}'.format(data["trigger_id"])    
    headers = {'Authorization' : 'JWT {0}'.format(request.session.get('jwt_token'))}
    r = requests.put(url, data=json.dumps(data), headers=headers)         
    notifications = requests.get(API_URI + '/notification', headers=headers)
    notification_list = notifications.json()

    triggers = requests.get(API_URI + '/trigger', headers=headers)
    trigger_list = triggers.json()
    
              
    return render(request, 'triggers.html',{'notification_list': notification_list,
                                            'trigger_list': trigger_list, 
                                            'deviceClassHtml':json.dumps(deviceClassHtml),
                                            'locationHtml':json.dumps(locationHtml),
                                            'groupHtml':json.dumps(groupHtml),
                                            'devicesHtml':json.dumps(devicesHtml),
                                            'groupDevices': groupDevices,
                                            }) 

  return render(request, 'triggers.html',{'notification_list': notification_list,
                                          'trigger_list': trigger_list,
                                          'deviceClassHtml':json.dumps(deviceClassHtml),
                                          'locationHtml':json.dumps(locationHtml),
                                          'groupHtml':json.dumps(groupHtml),
                                          'devicesHtml':json.dumps(devicesHtml),
                                          'groupDevices': groupDevices,
                                          })
  
  
       