from flask import current_app as app
from sqlalchemy.sql import text
from sqlalchemy import distinct,func
import os, time,uuid,re
from time import gmtime, strftime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models.model import * #Notification,Follows,Users,Story,Posts,Comments,Likes,flags_,Jobs,job_bid,Interests,Share
from flask import (Flask, g, render_template, flash, redirect, url_for, session,request, abort)
from flask_bcrypt import check_password_hash
from flask_login import(LoginManager, login_user, logout_user,login_required, current_user)
from flask_mysqldb import MySQL # sudo apt install default-libmysqlclient-dev  b4 installing flask-mysqldb
from flask_sqlalchemy import SQLAlchemy
from models.model import db
import urllib.request
from sqlalchemy import create_engine, exc,desc,or_,and_
from flask import Flask, request, redirect, jsonify,make_response,json,Blueprint
from werkzeug.utils import secure_filename
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token,get_jwt_identity)
import datetime

    
current_time = time.localtime()
sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
story_bp = Blueprint('story', __name__)

"""
------------------  PUSH NOTIFICATION --------------------

""" 
@jwt_required
def pusher(notification,registration_id):
    current_usa = get_jwt_identity()
    print(current_usa)
    from pyfcm import FCMNotification
    
    reg_id = jsonify(str(registration_id))
    print(registration_id)
    push_service = FCMNotification(api_key="AAAA8WXoSeU:APA91bEYkL4PwQnrs1DcjdycpWIU4KAg7HEJUq_iaUehC3gQmS_ozYzanH4QUHuFWAdm1nBXhKRKY1gXycBomjPg9AbuSf6dIq5ZxGcwBOrthyHPieraoQesRRlTxZEnyZHIZ_tE46gE")
    
 
    result = push_service.notify_single_device(registration_id=registration_id,data_message=notification)
    
    
    print(notification)
    print(result)
    print(registration_id)    


"""
------------------ NOTIFIER --------------------

"""


def notifier(activity,timestamp,message,data_url,user_data_url,status_code):
     """
       save notifications from activities

     """
     notification = Notification(

                   activity = activity,
                   user = user_data_url,
                   author =user_data_url,
                   timestamp =timestamp,
                   message = message,
                   data_url = data_url,
                   user_data_url = user_data_url,
                   status_code = status_code

             )

     db.session.add(notification)
     db.session.commit()
        
     response_object = {
                         "status": 1,
                          "message" : message,
                          "data_url" : data_url ,
                          "user_data_url" : user_data_url,
                          "status_code" : status_code,
                          
                    } 

 
 

"""
------------------  LOGGED CHECKER --------------------

""" 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            response_object = {
            'status': 'fail',
            'message': ' Please Log in to continue.',
        }
            return response_object
    return wrap

"""
------------------ NOTIFY  --------------------

"""
def notify():
    """
     this takes notifications for current user from database and returns at any api requset.

    """
    current_time = time.localtime()
    when = time.strftime('%H:%M:%S GMT', current_time) 
    user = Users.query.filter_by(username = session["current_user"]).first()
  
    user_ = Users.query.filter_by(id = user.id).first()
    usa = "'"+session["current_user"]+"'"
    no_t=  conn.execute("select * from notifications where author = %s"%usa)#Notification.query.filter_by(user = user_.id)
    note= no_t.fetchall()
    count = 0
    response_ = []
    for row in note:
        count = count +1
       
        notice = {

                "user_image_url": user.image_url,
                "message" : row.message,
                "data_url" : row.data_url ,
                "user_data_url" : row.user_data_url,
                "state" : row.status_code,
                "note_id": row.id,
                "when" : row.timestamp
                
                  }

        response_.append(notice)

        response_object = {
                    "notifications" : response_,
                    "note_count": count
        }
      
    
        return response_object


  
