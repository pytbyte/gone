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



jobs_bp = Blueprint('jobs', __name__)
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


def notifier(activity,timestamp,message,data_url, user_data_url, status_code,post_id,story_id=0,job_id=0,bid_id=0):
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
------------------  CREATE JOB --------------------

"""
@jobs_bp.route('/api/v1/create_job', methods=('GET', 'POST'))
@jwt_required
def create_job():

        #variable diclaration and definations
    
        data= request.json
        body = data.get('job_body')
        user_id = data.get('user_id')
        status = data.get('status'),
        job_category = data.get('job_category')
        job_title = data.get('title')
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
        
        if not job_category:      
            warning.append(" job_category is missing")  
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)

        if not job_title:      
            warning.append(" job_title is missing")  
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)

        #validate

        if  Users.query.filter_by(id = user_id).first() is None:
            warning.append(" user_id is invalid")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)
        
        #check and set status to public if job status not specified
        if not status:
            warning.append(" status is missing")
            status = 0

        _user = Users.query.filter_by(id = user_id).first()
        #job creation
       
        new_job = Jobs(
            job_body = body,
            job_title = job_title,
            author_id = user_id,            
            job_post_category =job_category,
            status = 0,
            timestamp =sasa,
            )
        
        #for existing job
        if Jobs.query.filter_by(job_body=body).count() != 0:
            response_object ={
                              "status":201,
                              "message" : "A job post exists with similar description"
                              }
            return jsonify(response_object)
        
        exist= db.session.query(Jobs).filter(and_(Jobs.job_body ==body,Jobs.author_id == _user.id)).first()
        #check existance and handle new db inserts
        if not exist:
            db.session.add(new_job)
            db.session.commit()
            created_job = db.session.query(Jobs).filter(and_(Jobs.job_body ==body,Jobs.author_id == _user.id)).first()
            message = "{} added a job in {} category".format(_user.username,job_category)

            p= Jobs.query.filter_by(id=created_job.id).first()
            p_comm = p.author_id
            pcommenter  = Users.query.filter_by(id=p_comm).first()
            Post_owner =pcommenter.device_id
            registration_id =Post_owner

            notification = {
              "event_type": "job_creation",
              "body" :message,
              "title" : "iMarket",
              "image":_user.image_url,
              "link": url_for("jobs.get_job",job_id = created_job.id),
              "job_id": created_job.id,
              "user_id":_user.id,
              "name": _user.username
               }
            pusher(notification,registration_id)
            created_job = db.session.query(Jobs).filter(and_(Jobs.job_body ==body,Jobs.author_id == _user.id)).first()
            return jsonify(created_job.to_json())        


"""
------------------  JOB PIC UPLOAD --------------------

"""

@jobs_bp.route('/api/v1/job_image/<job_id>',  methods=('GET', 'POST'))
@jwt_required

def upload_job_pic(job_id):   

    if request.method == 'POST':
        username =  get_jwt_identity()

        user_data = Users.query.filter_by(username = get_jwt_identity()).first()   
        #get file from request and save
        file = request.files["file"]
        if not file:
             return jsonify("missing file to upload!")

        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('static/images/jobs/'+str(user_data.id)+"/", f_name))

        #get  userdata
        username =get_jwt_identity()
        user_data =Users.query.filter_by(username= username).first()

        #query job by latest job_id
        targeted_job = Jobs.query.filter_by(id= job_id).first()
        if not job_id:
            new_job = Jobs(
            job_image_url = ('static/images/jobs/'+str(user_data.id)+"/"+f_name),

            status = 0,
            author_id = user.id,
            timestamp  = saa,

            )  
            db.session.add(new_job)
            db.session.commit()
        elif job_id is not None:
            #add image url to post
            targeted_job.job_image_url = ('static/images/jobs/'+str(user_data.id)+"/"+f_name)
            db.session.add(targeted_job)
            db.session.commit()
        
        response_object = {
                        'status' : 200,
                        'message' : 'upload successfull',                     
                        'job_id': targeted_job.id,
                        'job_body' : targeted_job.job_body,
                        'job_image_url' : targeted_job.job_image_url,
                        'job_category' : targeted_job.job_post_category,
                        'job_author_url' : url_for('accounts.get_user', user_id=targeted_job.author_id),
                        'job_url': url_for('jobs.get_job', job_id = targeted_job.id),
                        'user_id': targeted_job.author_id
                        
                      }

      
        return jsonify(response_object)
  

  

"""
------------------   UPDATE JOB --------------------

