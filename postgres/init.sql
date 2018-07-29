INSERT INTO "permission" ("name", "value", "object") VALUES ('get_user', 'get user', 'user');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_user', 'add user', 'user');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_user', 'update user', 'user');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_user', 'delete user', 'user');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_users', 'get users', 'user');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_user_group', 'get user_group', 'user_group');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_user_group', 'add user_group', 'user_group');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_user_group', 'update user_group', 'user_group');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_user_group', 'delete user_group', 'user_group');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_user_groups', 'get user_groups', 'user_group');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_user_group_roles', 'get user_group roles', 'user_group');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_role', 'get role', 'role');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_role', 'add role', 'role');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_role', 'update role', 'role');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_role', 'delete role', 'role');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_roles', 'get roles', 'role');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_role_permissions', 'get role permissions', 'role');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_jobs', 'get jobs', 'job');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_job', 'get job', 'job');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_job', 'add job', 'job');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_job', 'update job', 'job');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_job', 'delete job', 'job');
INSERT INTO "permission" ("name", "value", "object") VALUES ('validate_jobs', 'validate job', 'job');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_workflows', 'get workflows', 'workflow');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_workflow', 'get workflow', 'workflow');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_workflow', 'add workflow', 'workflow');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_workflow', 'update workflow', 'workflow');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_workflow', 'delete workflow', 'workflow');
INSERT INTO "permission" ("name", "value", "object") VALUES ('validate_workflows', 'validate workflow', 'workflow');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_devices', 'get devices', 'device');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_device', 'get device', 'device');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_device', 'add device', 'device');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_device', 'update device', 'device');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_device', 'delete device', 'device');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_notifications', 'get notifications', 'notification');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_notification', 'get notification', 'notification');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_notification', 'add notification', 'notification');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_notification', 'update notification', 'notification');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_notification', 'delete notification', 'notification');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_triggers', 'get triggers', 'trigger');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_trigger', 'get trigger', 'trigger');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_trigger', 'add trigger', 'trigger');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_trigger', 'update trigger', 'trigger');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_trigger', 'delete trigger', 'trigger');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_compliance_reports', 'get compliance_reports', 'compliance_report');
INSERT INTO "permission" ("name", "value", "object") VALUES ('get_compliance_report', 'get compliance_report', 'compliance_report');
INSERT INTO "permission" ("name", "value", "object") VALUES ('add_compliance_report', 'add compliance_report', 'compliance_report');
INSERT INTO "permission" ("name", "value", "object") VALUES ('update_compliance_report', 'update compliance_report', 'compliance_report');
INSERT INTO "permission" ("name", "value", "object") VALUES ('delete_compliance_report', 'delete compliance_report', 'compliance_report');
INSERT INTO "permission" ("name", "value", "object") VALUES ('execute_compliance_report', 'execute_compliance_report', 'compliance_report');

INSERT INTO "permission" ("name", "value", "object") VALUES ('get_tasks', 'get tasks', 'task');

INSERT INTO "role" ("name") VALUES ('admin');

INSERT INTO "role_permissions" ("role_id", "permission_id")
SELECT role.id, permission.id FROM role, permission
WHERE role.name = 'admin';

INSERT INTO "user_group" ("name") VALUES ('admin');
INSERT INTO "user_group_roles" ("user_group_id", "role_id")
SELECT user_group.id, role.id FROM user_group, role
WHERE role.name = 'admin' AND user_group.name = 'admin';

INSERT INTO "user" ("user_group", "username", "password", "email", "phone_number")
SELECT user_group.id, 'admin', 'pbkdf2:sha256:50000$q8QOSW9O$db66f5b53c54860a208b97a3794c8c938ab86c4f2cde137b6307b582d879a4b0', '', ''
FROM user_group
WHERE user_group.name = 'admin';
INSERT INTO "deviceClass" ("name") values ('discovered');
CREATE EXTENSION tablefunc;
