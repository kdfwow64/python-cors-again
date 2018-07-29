from flask_restful import Resource, reqparse, request
from models.compliance_element import ComplianceElementModel
import json

class ComplianceElement(Resource):
  def get(self, id=None):
    queryData = request.args.to_dict()
    if id:
      compliance_element = ComplianceElementModel.find_by_id(id)
      if compliance_element:
        return compliance_element.json(), 200
      else:
        return {'error': 'compliance_element not found'}, 404
    compliance_elements = ComplianceElementModel.find(**queryData)
    return {'compliance_elements': list(map(lambda x: x.json(), compliance_elements))}, 200

  def post(self, name=None):
    data = json.loads(request.data)
    name=data.get("name",name)
    if ComplianceElementModel.find_by_name(name):
      return {'error': "A compliance_element with name '{}' already exists.".format(name)}, 400
    compliance_element = ComplianceElementModel(**data)
    try:
      compliance_element.save_to_db()
    except:
      return {"error": "An error occurred creating the compliance_element."}, 500
    return compliance_element.json(), 201

  def put(self, name):
    data = json.loads(request.data)
    compliance_element = ComplianceElementModel.find_by_name(name)
    if compliance_element:
      compliance_element.update(**data)
    else:
      return {'error': 'compliance_element not found'}, 404
    compliance_element.save_to_db(commit=True)
    return compliance_element.json(), 201

  def delete(self, name):
    compliance_element = ComplianceElementModel.find_by_name(name)
    if compliance_element:
      compliance_element.delete_from_db()
    else:
      return {'error': 'compliance_element not found'}, 404
    return {'success': 'compliance_element deleted'}, 202