"""

@jobs_bp.route('/api/v1/update_job', methods=('GET', 'POST','PUT')  )
@jwt_required
def update_job():
    
    #deffinations
    data = request.json
    
    body =data.get('job_body')
    status = data.get('status')
    user_id = data.get('user_id')
    job_id = data.get('job_id')
    job_title= data.get('job_title')
    job_category = data.get('job_category')
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
        
    if not job_id:      
        warning.append(" job_id is missing")
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
    
    if not job_title:      
        warning.append(" job_title is missing")  
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

    if Jobs.query.filter_by(id = job_id).first() is None:
        warning.append(" job_id is invalid")
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
                  "status":201,
                  "errors" : warning
              }  
         return jsonify(response_object)
    
    #verify a job to update by job_id and author_id
    _user = Users.query.filter_by(id =user_id).first()
    exist= db.session.query(Jobs).filter(and_(Jobs.author_id == _user.id,Jobs.id == job_id)).first()
    
    if not exist:
        response_object = {
          "status": 201,
          "errors": "job doesnt exist!"
        }
        return jsonify(response_object)
    
    #preserve unchanged fileds
    if  body == exist.job_body :          
        warning.append(" job already exists")                
    if body != exist.job_body:
       exist.job_body = body
    
    if  status == exist.status :          
        warning.append(" status unchanged")                
    if status != exist.status:
       exist.status = status

    if job_title == exist.job_title :          
        warning.append(" status unchanged")                
    if job_title != exist.job_title:
       exist.job_title = job_title
    #create update data
    exist.job_title =job_title
    exist.job_body =body
    exist.job_category = job_category
    exist.status = status
    db.session.add(exist)
    db.session.commit()
    
    #respond
    exis_t= db.session.query(Jobs).filter(and_(Jobs.author_id == _user.id,Jobs.id == job_id)).first()
    message = "{} updated their job post".format(str(get_jwt_identity()))

    notification = {
              "event_type": "job_update",
              "body" :message,
              "title" : "iMarket",
              "image":exis_t.job_image_url,
              "link": url_for("jobs.get_job",job_id = job_id),
              "job_id": job_id,
              "user_id":_user.id,
              "name": _user.username
               }
    #pusher(notification)
    return jsonify(exis_t.to_json())    



"""
------------------    CREATE JOB COMMENT  --------------------

