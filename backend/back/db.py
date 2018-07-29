from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS

import configparser
parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

app = Flask(__name__)
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(parser.get('POSTGRESQL_SECTION', 'USER'),
                                                                              parser.get('POSTGRESQL_SECTION', 'PASSWORD'),
                                                                              parser.get('POSTGRESQL_SECTION', 'POSTGRESQL_HOST'),
                                                                              parser.get('POSTGRESQL_SECTION', 'DATABASE'),)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

