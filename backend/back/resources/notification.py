from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.notification import NotificationModel
from models.subscriber import SubscriberModel
from models.user import UserModel
import json
from datetime import datetime
import logging
import ast
from resources.auth import requires_permission

class Notification(Resource):
    
  @requires_permission('get_notification')  
  def get(self, id=None):
    queryData = request.args.to_dict()
    if id:  
      notification = NotificationModel.find_by_id(id)                           
      if notification: return notification.json()
      else: return {'message': 'notification not found'}, 404
    notifications = NotificationModel.find(**queryData)
    return {'notifications': list(map(lambda x: x.json(), notifications))}

  @requires_permission('add_notification')    
  def post(self, **somedata):
    data = json.loads(request.data)
    """if NotificationModel.find_by_id(id):
      return {'message': "A notification with id : {}, already exists.".format(id)}, 400"""
    notification = NotificationModel(**data)
    #try:     
    notification.save_to_db()
    """except:
      return {"message": "An error occurred inserting the notification."}, 500"""
    
    _subscribers = data.get("subscriber_list")
    if _subscribers:
      for sub in _subscribers:  
        subscriber = SubscriberModel(notification.id, sub)
        subscriber.save_to_db()               
      #except: return {"message": "An error occurred inserting the subscriber."}, 500
      return notification.json(), 201
      
  @requires_permission('delete_notification')    
  def delete(self, id):       
    notification = NotificationModel.find_by_id(id)
    if notification:
      notification.delete_from_db()
      return {'success': 'Notification deleted'}, 202
    return {'error': 'Notification not found'}, 404

  @requires_permission('update_notification')    
  def put(self, id):
    data = json.loads(request.data)
    notification = NotificationModel.find_by_id(id)  
    subscriber_list = SubscriberModel.find(**{"notification_id": id})
    user_list = [u.subscribername for u in subscriber_list]
    
    if 'name' in data:   
        notification.name = data["name"]      
    if 'trigger_id' in data:
        notification.trigger_id = data["trigger_id"]                 
    if 'action' in data:
        notification.action = data['action']       
    if 'text' in data:    
        notification.text = data['text']
    if 'enable' in data:     
        notification.enable = data['enable']  
    if 'subscribers' in data and user_list !=data["subscribers"]:     
      _subscribers = data["subscribers"]
      for sub in _subscribers:             
        if not str(sub) in user_list:                    
          subdata = {}
          subdata["notification_id"] = id   
          subdata["subscribername"] = sub
          subscriber=SubscriberModel(**subdata) 
          subscriber.save_to_db()         
                          
      for sub in user_list:         
        if not str(sub) in _subscribers:
          subscriber=SubscriberModel.findOne(**{"subscribername":sub,
                                             "notification_id":id})
          subscriber.delete_from_db()   
    else:
       
        notification = NotificationModel(**data)   
    notification.last_update_time = datetime.now().isoformat()
    notification.save_to_db()
    return notification.json()          
  
     