""" 

@jobs_bp.route('/api/v1/job_comment', methods=('GET', 'POST'))        
@jwt_required
def create_job_comment():
    #deffinations
    data=request.json
    current_time = time.localtime()
    saa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    job_id = data.get('job_id')
    body= data.get("job_comment")
    user_id = data.get('user_id')
    warning=[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check for empty input
    if not user_id:      
        warning.append(" user_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }

        return jsonify(response_object)

    if not job_id:      
        warning.append(" job_id is missing")
        response_object = {
          "status":201,
          "errors": warning
        }        
        return jsonify(response_object)
    
    if not body:      
        warning.append(" job_comment is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)

    #verify user_id
        #verify user_id
    if Users.query.filter_by(id = user_id).first() is None : 
        warning.append("user_id : {} doesn't exist !".format(user_id))
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    if Jobs.query.filter_by(id= job_id).first() is None: 
        warning.append("job_id doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    #target a job to like by job_id and user_id
    exist= db.session.query(Jobs).filter(and_(Jobs.id == job_id,Jobs.status == 0)).first()
    
    #job missing
    if not exist:
        response_object = {
          "status": 201,
          "errors": " invalid job id."
        }
        return jsonify(response_object)

    #job missing
    if not exist:
        response_object = {
          "status": 201,
          "errors": " invalid job id."
        }
        return jsonify(response_object)


    #prepare comment_data
    comment = Comments(  

        job_id = job_id,
        author_id = user_id,
        body =body,
        timestamp =saa,
        disabled = 0,
        status = 0,
        )
    
    db.session.add(comment)
    db.session.commit()
    
    timestamp =saa    
    to_notify = user_id
    if to_notify == user_id:
        activity = "commented on your job"
    elif to_notify != user_id:
        activity = "commented on a job"
    
    usa_ = Comments.query.order_by(desc(Comments.timestamp)).filter_by(job_id = job_id).limit(1).one()
    user_=Users.query.filter_by(id = user_id).first()
    comments = []
    if not usa_:
        response_object={
            "status":201,
            "message":"no comment found"
           }
        return jsonify(response_object)
    if usa_:
        data_url= url_for("jobs.single_job_comment", comment_id = usa_.id)
        user_data_url= url_for("accounts.get_user",user_id=user_id),
        status_code=  0
        if status_code == 0:
            status_code = "Unread"
        elif status_code ==1:
            status_code = "read"

        #notify job owner and followers done in response_object
        message = ("{} {} ").format(user_.username, activity)
        notifier(activity,timestamp,message,data_url, user_data_url, status_code,post_id=0,story_id=0,job_id=job_id,bid_id=0)  
        print(message)
        #push notification
        p= Jobs.query.filter_by(id=job_id).first()
        p_comm = p.author_id
        pcommenter  = Users.query.filter_by(id=p_comm).first()
        job_owner =pcommenter.device_id
        registration_id = str(job_owner)
        notification = {
              "event_type": "job_comment",
              "body" :message,
              "title" : "iMarket",
              "image":user_.image_url,
              "link":data_url,
              "job_id": job_id,
              "user_id":user_.id,
              "name": user_.username
               }
        pusher(notification,registration_id)


        #return comment
        return jsonify( usa_.job_json())




"""
------------------   GET COMMENT --------------------

"""       
   

@jobs_bp.route('/api/v1/single_job_comment', methods=('GET', 'POST'))
@jwt_required
def single_job_comment():
    data = request.json
    comment_id =data.get("comment_id")
    warning= []
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    if not comment_id:
        warning.append("comment_id missing!")        
        return jsonify(warning)
  

    comment = Comments.query.filter_by(id = comment_id).first()

    if Comments.query.filter_by(id = comment_id).first() is None :
        response_object = {
        "status": 201,
        "message" : "no comment identified by id {}! ".format(comment_id)
        }
        return jsonify(response_object)

     
    if not comment : 
        response_object = {
        " status" : 201,
        "error" : " comment doesn't exists "

        }
        return jsonify(response_object)
    response_object ={
        "status":200,
        "content":comment.body,
        "commenter":comment.author_id,
        "comment_id" : comment.id,
        "job_id": comment.job_id

                  }
    return  jsonify(comment.job_json())


"""
------------------   GET JOB COMMENTS --------------------

"""
@jobs_bp.route('/api/v1/job_comments', methods=('GET', 'POST'))
@jwt_required
def job_comments():
    data = request.json
    
    warning= []
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()
    comments =db.session.query(Comments)
    

   
    if not comments:
        response_object ={
         " error": "comments doesn't exist",
         "status" :201
           }
        return jsonify(reponse_object)
    comments =db.session.query(Comments)

    return jsonify ([comment.job_json() for comment in comments])


   

"""
------------------   UPDATE JOB COMMENT --------------------

