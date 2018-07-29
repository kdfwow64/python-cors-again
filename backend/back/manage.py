
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db, app
from models.device import DeviceModel
from models.deviceClass import DeviceClassModel
from models.location import LocationModel
from models.group import GroupModel
from models.job import JobModel
from models.task import TaskModel
from models.user import UserModel
from models.user_group import UserGroupModel
from models.permission import PermissionModel
from models.role_permission import RolePermissionModel
from models.role import RoleModel
from models.trigger import TriggerModel
from models.notification import NotificationModel
from models.rule import RuleModel
from models.subscriber import SubscriberModel
from models.eval import EvalModel
from models.link import LinkModel
from models.workflow import WorkflowModel
from models.workflow_composition import WorkflowCompositionModel
from models.compliance_report import ComplianceReportModel
from models.compliance_element import ComplianceElementModel
from models.compliance_execution import ComplianceExecutionModel
from models.check import CheckModel
from models.check_result import CheckResultModel
from models.job_template import JobTemplateModel

import configparser

parser = configparser.ConfigParser()
parser.read('/opt/optima/global_configuration/optima_configuration_file.cnf')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/{3}'.format(parser.get('POSTGRESQL_SECTION', 'USER'),
                                                                              parser.get('POSTGRESQL_SECTION', 'PASSWORD'),
                                                                              parser.get('POSTGRESQL_SECTION', 'POSTGRESQL_HOST'),
                                                                              parser.get('POSTGRESQL_SECTION', 'DATABASE'),)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
