from django.shortcuts import render
import requests
import json

def create(request):
  name = request.POST["name"]
  data = request.POST
  url = 'http://172.18.0.2:5000/device/{0}'.format(data["name"])
  headers = {'Content-Type' : 'application/json'}
  r = requests.post(url, data=json.dumps(data), headers=headers)
  return render(request, 'devices1.html')
	
def delete(request):
  name = request.GET["name"]
  url = "http://172.18.0.2:5000/device/{0}".format(name)
  headers = {'Content-Type' : 'application/json'}
  r = requests.delete(url, headers=headers)

def edit(request):
  name = request.GET["name"]
  data = request.GET
  url = 'http://172.18.0.2:5000/device/{0}'.format(data["name"])
  headers = {'Content-Type' : 'application/json'}
  r = requests.post(url, data=json.dumps(data), headers=headers)
  return render(request, 'devices1.html')