"""


@jobs_bp.route('/api/v1/update_job_comment', methods=('GET', 'POST', 'PUT'))
@jwt_required
def update_job_comments():
    
    #deffinations
    data = request.json
    
    body =data.get('job_comment')
    user_id = data.get('user_id')
    comment_id = data.get('comment_id')
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

    if not comment_id:      
        warning.append(" comment_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }
        return jsonify(response_object)


    #set status to public on default
   
    if Users.query.filter_by(id = user_id).first() is None:          
         warning.append(" user_id is invalid")
         #return response
         response_object = {
                  "status": 201,
                  "errors" : warning
              }  
         return jsonify(response_object )
    
    #verify a comment to update by comment_id and author_id
    _user = Users.query.filter_by(id =user_id).first()
    exist= db.session.query(Comments).filter(and_(Comments.author_id == _user.id,Comments.id == comment_id)).first()
    
    if not exist:
        response_object = {
          "status": 201,
          "errors": "comment doesnt exist!"
        }
        return jsonify(response_object)
    
    #preserve unchanged fileds
    if  body == exist.body :          
        warning.append(" comment already exists")
    if body != exist.body:
       exist.body = body    
    #create update data
    exist.body =body
    exist.status = 0
    db.session.add(exist)   
    db.session.commit()
    
    #respond
    return jsonify(exist.job_json())  



"""
------------------   GET JOB --------------------

"""       


@jobs_bp.route('/api/v1/get_job', methods=('GET', 'POST'))
@jwt_required
def get_job():
    #definations 
    data = request.json
    job_id = data.get("job_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_job_ids = []
    user_jobs = [] 
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
        warning.append("user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

    if not job_id:
        warning.append("job_id  is missing!")
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
    
    if Jobs.query.filter_by(id= job_id).first() is None: 
        warning.append("job_id doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    #get job_data   
    jobs= db.session.query(Jobs).filter(and_(Jobs.author_id == user_id,Jobs.id == job_id)).first()
    if jobs:
       return jsonify(jobs.to_json())
    else :
       response_object={
          "status": 201,
          "error" :  "job not found"
           }
       return jsonify(response_object)

"""
------------------------- GET USER JOBS -----------------------
"""
@jobs_bp.route('/api/v1/user_jobs',methods = ('GET','POST'))
@jwt_required
def user_jobs():

   data =request.json
   private =[]
   user_id = data.get("user_id")
   device_id =data.get('device_id')
   if not device_id:
       return jsonify('device_id missing')
   #update users device id
   username = get_jwt_identity()
   user_data = Users.query.filter_by(username = username).first()
   user_data.device_id = device_id
   db.session.commit()

   if not user_id:
    return jsonify("user_id missing!")
   if Users.query.filter_by(id=user_id).first() is None:
       return jsonify("invalid user_id")
   user_jobs = db.session.query(Jobs).filter(and_(Jobs.author_id ==user_id,Jobs.status ==0)).all()
   if not user_jobs:
       return jsonify("no jobs found for this user")
   return jsonify([u_j.to_json() for  u_j in user_jobs])

"""
------------------------------- GET ALL JOBS ------------------

"""
@jobs_bp.route('/api/v1/all_jobs',methods=("GET","POST"))
@jwt_required
def get_jobs():
    data = request.json
    user_id = data.get('user_id')
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    if not user_id:
      return  jsonify("missing user_id")
    if Users.query.filter_by(id= user_id).first() is None:
      return jsonify("invelid user_id")
    jobs = db.session.query(Jobs).all()
    return jsonify([job.to_json() for job in jobs])




"""
------------------   GET JOB BY CATEGORY--------------------

"""       


@jobs_bp.route('/api/v1/job_category', methods=('GET', 'POST'))
@jwt_required
def job_category():
    #definations 
    data = request.json
    job_category = data.get("job_category")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_job_categorys = []
    user_jobs = [] 
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
        warning.append("user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

    if not job_category:
        warning.append("job_category  is missing!")
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
    
    if Jobs.query.filter_by(job_post_category= job_category).first() is None: 
        warning.append("job_category doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    #get job_data   
    jobs= db.session.query(Jobs).filter(and_(Jobs.job_post_category == job_category, Jobs.status ==0)).all()   
    if jobs:
        return jsonify([job.to_json() for job in jobs])
    else:
       response_object = {"status" : 201, "error" :  "job doesn't  exist"}
       return jsonify(response_object)
  

"""
------------------  JOB SHARE MODULE --------------------

