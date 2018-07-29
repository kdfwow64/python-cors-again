import requests
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from front.configuration import *

def authetication_required():
  def wrapper(fn):
      def decorator(request, *args, **kwargs):
        headers = {'Authorization': 'JWT %s' % request.session.get('jwt_token')}
        r = requests.get('%s/check_user' % API_URI, headers=headers)
        res = r.json()

        if not res.get("check_token"):
          return redirect(reverse("login"))

        return fn(request, *args, **kwargs)
      return decorator
  return wrapper