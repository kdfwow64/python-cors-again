from flask_restful import Resource, reqparse, request
from models.job_template import JobTemplateModel
import json

class JobTemplate(Resource):
  def get(self, name=None):
    queryData = request.args.to_dict()
    if name:
      job_template = JobTemplateModel.find_by_name(name)
      if job_template:
        return job_template.json(), 200
      else:
        return {'error': 'job_template not found'}, 404
    job_templates = JobTemplateModel.find(**queryData)
    return {'job_templates': list(map(lambda x: x.json(), job_templates))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    if JobTemplateModel.find_by_name(name):
      return {'error': "A job_template with name '{}' already exists.".format(name)}, 400
    job_template = JobTemplateModel(**data)
    try:
      job_template.save_to_db()
    except:
      return {"error": "An error occurred creating the job_template."}, 500
    return job_template.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    job_template = JobTemplateModel.find_by_name(name)
    if job_template:
      job_template.update(**data)
    else:
      return {'error': 'job_template not found'}, 404
    job_template.save_to_db(commit=True)
    return job_template.json(), 201

  def delete(self, name):
    job_template = JobTemplateModel.find_by_name(name)
    if job_template:
      job_template.delete_from_db()
    else:
      return {'error': 'job_template not found'}, 404
    return {'success': 'job_template deleted'}, 202