"""


@jobs_bp.route('/api/v1/job_share', methods=('GET', 'POST'))
@jwt_required
def create_job_share():

        #variable diclaration and definations
        current_time = time.localtime()
        sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        data= request.json
        job_id = data.get('job_id')
        user_id = data.get('user_id'),
        status = 0,
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
        # check for data presence
        if not job_id :      
            warning.append(" job_id is missing") 
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
        #check for data validity
        if Jobs.query.filter_by(id= job_id).first() is None: 
            warning.append("job_id : {} doesn't exist !".format(job_id))
            response_object = {
            "status": 201,
            "errors": warning
            }
            return jsonify(response_object)
        if Users.query.filter_by(id= user_id).first() is None: 
            warning.append("user_id doesn't exist!")
            response_object = {
            "status": 201,
            "errors": warning
            }
            return jsonify(response_object)
        #target a flag to delete by flag_id and user
        exist = db.session.query(Share).filter(and_(Share.user == user_id,Share.job_id == job_id)).first() 

        new_share = Share(
            job_id = job_id,
            status = status,           
            user=user_id,
            )      
        if not exist:  
            db.session.add(new_share)
            db.session.commit()

        created_shared =db.session.query(Share).filter(and_(Share.user == user_id,Share.job_id == job_id)).first() 

        #Share.query.order_by(desc(Share.timestamp)).filter_by(job_id = job_id).limit(1).one()
        print(created_shared)
        user = Users.query.filter_by(id= user_id).first()
        
        activity = 'shared a job'
        timestamp = sasa
        post_sharer = user.username
        data_url= url_for("jobs.get_job", job_id = job_id)
        user_data_url= url_for("accounts.get_user",user_id=user_id)
        status_code=  0
        if status_code == 0:
            status_code = "Unread"
        elif status_code ==1:
            status_code = "read"

        #notify post owner and followers done in response_object

        message = ("{} {} ").format(post_sharer,activity)
        print(message)

        P= Jobs.query.filter_by(id=job_id).first()
        p_comm = P.author_id
        pcommenter  = Users.query.filter_by(id=p_comm).first()
        Post_owner =pcommenter.device_id
        registration_id =str(Post_owner)


        notifier(activity,timestamp,message,data_url, user_data_url, status_code,post_id=0,story_id=0,job_id=P.id,bid_id=0)
        notification = {
              "event_type": "job_share",
              "body" :message,
              "title" : "iMarket",
              "image":user.image_url,
              "link": url_for("jobs.get_job",job_id = job_id),
              "job_id": job_id,
              "user_id":user.id,
              "name": user.username
               }
        pusher(notification,registration_id)
        #return share_data       
        return jsonify(created_shared.job_json())        




"""
------------------  CREATE BID --------------------

