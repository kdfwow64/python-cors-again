from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
import logging
from logging.handlers import RotatingFileHandler
from db import db, app
from security import authenticate, identity
from resources.user import User
from resources.job import Job
from resources.device import *
from resources.group import *
from resources.deviceClass import *
from resources.location import *
from resources.dashboard import Dashboard
from resources.dashboardElement import DashboardElement
from models.task import TaskModel 
from resources.task import Task
from resources.result import Result
from resources.check_user import Check_User
from flask_cors import CORS
from datetime import datetime, timedelta
from resources.user_group import UserGroup, UserGroups, UserGroupRoles
from resources.permission import Permission, Permissions
from resources.rule import Rule
from resources.role import Role, Roles, RolePermissions
from resources.notification import Notification
from resources.trigger import Trigger
from resources.rule import Rule
from resources.subscriber import Subscriber
from resources.workflow import Workflow
from resources.eval import Eval
from resources.link import Link
from resources.auth import Login
from resources.compliance_report import ComplianceReport
from resources.compliance_element import ComplianceElement
from resources.compliance_execution import ComplianceExecution
from resources.check import Check
from resources.check_result import CheckResult
from resources.job_template import JobTemplate
import configparser

parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=10000)
app.config['JWT_LEEWAY'] = 5


OPTIMA_LOG_FOLDER = '/opt/'
OPTIMA_BACKEND_API_LOGFILE = OPTIMA_LOG_FOLDER + '/optima-api.log'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(parser.get('POSTGRESQL_SECTION', 'USER'),
                                                                              parser.get('POSTGRESQL_SECTION', 'PASSWORD'),
                                                                              parser.get('POSTGRESQL_SECTION', 'POSTGRESQL_HOST'),
                                                                              parser.get('POSTGRESQL_SECTION', 'DATABASE'),)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Job, '/job/<string:id>', '/job')
api.add_resource(Device, '/device/<string:name>', '/device')
api.add_resource(Group, '/group/<string:name>', '/group')
api.add_resource(GroupList, '/groups')
api.add_resource(DeviceClass, '/deviceClass/<string:name>', '/deviceClass')
api.add_resource(DeviceClassList, '/deviceClasses')
api.add_resource(Location, '/location/<string:name>', '/location')
api.add_resource(LocationList, '/locations')
api.add_resource(DeviceList, '/devices')
api.add_resource(Childingroup, '/group/childs/<string:name>')
#api.add_resource(Deviceingroup, '/device/group/<string:name>')
#api.add_resource(DeviceindeviceClass, '/device/deviceClass/<string:name>')
#api.add_resource(Deviceinlocation, '/device/location/<string:name>')
api.add_resource(Dashboard, '/dashboard/<string:id>', '/dashboard')
api.add_resource(DashboardElement, '/dashboardElement/<string:name>', '/dashboardElement')
api.add_resource(Task, '/task', '/task/<string:id>')
api.add_resource(Result, '/result/<string:id>', '/result')
api.add_resource(User, '/user/<string:id>', '/user')
api.add_resource(UserGroups, '/user_groups/', '/user_groups')
api.add_resource(UserGroup, '/user_group/<string:id>', '/user_group')
api.add_resource(UserGroupRoles, '/user_group/<string:id>/roles', '/user_group')
api.add_resource(Permissions, '/permissions/', '/permissions')
api.add_resource(Permission, '/permission/<string:id>', '/permission')
api.add_resource(Check_User, '/check_user')
api.add_resource(Notification, '/notification/<string:id>', '/notification')
api.add_resource(Trigger, '/trigger/<string:id>', '/trigger')
api.add_resource(Role, '/role/<string:id>', '/role')
api.add_resource(Roles, '/roles/', '/roles')
api.add_resource(RolePermissions, '/role/<string:id>/permissions', '/roles')
api.add_resource(Rule, '/rule/<string:id>', '/rule')
api.add_resource(Subscriber, '/subscriber/<string:id>', '/subscriber')
api.add_resource(Workflow, '/workflow/<string:id>', '/workflow')
api.add_resource(Eval, '/eval/<string:id>', '/eval')
api.add_resource(Link, '/link/<string:id>', '/link')
api.add_resource(Login, '/login')
api.add_resource(ComplianceReport, '/compliance_report', '/compliance_report/<string:id>')
api.add_resource(ComplianceElement, '/compliance_element', '/compliance_element/<string:id>')
api.add_resource(ComplianceExecution, '/compliance_execution', '/compliance_execution/<string:id>')
api.add_resource(Check, '/check', '/check/<string:id>')
api.add_resource(CheckResult, '/check_result', '/check_result/<string:id>')
api.add_resource(JobTemplate, '/job_template', '/job_template/<string:id>')

if __name__ == '__main__':
    handler = RotatingFileHandler(OPTIMA_BACKEND_API_LOGFILE, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=parser.getint('API_SECTION', 'API_PORT'), debug=True,threaded=True)
