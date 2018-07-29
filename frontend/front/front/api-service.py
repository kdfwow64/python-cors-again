import ast
import urllib
import csv
from django.http import HttpResponse
from front.common import authetication_required
import configparser
parser = configparser.ConfigParser()
parser.read('/opt/optima_configuration_file.cnf')


def get(url, headers, data ):
  data = request.GET
  url = "http://{0}:{1}/device/{0}".format(data["delete_device"])
  headers = {'Authorization' : 'JWT {0}'.format(request.session['jwt_token'])}
  r = requests.delete(url, headers=headers)