"""
@jobs_bp.route('/api/v1/create_bid', methods=('GET', 'POST'))
@jwt_required
def create_bid():

        #variable diclaration and definations
    
        data= request.json
        body = data.get('bid_body')
        user_id = data.get('user_id')
        status = data.get('status'),
        bid_ammount = data.get('bid_ammount')
        job_id = data.get('job_id')
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
        
        if not bid_ammount:      
            warning.append(" bid_ammount is missing")  
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)

        if not job_id:      
            warning.append(" job_id is missing")  
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)

        #validate

        if  Users.query.filter_by(id = user_id).first() is None:
            warning.append(" user_id is invalid")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)

        if  Jobs.query.filter_by(id = job_id).first() is None:
            warning.append(" job_id is invalid")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return jsonify(response_object)
        
        #check and set status to public if job status not specified
        if not status:
            warning.append(" status is missing")
            status = 0

        _user = Users.query.filter_by(id = user_id).first()
        #job creation
       
        new_bid = job_bid(
            bid_body = body,
            job_id = job_id,
            author_id = user_id,            
            bid_ammount =bid_ammount,
            status = 0,
            timestamp =sasa,
            )
        #for empty database tables
        if job_bid.query.filter_by(bid_body=body).count() == 0:
            db.session.add(new_bid)
            db.session.commit()      
            exist= db.session.query(job_bid).filter(and_(job_bid.bid_body ==body,job_bid.author_id == _user.id)).first()
            return exist.to_json()
            
        exist= db.session.query(job_bid).filter(job_bid.bid_body ==body).first()
        if  exist:
            db.session.add(new_bid)
            db.session.commit()
            created_job = db.session.query(job_bid).filter(and_(job_bid.bid_body ==body,job_bid.author_id == _user.id)).first()
            message = "{} added a bid on a job. ".format(_user.username)
            P= job_bid.query.filter_by(job_id=job_id).first()
            p_comm = P.author_id
            pcommenter  = Users.query.filter_by(id=p_comm).first()
            Post_owner =pcommenter.device_id
            registration_id =str(Post_owner)



            notification = {
              "event_type": "create_bid",
              "body" :message,
              "title" : "iMarket",
              "image":_user.image_url,
              "link": url_for("jobs.get_job",job_id =exist.job_id),
              "job_id":exist.job_id,
              "user_id":_user.id,
              "name": _user.username
               }
            #pusher(notification,registration_id)
            return jsonify(created_job.to_json()) 
          


"""
------------------   UPDATE BID --------------------

"""

@jobs_bp.route('/api/v1/update_bid', methods=('GET', 'POST', 'PUT'))
@jwt_required
def update_bid():
    
    #deffinations
    data = request.json
    
    body =data.get('bid_body')
    user_id = data.get('user_id')
    bid_id = data.get('bid_id')
    status = data.get('status')
    bid_ammount = data.get('bid_ammount')
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
        
    if not bid_ammount:      
        warning.append(" bid_ammount is missing")
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
    
    if not bid_id:      
        warning.append(" bid_id is missing")  
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

    if job_bid.query.filter_by(id = bid_id).first() is None:
        warning.append(" bid_id is invalid")
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
                  "status":201,
                  "errors" : warning
              }  
         return jsonify(response_object)
    
    #verify a job to update by bid_bid and author_id
    _user = Users.query.filter_by(id =user_id).first()
    exist= db.session.query(job_bid).filter(and_(job_bid.author_id == _user.id,job_bid.id == bid_id)).first()
    
    if not exist:
        response_object = {
          "status": 201,
          "errors": "job doesnt exist!"
        }
        return jsonify(response_object)
    
    #preserve unchanged fileds
    if  body == exist.bid_body :          
        warning.append(" job already exists")                
    if body != exist.bid_body:
       exist.bid_body = body
    
    if  status == exist.status :          
        warning.append(" status unchanged")                
    if status != exist.status:
       exist.status = status

    if bid_ammount == exist.bid_ammount:          
        warning.append(" status unchanged")                
    if bid_ammount  != exist.bid_ammount :
       exist.bid_ammount = bid_ammount 
    #create update data
    
    exist.bid_body =body
    exist.bid_ammount = bid_ammount
    exist.status = status

    db.session.commit()
    
    #respond
    job = Jobs.query.filter_by(id =exist.job_id).first()
    exis_t= db.session.query(job_bid).filter(and_(job_bid.author_id == user_id,  job_bid.id == bid_id)).first()
    message = "{} updated their bid".format(get_jwt_identity())
    notification = {
              "event_type": "bid_update",
              "body" :message,
              "title" : "iMarket",
              "image":job.job_image_url,
              "link": url_for("jobs.get_bid",bid_id = exis_t.id),
              "bid_id": exis_t.id,
              "user_id":user_id,
              "name": str(get_jwt_identity())
               }
    #pusher(notification)
    return jsonify(exis_t.to_json())    



"""
------------------   GET BID--------------------

