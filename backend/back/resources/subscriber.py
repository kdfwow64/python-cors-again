from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.subscriber import SubscriberModel
import json

class Subscriber(Resource):
  def get(self, id = None):
    queryData = request.args.to_dict()
    if id:
      subscriber = SubscriberModel.findById(id)
      if subscriber: return subscriber.json()
      else: return {'message': 'subscriber not found'}, 404
    subscriber = SubscriberModel.find(**queryData)
    return {'subscribers': list(map(lambda x: x.json(), subscriber))}

  def post(self, **somedata):
    data = json.loads(request.data)
    """if SubscriberModel.find_by_name(name):
    return {'message': "A notification subscriber with name '{}' already exists.".format(name)}, 400"""
    subscriber = SubscriberModel(**data)
    print(data)
    try:  
      subscriber.save_to_db()        
    except:
      return {"message": "An error occurred creating the notification subscriber."}, 500
        
    return subscriber.json(), 201 
    
#   def put(self, id):
#     data = json.loads(request.data)
#     subscriber = SubscriberModel.findById(id)
#     
#     if 'subscriber_id' in data:
#       subscriber.subscriber_id = data['subscriber_id']
#     if 'subscribername' in data:
#       subscriber.subscribername = data['subscribername']
#     if 'email' in data:
#       subscriber.email = data['email']
#     if 'notification_id' in data:
#         subscriber.notification_id = data['notification_id']
#     else:
#       subscriber = SubscriberModel(**data)
#         
#     subscriber.save_to_db()
#     return subscriber.json()
    
  def delete(self, id):
    subscriber = SubscriberModel.findById(id)
    if subscriber:
      subscriber.delete_from_db()
    return {'message': 'notification subscriber deleted'}