"""
------------------  CREATE STORY--------------------
This  creates a story from a POST request
status codes:
   - 1 deleted
   - 2  private
   - 0 public (default)


"""
@story_bp.route('/api/v1/create_story', methods=('GET', 'POST'))
@jwt_required
def create_storys():

        #variable diclaration and definations
    
        data= request.json
        body = data.get('body')
        user_id = data.get('user_id')
        status = data.get('status'),
        timestamp =sasa
        warning = []
        device_id =data.get('device_id')
        if not device_id:
            return jsonify('device_id missing')
        #update users device id
        username = get_jwt_identity()
        user_data = Users.query.filter_by(username = username).first()
        user_data.device_id = device_id
        db.session.commit()
        #data validation
        #check for data presence and return error for missing values       
        
        if not body:
            warning.append(" content is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)
        
        if not user_id:
            warning.append(" user_id is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)
        #validate

        if Users.query.filter_by(id = user_id).first() is None:
            warning.append(" user_id is invalid")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)
       
        
        #check and set status to public if story status not specified
        if not status:
            warning.append(" status is missing")
            status = 0

       
        #get user data via user_id
        _user = Users.query.filter_by(id = user_id).first()
        #story creation
       
        new_story = Story(
            body = body,
            author_id = user_id,            
            status = 0,
            timestamp =sasa,
            )
        #for empty database tables
        if Story.query.filter_by(body=body).count() == 0:
            db.session.add(new_story)
            db.session.commit()
            exist= db.session.query(Story).filter(and_(Story.body ==body,Story.author_id == _user.id)).first()
            return jsonify(exist.to_json())
        exist=db.session.query(Story).filter(and_(Story.body ==body,Story.author_id ==user_id)).first()
        
        db.session.add(new_story)
        db.session.commit()
        created_story =db.session.query(Story).filter(and_(Story.body ==body ,Story.author_id ==user_id)).first()
        message = "{} added a new story".format(user_id)
        notification = {
              "event_type": "create_story",
              "body" :message,
              "title" : "iMarket",
              "image":_user.image_url,
              "link": url_for("get_story",story_id = created_story.id),
              "story_id": created_story.id,
              "user_id":_user.id,
              "name": _user.username
               }
        #pusher(notification)
        return jsonify(created_story.to_json())

        #show private story to the story author   
        if created_story.status ==2 and exist.author_id ==_user.id:
            created_story = exist
            #return story_data
            return jsonify(created_story.to_json())   





"""
------------------   UPDATE STORY --------------------

"""

@story_bp.route('/api/v1/update_story', methods=('GET', 'POST', 'PUT'))
@jwt_required
def update_story():
    
    #deffinations
    data = request.json
    
    body =data.get('body')
    status = data.get('status')
    user_id = data.get('user_id')
    story_id = data.get('story_id')
    
    warning=[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check data for empty input
    if not user_id:      
        warning.append(" user_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }
        return jsonify(response_object)
        
    if not story_id:      
        warning.append(" story_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }
        return jsonify(response_object)
        
    if not body:
        warning.append(" body is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }
        return jsonify(response_object)

    #validate existance

    if Users.query.filter_by(id = user_id).first() is None:
        warning.append(" user_id is invalid")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return jsonify(response_object)
    


    if Story.query.filter_by(id = story_id).first() is None:
        warning.append(" story_id is invalid")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return jsonify(response_object)
        
    #set status to public on default
    if not status :
        warning.append(" status is missing")
        ststus = 0
    if status == "":
        status =0 
    if Users.query.filter_by(id = user_id).first() is None:          
         warning.append(" user_id is invalid")                 
         #return response
         response_object = {
                  "status": 201,
                  "errors" : warning
              }  
         return jsonify(response_object) 
    
    #verify a story to update by story_id and author_id
    _user = Users.query.filter_by(id =user_id).first()
    exist= db.session.query(Story).filter(and_(Story.author_id == _user.id,Story.id == story_id)).first()
    
    if not exist:
        response_object = {
          "status": 201,
          "errors": "story doesnt exist!"
        }
        return jsonify(response_object)
    
    #preserve unchanged fileds
    if  body == exist.body :          
        warning.append(" story already exists")                
    if body != exist.body:
       exist.body = body
    
    if  status == exist.status :          
        warning.append(" status unchanged")                
    if status != exist.status:
       exist.status = status
    
    #create update data
    exist.body =body
    
    exist.status = status
    db.session.add(exist)
    db.session.commit()
    
    #respond
    return jsonify(exist.to_json())    



"""
------------------   GET STORY --------------------

"""       


@story_bp.route('/api/v1/get_story', methods=('GET', 'POST'))
@jwt_required
def get_story():
    #definations 
    data = request.json
    story_id = data.get("story_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_story_ids = []
    user_Story = [] 
    warning = []
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check data for blanks
    _user = Users.query.filter_by(status = 0).all()
    if not user_id:
        warning.append("user_id : user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)
    
    for _user_ in _user:
        existing_user_ids.append(_user_.id)
        
    #verify user_id
    if Users.query.filter_by(id = user_id).first() is None : 
        warning.append("user_id : {} doesn't exist !".format(user_id))
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    if Story.query.filter_by(id= story_id).first() is None: 
        warning.append("story_id doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    #get post_data   
    story= db.session.query(Story).filter(and_(Story.author_id == user_id, Story.id == story_id)).first()
    if  story.status ==0: 
        return jsonify(story.to_json()) 
    else :
        response_object = {"ststus" : 201, "error" : "story missing"}
        return  jsonify(response_object)


"""
-----------    DELETE STORY ---------------
"""

@story_bp.route("/api/v1/delete_story",methods=('POST','GET'))
@jwt_required
def delete_story():
     data = request.json
     user_id= data.get("user_id")
     story_id= data.get("story_id")
     device_id =data.get('device_id')
     if not device_id:
       return jsonify({"status":201,"message":'device_id missing'})
     #update users device id
     username = get_jwt_identity()
     user_data = Users.query.filter_by(username = username).first()
     user_data.device_id = device_id
     db.session.commit()

     if not story_id:
      return jsonify({"Error":"story _id missing.", "status":201})
     if not user_id:
      return jsonify({"Error":"user id missing","status":201})
     if Users.query.filter_by(id=user_id)is None:
        r={
           "STATUS":201,
           "ERROR": "INVALID USER ID"

          }
        return jsonify(r)
     if Story.query.filter_by(id = story_id ).first() is None:
        return jsonify({"status":201,"error":"STORY ID INVALID"})
     story = db.session.query(Story).filter(and_(Story.id ==story_id, Story.author_id == user_id)).first()
     if story:
        story.status = 1
        db.session.commit()
        return jsonify({"story_data":story.to_json(), "message":"story deleted successfully"})
     else:
        return jsonify({"status":201,"error" :"story doesn't exist"})



""" 

------------------  UPLOAD STORY IMAGE --------------------


""" 

@story_bp.route('/api/v1/story_image/<story_id>' , methods = ("GET","POST"))
@jwt_required
def upload_story_pic(story_id):    
    data= request.files
    file = request.files['file']
    username = get_jwt_identity()
    user_data =Users.query.filter_by(username= username).first()    
    id = user_data.id

    if db.session.query(Story).filter(and_(Story.id ==story_id, Story.status ==0)).first() is None:
        return jsonify({"status":201,"message":"invalid story_id"})

    extension = os.path.splitext(file.filename)[1]
    f_name = str(uuid.uuid4()) + extension
    file.save(os.path.join('static/images/story/'+str(user_data.id)+"/", f_name))

    targeted_story =Story.query.filter_by(id=story_id).first()
    targeted_story.story_image_url =('static/images/story/{}/{}'.format(user_data.id,f_name))
    db.session.add(targeted_story)
    db.session.commit()
    response_object = {
                    'status' : 200,
                    'message' : 'upload successfull',                     
                    'story_id': targeted_story.id,
                    'story_body' : targeted_story.body,
                    'story_image_url' : targeted_story.story_image_url,
                    'story_author_url' : url_for('accounts.get_user', user_id= targeted_story.author_id),
                    'story_url': url_for('story.get_story', story_id = targeted_story.id),
                    'user_id':targeted_story.author_id
                    
                  }

  
    return jsonify(response_object)



"""
------------------   GET STORIES --------------------

"""       


@app.route('/api/v1/get_stories', methods=('GET', 'POST'))
@jwt_required
def get_stories():
    #definations 
    data = request.json
    story_id = data.get("story_id")
    user_id = data.get("user_id")
    active_stories =[] 
    warning = []
    device_id =data.get('device_id')
    
    if not device_id:
       return jsonify('device_id missing')
    
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check data for blanks
    _user = Users.query.filter_by(status = 0).all()
    if not user_id:
        warning.append("user_id : user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)
    
    Story_data = Story.query.filter_by(status =0).all()
    if Story_data : 
        return jsonify([Story_.to_json() for Story_ in Story_data]) 
    else:
        return jsonify({"status":201, "message": "no storuies found!"})