"""       


@jobs_bp.route('/api/v1/get_bid', methods=('GET', 'POST'))
@jwt_required
def get_bid():
    #definations 
    data = request.json
    bid_id = data.get("bid_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_bid_bids = []
    user_bid_bid = [] 
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
        warning.append("user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

    if not bid_id:
        warning.append("bid_id  is missing!")
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
    
    if job_bid.query.filter_by(id= bid_id).first() is None: 
        warning.append("job_bid doesn't exist !")
        response_object = {
        "status": 1,
        "errors": warning
        }
        return jsonify(response_object)
    #get bid_data   
    bid_bid= db.session.query(job_bid).filter(and_(job_bid.status == 0, job_bid.id == bid_id)).first()
    if bid_bid :   
        return jsonify(bid_bid.to_json())
    else:
        response_object = {"status": 201, "error" : "bid  missing"}
        return jsonify(response_object)


"""
------------------   GET JOB BIDS --------------------

"""       

@jobs_bp.route('/api/v1/job_bids', methods=('GET', 'POST'))
@jwt_required
def job_bids():
    #definations 
    data = request.json
    job_id = data.get("job_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_bid_bids = []
    user_bid_bid = [] 
    warning = []

    #check data for blanks
    _user = Users.query.filter_by(status = 0).all()
    if not user_id:
        warning.append("user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

    if not job_id:
        warning.append("job_id  is missing!")
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
    
    if job_bid.query.filter_by(job_id=job_id).first() is None: 
        warning.append("job_bid doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    #get bid_data 
    bids= {}  
    bid_bid= db.session.query(job_bid).filter(job_bid.job_id ==job_id).all()
    if bid_bid:  
       return jsonify([bid_.to_json() for bid_ in bid_bid])
    else:
        response_object = {"status" : 201,"error" : "bid missing"}
        return jsonify(response_object)

"""
---------------------  JOB_BIDDERS ---------------

"""


@jobs_bp.route('/api/v1/job_bidders', methods=("GET","POST"))
@jwt_required
def job_bidders():
    #get request_data 
    data=request.json
    job_id = data.get('job_id')
    user_id = data.get('user_id')
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
    # check for data presence
    if not job_id :      
        warning.append(" job_id is missing") 
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)

    if not user_id:
        warning.append(" job_id is missing") 
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)

    if  Users.query.filter_by(id =user_id).first() is None:
        warning.append(" invalid user_id") 
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)   

    if   Jobs.query.filter_by(id= job_id).first() is None: 
        warning.append(" invalid job_id") 
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)





 
    likers_list =[]

   
    job_bidder = job_bid.query.filter_by(job_id =job_id).all()
    x=[]
    y = []
    z =[]
    d =[]
    for job_ in  job_bidder:
        x.append(job_.author_id)

    for item in x:
        user_ = Users.query.filter_by(id = item).first()
        if user_.username not in y:
             z.append(str(url_for("accounts.get_user",user_id = user_.id)))
             y.append(str(user_.username))

    for item in  z:
       c =str(" %s")%(item)
       c_= str(" %s")%(user_.id)
       C={"bidder_url":c,"user_id":c_, "job_id":job_id}
       if c not in d:
          d.append(C)

    return jsonify(d), 200










"""
------------------   DELETE BID--------------------

"""       


@jobs_bp.route('/api/v1/delete_bid', methods=('GET', 'POST'))
@jwt_required
def delete_bid():
    #definations 
    data = request.json
    bid_id= data.get("bid_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_bid_bids = []
    user_bid_bid = [] 
    warning = []

    #check data for blanks
    _user = Users.query.filter_by(status = 0).all()
    if not user_id:
        warning.append("user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

    if not bid_id:
        warning.append("bid_id is missing!")
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
    
    if job_bid.query.filter_by(id=bid_id).first() is None: 
        warning.append("job_bid doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    #get bid_data   
    bid_bid= db.session.query(job_bid).filter(and_(job_bid.author_id == user_id, job_bid.id==bid_id)).first()
    if bid_bid:
        db.session.delete(bid_bid)
        db.session.commit()

        response_object = {
        "status": 200,
        "bid_id" : bid_id,
        "user_id": user_id,
        "errors": "bid deleted successfully"
        }
        return jsonify(response_object)
    if not  bid_bid:
        response_object = {
        "status":201,
        "error": "bid doesnt match user_id"
         }
        return jsonify(response_object)




    


"""
------------------   DELETE JOB --------------------

