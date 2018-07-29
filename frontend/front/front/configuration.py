import configparser

parser = configparser.RawConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

API_URI = 'http://{0}:{1}'.format(parser.get('API_SECTION', 'API_HOST'),
                                  parser.get('API_SECTION', 'API_PORT'))

KIBANA_URL = parser.get('ELK_STACK_SECTION', 'KIBANA_HOST')
KIBANA_PORT = parser.get('ELK_STACK_SECTION', 'KIBANA_PORT')
KIBANA_URL_SUFFIX = parser.get('ELK_STACK_SECTION', 'KIBANA_URL_SUFFIX')