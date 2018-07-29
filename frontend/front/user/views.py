from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
import requests
import json
from front.common import authetication_required
from front.configuration import *
from requests.auth import HTTPBasicAuth


@authetication_required()
def UserCreate(request):
  message = ''
  url = API_URI + '/user'
  headers = {'Authorization': 'JWT %s' % request.session['jwt_token']}
  url_all_user_groups = API_URI + '/user_groups'
  r = requests.get(url_all_user_groups, headers=headers)
  all_user_groups = {}
  if r.status_code == 200:
    all_user_groups = r.json()

  if request.method == 'POST':
    data = request.POST
    if data['password'] == data['confirm_password']:
      r = requests.post(url, data=json.dumps(data), headers=headers)
      if r.status_code == 200:
        return redirect(reverse("user:user"))
      else:
        if 'error' in r.text:
          message = r.json()['error']
        else:
          message = "Unknown error"
        # return render(request, 'user/user_form.html', {'message': message, 'action': 'add'})
    else : message = 'confirm password'
  return render(request, 'user/user_form.html',
                {'action': 'add',
                 'message': message,
                 "all_user_groups": all_user_groups})

@authetication_required()
def User(request):
  url = API_URI + '/user'
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jsondata = r.json()
  else: jsondata = {}
  return render(request, 'user/user.html', {'jsondata': jsondata})