"""       


@jobs_bp.route('/api/v1/delete_job', methods=('GET', 'POST'))
@jwt_required
def delete_job():
    #definations 
    data = request.json
    job_id= data.get("job_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_bid_bids = []
    user_bid_bid = [] 
    warning = []

    #check data for blanks
    _user = Users.query.filter_by(status = 0).all()
    if not user_id:
        warning.append("user_id is missing!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

    if not job_id:
        warning.append("job_id is missing!")
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
    
    if Jobs.query.filter_by(id=job_id).first() is None: 
        warning.append("job doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    #get job_data   
    job_data= db.session.query(Jobs).filter(and_(Jobs.author_id == user_id, Jobs.id==job_id)).first()
    if job_data:
        job_data.status =1
        db.session.commit()

        response_object = {
        "job_id" : job_id,
        "status": 200,
        "errors": "job deleted successfully"
        }
        return jsonify(response_object)
    if not  job_data:
        response_object = {
        "status":201,
        "job_id" : job_id,
        "error": "job doesnt exist"
         }
        return jsonify(response_object)


    if  job_data.author_id != user_id:
         response_object={
                         "status" : 201,
                         "error" : "permission denied!",
                         "job_id" : job_id,
                         "user_id": user_id,
                         "job_author_id" : job_data.author_id,
                         }
         return jsonify(response_object)


"""
------------------   HIDE JOB --------------------

"""       
@jobs_bp.route('/api/v1/hide_job', methods=('GET', 'POST'))        
@jwt_required
def hide_job():
    #deffinations
    data= request.json
    user_id = data.get('user_id')
    job_id = data.get('job_id')
    warning=[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check for empty input
    if not user_id:      
        warning.append(" user_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }        
        return jsonify(response_object)

    if not job_id:
        warning.append(" job_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    hidden_job = db.session.query(Jobs).filter(and_(Jobs.status == 0, Jobs.id == job_id)).first()
    if not hidden_job:
       return jsonify({"status": 201, "message":"no active job identified by job_id:  {} ".format(job_id)})
    elif  hidden_job:
       hidden_job.status = 3
       if hidden_job.author_id != user_id:
         return jsonify({"status" : 201, "message": "Permission denied! edith wht you've authored."})
       db.session.commit()
       return jsonify({"status" : 200, "message":"job data is now hidden", "job_data" : hidden_job.to_json()})



"""
------------------   UNHIDE JOB --------------------

"""       
@jobs_bp.route('/api/v1/unhide_job', methods=('GET', 'POST'))        
@jwt_required
def unhide_job():
    #deffinations
    data= request.json
    user_id = data.get('user_id')
    job_id = data.get('job_id')
    warning=[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check for empty input
    if not user_id:      
        warning.append(" user_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
         }        
        return jsonify(response_object)

    if not job_id:
        warning.append(" job_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    hidden_job = db.session.query(Jobs).filter(and_(Jobs.status == 3, Jobs.id == job_id)).first()
    if not hidden_job:
       return jsonify({"status": 201, "message":"no active job identified by job_id:  {} ".format(job_id)})
    elif  hidden_job:
       hidden_job.status = 0
       if hidden_job.author_id != user_id:
         return jsonify({"status" : 201, "message": "Permission denied! edith wht you've authored."})
       db.session.commit()
       return jsonify({"status" : 200, "message":"job data is now visible", "job_data" : hidden_job.to_json()})