@authetication_required()
def UserDelete(request, obj_id=None):
  url = API_URI + '/user/%s' % obj_id
  headers = {'Authorization': 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.delete(url, headers=headers)
  return redirect(reverse("user:user"))


@authetication_required()
def UserEdit(request, obj_id=None):
  message = ''
  url = API_URI + '/user/%s' % obj_id
  headers = {'Authorization': 'JWT %s' % request.session['jwt_token']}

  url_all_user_groups = API_URI + '/user_groups'
  r = requests.get(url_all_user_groups, headers=headers)
  all_user_groups = {}
  if r.status_code == 200:
    all_user_groups = r.json()

  if request.method == 'POST':
    data = request.POST
    r1 = requests.put(url, data=json.dumps(data), headers=headers)
    if r1.status_code == 200:
      return redirect(reverse("user:user"))
    else:
      if 'error' in r1.text:
        message = r1.json()['error']
      else:
        message = "Unknown error"

  r = requests.get(url, headers=headers)
  jsondata = {}
  if r.status_code == 200:
    jsondata = r.json()

  return render(request, 'user/user_form.html',
                {'action': 'edit',
                 "obj": jsondata,
                 'message': message,
                 "all_user_groups": all_user_groups,
                 'message': message})


@authetication_required()
def UserGroupCreate(request):
  message = ''

  url = API_URI + '/user_group'
  headers = {'Authorization': 'JWT %s' % request.session['jwt_token']}

  url_all_roles = API_URI + '/roles'
  r = requests.get(url_all_roles, headers=headers)
  all_roles = {}
  if r.status_code == 200:
    all_roles = r.json()
  if request.method == 'POST':
    all_roles_id = [role['id'] for role in all_roles["roles"]]
    data = request.POST
    user_group = {}
    if "name" in data:
      user_group["name"] = data["name"]

    user_group["roles"] = []
    for ugr in all_roles_id:
      ugr = str(ugr)
      #if ugr in data.keys():
      #if data[ugr] == "1":
      if ugr in data["selected_values"].split(','):
        #user_group["roles"].append({"id": ugr})
        user_group["roles"].append({"id": ugr})

    r1 = requests.post(url, data=json.dumps(user_group), headers=headers)

    if r1.status_code == 201:
      return redirect(reverse("user:user_group"))
    else:
      if 'error' in r1.text:
        message = r1.json()['error']
      else:
        message = "Unknown error"
      # return render(request, 'user_group/user_group_form.html', {'message': message, 'action': 'add'})

  return render(request, 'user_group/user_group_form.html',
                {'action': 'add',
                 'message': message,
                 "all_roles": all_roles})


@authetication_required()
def UserGroup(request):
  url = API_URI + '/user_groups'
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jsondata = r.json()
  else: jsondata = {}

  result = {'user_groups': []}
  if 'user_groups' in jsondata.keys():
    for user_group in jsondata['user_groups']:
      url_roles = API_URI + '/user_group/%s/roles' % user_group['id']
      r = requests.get(url_roles, headers=headers)
      roles = {}
      if r.status_code == 200:
        roles = r.json()

      if 'roles' in roles.keys():
        user_group['roles'] = roles['roles']

      result['user_groups'].append(user_group)

  return render(request, 'user_group/user_group.html', {'jsondata': result})


@authetication_required()
def UserGroupDelete(request, obj_id=None):
  url = API_URI + '/user_group/%s' % obj_id
  headers = {'Authorization': 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.delete(url, headers=headers)
  return redirect(reverse("user:user_group"))


@authetication_required()
def UserGroupEdit(request, obj_id=None):
  message = ''
  url = API_URI + '/user_group/%s' % obj_id
  headers = {'Authorization': 'JWT %s' % request.session['jwt_token']}

  url_all_roles = API_URI + '/roles'
  r = requests.get(url_all_roles, headers=headers)
  all_roles = {}
  if r.status_code == 200:
    all_roles = r.json()

  all_roles_id = [role['id'] for role in all_roles["roles"]]

  if request.method == 'POST':
    data = request.POST
    user_group = {"roles": []}
    for ugr in all_roles_id:
      ugr = str(ugr)
      #if ugr in data.keys():
      #if data[ugr] == "1":
      if ugr in data["selected_values"].split(','):
        #user_group["roles"].append({"id": ugr})
        user_group["roles"].append({"id": ugr})

    r1 = requests.put(url, data=json.dumps(user_group), headers=headers)
    if r1.status_code == 201:
      return redirect(reverse("user:user_group"))
    else:
      if 'error' in r1.text:
        message = r1.json()['error']
      else:
        message = "Unknown error"

  r = requests.get(url, headers=headers)
  jsondata = {}
  if r.status_code == 200:
    jsondata = r.json()

  url_roles = API_URI + '/user_group/%s/roles' % obj_id
  r = requests.get(url_roles, headers=headers)
  roles = {}
  roles_id = {}
  if r.status_code == 200:
    roles = r.json()
    roles_id = [role['id'] for role in roles["roles"]]

  return render(request, 'user_group/user_group_form.html',
                {'action': 'edit',
                 "obj": jsondata,
                 "message": message,
                 "all_roles": all_roles,
                 "roles_id": roles_id})


@authetication_required()
def RoleCreate(request):
  message = ''

  url = API_URI + '/role'
  headers = {'Authorization': 'JWT %s' % request.session['jwt_token']}

  url_all_permissions = API_URI + '/permissions'
  r = requests.get(url_all_permissions, headers=headers)
  all_permissions = {}
  if r.status_code == 200:
    all_permissions = r.json()

  if request.method == 'POST':
    data = request.POST
    role = {}
    if "name" in data:
      role["name"] = data["name"]

    all_permissions_id = [permission['id'] for permission in all_permissions["permissions"]]

    role["permissions"] = []
    for rp in all_permissions_id:
      rp = str(rp)
      # if rp in data.keys():
      if rp in data["selected_values"].split(','):
        #if data[rp] == "1":
        role["permissions"].append({"id": rp})

    r1 = requests.post(url, data=json.dumps(role), headers=headers)
    if r1.status_code == 201:
      return redirect(reverse("user:role"))
    else:
      if 'error' in r1.text:
        message = r1.json()['error']
      else:
        message = "Unknown error"

  return render(request, 'role/role_form.html',
                {'action': 'add',
                 'message': message,
                 "all_permissions": all_permissions})


@authetication_required()
def Role(request):
  url = API_URI + '/roles'
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.get(url, headers=headers)
  if r.status_code == 200: jsondata = r.json()
  else: jsondata = {}

  result = {'roles': []}


  if 'roles' in jsondata.keys():
    for role in jsondata['roles']:
      url_permissions = API_URI + '/role/%s/permissions' % role['id']
      r = requests.get(url_permissions, headers=headers)
      permissions = {}
      if r.status_code == 200:
        permissions = r.json()

      role['permissions'] = permissions['permissions']

      result['roles'].append(role)

  return render(request, 'role/role.html', {'jsondata': result})


@authetication_required()
def RoleDelete(request, obj_id=None):
  url = API_URI + '/role/%s' % obj_id
  headers = {'Authorization': 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.delete(url, headers=headers)
  return redirect(reverse("user:role"))


@authetication_required()
def RoleEdit(request, obj_id=None):
  message = ''
  url = API_URI + '/role/%s' % obj_id
  headers = {'Authorization': 'JWT %s' % request.session['jwt_token']}

  url_all_permissions = API_URI + '/permissions'
  r = requests.get(url_all_permissions, headers=headers)
  all_permissions = {}
  if r.status_code == 200:
    all_permissions = r.json()

  all_permissions_id = [permission['id'] for permission in all_permissions["permissions"]]

  if request.method == 'POST':
    data = request.POST
    role = {"permissions": []}
    for rp in all_permissions_id:
      rp = str(rp)
      # if rp in data.keys():
      if rp in data["selected_values"].split(','):
        # if data[rp] == "1":
        role["permissions"].append({"id": rp})

    r1 = requests.put(url, data=json.dumps(role), headers=headers)
    if r1.status_code == 201:
      return redirect(reverse("user:role"))
    else:
      if 'error' in r1.text:
        message = r1.json()['error']
      else:
        message = "Unknown error"

  r = requests.get(url, headers=headers)
  jsondata = {}
  if r.status_code == 200:
    jsondata = r.json()

  url_permissions = API_URI + '/role/%s/permissions' % obj_id
  r = requests.get(url_permissions, headers=headers)
  permissions = {}
  permissions_id = {}
  if r.status_code == 200:
    permissions = r.json()
    permissions_id = [permission['id'] for permission in permissions["permissions"]]

  return render(request, 'role/role_form.html',
                {'action': 'edit',
                 "obj": jsondata,
                 "message": message,
                 "all_permissions": all_permissions,
                 "permissions_id": permissions_id})


def Logout(request):
  del request.session['jwt_token']
  return redirect(reverse("login"))


def Login(request):
    message = ""
    validated_agrement = False
    agrement_file = open("/opt/optima/frontend/front/user/agrement.txt","r+b")
    validated = agrement_file.read()
    if validated == b"validated_agrement = true":
      validated_agrement = True
    if (request.POST.get('send_agrement')):
      data = request.POST
      agree = data.get('_agrement')
      if agree == 'on':
        agrement_file.write(b"validated_agrement = true")
        validated_agrement = True
    if (request.POST.get('login_form')):
        data = request.POST
        url = API_URI + '/login'
        headers = {'Content-Type': 'application/json'}
        r = requests.get(url, headers=headers, auth=HTTPBasicAuth(data["username"], data["password"]))
        if r.status_code == 200:
            response = r.json()
            if response.get("access_token"):
                request.session['jwt_token'] = response["access_token"]
                host = request.META.get('HTTP_HOST', 'localhost')
                hostname = host.split(':')[0]
                kibanaHost = 'http://' + hostname + ':' + KIBANA_PORT + KIBANA_URL_SUFFIX
                return render(request, 'home.html', {'kibana_host': kibanaHost})

        message = "The username or password that you've entered are not correct."
        return render(request, 'login.html', {'message': message})
    return render(request, 'login.html', {'message': message,
                                          'validated_agrement': validated_agrement,
                                          })
