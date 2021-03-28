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
posts_bp = Blueprint('posts', __name__)

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


def notifier(activity,timestamp,message,data_url,user_data_url,status_code,post_id,story_id,job_id,bid_id,author,user):
     """
       save notifications from activities

     """
     notification = Notification(

                   activity = activity,
                   user = user,
                   author =author,
                   timestamp =timestamp,
                   message = message,
                   data_url = data_url,
                   user_data_url = user_data_url,
                   status_code = status_code,
                   post_id = post_id,
                   story_id=story_id,
                   job_id= job_id,
                   bid_id=bid_id


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
------------------  CREATE POST --------------------

"""

@posts_bp.route('/api/v1/create_post', methods=('GET', 'POST'))
@jwt_required
def create_post():

        #variable diclaration and definations
    
        data= request.json
        body = data.get('body')
        user_id = data.get('user_id')
        status = data.get('status'),
        post_category = data.get('post_category')
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
            return response_object
        
        if not user_id:
            warning.append(" user_id is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
        
        if not post_category:      
            warning.append(" post_category is missing")  
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
        #validate

        if Users.query.filter_by(id = user_id).first() is None:
            warning.append(" user_id is invalid")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
       
        
        #check and set status to public if post status not specified
        if not status:
            warning.append(" status is missing")
            status = 0

        # duplicate value error handling 
        _post = Posts.query.filter_by(status = 0).all()
        existing_post_ids = []
        existing_user_ids = []
        
      
        #check user_id:
        _user = Users.query.filter_by(status =0).all()
      
        for _user_ in _user:
            existing_user_ids.append(_user_.id)

        if Users.query.filter_by(id = user_id).first() is None:          
              warning.append(" user_id is invalid")                 
              #return response
              response_object = {
                  "status":201,
                  "errors" : warning
                }  
              return response_object 
        
        #check post_id
        for _post_ in _post:
            existing_post_ids.append(_post_.id)
            
   
            
        #get user data via user_id
        _user = Users.query.filter_by(id = user_id).first()
        #post creation
       
        new_post = Posts(
            body = body,
            author_id = user_id,
            
            post_category =post_category,
            status = status,
            timestamp =sasa,
            )
        #for empty database tables
        if Posts.query.filter_by(body=body).count() == 0:
            db.session.add(new_post)
            db.session.commit()
            exist= db.session.query(Posts).filter(and_(Posts.body ==body,Posts.author_id == _user.id)).first()
            created_post = exist
            message = "{} added a post in {} category".format(_user.username,exist.post_category)
            to_usr=[]
            to_=Follows.query.filter_by(followed_id= user_id).all()

            for t in to_:
              to_u =Users.query.filter_by(id=t.follower_id).first()
              to_usr.append(to_u.device_id)
              registration_id = str(to_usr)
              notification = {
                      "event_type": "post_creation",
                      "body" :message,
                      "title" : "iMarket",
                      "image":_user.image_url,
                      "link": url_for("posts.get_post",post_id = exist.post_id),
                      "post_id": exist.post_id,
                      "user_id":_user.id,
                      "name": _user.username
                       }
             #pusher(notification,registration_id)

            return created_post.to_json()       
        exist= db.session.query(Posts).filter(and_(Posts.body ==body,Posts.author_id == _user.id)).first()
        if not exist:
            db.session.add(new_post)
            db.session.commit()
            created_post = exist
            message = "{} added a post in {} category".format(exist.username,exist.post_category)
            to_usr=[]
            to_=Follows.query.filter_by(followed_id= user_id).all()

            for t in to_:
              to_u =Users.query.filter_by(id=t.follower_id).first()
              to_usr.append(to_u.device_id)
              registration_id = str(to_usr)
              notification = {
	              "event_type": "post_creation",
	              "body" :message,
	              "title" : "iMarket",
	              "image":_user.image_url,
	              "link": url_for("posts.get_post",post_id = exist.post_id),
	              "post_id": exist.post_id,
	              "user_id":_user.id,
	              "name": _user.username
	               }
            pusher(notification,registration_id)
            return created_post.to_json()        
            
        
        if exist :
            warning.append(" post data exists")                 
            #return response
            response_object = {
              "status":201,
              "errors" : warning
            }  
            return jsonify(response_object) 
        #show private post to the post author   
        if exist.status == 1 and exist.author_id ==_user.id:
            created_post = exist
            #return post_data
            return created_post.to_json()   





"""
---------------------------   UPDATE POST --------------------

"""

@posts_bp.route('/api/v1/update_post', methods=('GET', 'POST', 'PUT'))
@jwt_required
def update_post():
    
    #deffinations
    data = request.json
    
    body =data.get('body')
    status = data.get('status')
    user_id = data.get('user_id')
    post_id = data.get('post_id')
    post_category = data.get('post_category')
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
        
    if not post_id:      
        warning.append(" post_id is missing")
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
        return  jsonify(response_object)
    


    if Posts.query.filter_by(id = post_id).first() is None:
        warning.append(" post_id is invalid")
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
    
    #verify a post to update by post_id and author_id
    _user = Users.query.filter_by(id =user_id).first()
    exist= db.session.query(Posts).filter(and_(Posts.author_id == _user.id,Posts.id == post_id)).first()
    
    if not exist:
        response_object = {
          "status": 201,
          "errors": "post doesnt exist!"
        }
        return  jsonify(response_object)
    
    #preserve unchanged fileds
    if  body == exist.body :          
        warning.append(" post already exists")                
    if body != exist.body:
       exist.body = body
    
    if  status == exist.status :          
        warning.append(" status unchanged")                
    if status != exist.status:
       exist.status = status
    
    #create update data
    exist.body =body
    exist.post_category = post_category
    exist.status = status
    db.session.add(exist)
    db.session.commit()
    
    #respond
    return jsonify(exist.to_json())



"""
------------------   UPLOAD POST IMAGE --------------------

"""


@posts_bp.route('/api/v1/post_image/<post_id>',  methods=('GET', 'POST'))
@jwt_required
def upload_post_pic(post_id):   
    """
    works by attaching image_url to a fresh post 
  
    """  
    #deffinations
    data =request
    warning =[]
    #validate existance
  

    if  Posts.query.filter_by(id = post_id).first() is None:
        warning.append(" post_id is invalid")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return jsonify(response_object)

    if request.method == 'POST':
        user_data = Users.query.filter_by(username = get_jwt_identity()).first()   
        #get file from request and save
        file = request.files["file"]
        if not file:
             return jsonify({"status":201,"message":"missing file to upload!"})
    
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('static/images/posts/'+str(user_data.id)+"/", f_name))            
       
        #get  userdata
        username =get_jwt_identity()
        user_data =Users.query.filter_by(username= username).first()    
        
        #query post by latest post_id
        targeted_post = Posts.query.filter_by(id= post_id).first()
        if not post_id:
            new_post = Posts(
            post_image_url = ('static/images/posts/'+str(user_data.id)+"/"+f_name),
            
            status = 0,
            author_id = user.id,
            timestamp  = saa,
            
            )  
            db.session.add(new_post)
            db.session.commit()
        elif post_id is not None:
            #add image url to post
            targeted_post.post_image_url = ('static/images/posts/'+str(user_data.id)+"/"+f_name)
            db.session.add(targeted_post)
            db.session.commit()

     

        response_object = {
                        'status' : 200,
                        'user_id':targeted_post.author_id,
                        'message' : 'upload successfull',                     
                        'post_id': targeted_post.id,
                        'post_body' : targeted_post.body,
                        'post_image_url' : targeted_post.post_image_url,
                        'post_category' : targeted_post.post_category,
                        'post_author_url' : url_for('accounts.get_user', id= user_data.id),
                        'post_data_url': url_for("posts.get_post", post_id = targeted_post.id)
                      
                      }
      
        return jsonify(response_object)




"""
------------------   LIKE POST --------------------

"""       


@posts_bp.route('/api/v1/like_post', methods=('GET', 'POST'))        
@jwt_required
def like_post():
    #deffinations
    data= request.json
    user_id = data.get('user_id')
    post_id = data.get('post_id')
    warning=[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify({"status":201,"message":'device_id missing'})
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

    if not post_id:      
        warning.append(" post_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    
    #validate existance

    if  Users.query.filter_by(id = user_id).first() is None:
        warning.append(" user_id is invalid")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return jsonify(response_object)
    


    if Posts.query.filter_by(id = post_id).first() is None:
        warning.append(" post_id is invalid")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return jsonify(response_object)

    #target a post to like by post_id and user_id
    exist= db.session.query(Posts).filter(and_(Posts.id == post_id,Posts.status == 0)).first()
    
    #post missing
    if not exist:
        response_object = {
          "status": 201,
          "errors": "post doesnt exist! check inputs and try again"
        }
        return jsonify(response_object)
    
    #get user_data
    user =Users.query.filter_by(id= user_id).first()
    likes= db.session.query(Likes).filter(and_(Likes.liker == user_id,Likes.post_id == post_id)).first()
    lik = Likes(
        post_id = post_id,
        liker =user_id,
      
            )
   
    if likes:
        response_object = {
          "status": 201,
          "errors": "post like exist!"
        }
        return jsonify(response_object)
    if not likes:
        db.session.add(lik)
        db.session.commit()
        likes= db.session.query(Likes).filter(and_(Likes.liker == user_id,Likes.post_id == post_id)).first()
        t_post = Posts.query.filter_by(id=post_id).first()
       
        activity = "liked your post"
        timestamp = sasa
        data_url= url_for("posts.get_post",post_id=post_id)
        user_data_url= url_for("accounts.get_user",user_id=user_id)
        post_id = post_id
        user = user_id
        author = t_post.author_id
        job_id = "0"
        bid_id = "0"
        story_id= "0"

        status_code=  0
        if status_code == 0:
           status_code = "Unread"
        elif status_code == 1:
           status_code = "read"
    

        #get liked post
        target_post = Posts.query.filter_by(id=post_id).first()
        #get user_id from post
        id_=target_post.author_id
        target_user =Users.query.filter_by(id=id_).first()
        _user =Users.query.filter_by(id=user_id).first()     
        #get device_id from user_id 
        dev_id = target_user.device_id
        registration_id= str(dev_id)

        message = ("{} liked your post").format(_user.username)
        notifier(activity,timestamp,message,data_url, user_data_url, status_code,post_id=target_post.id,story_id=0,job_id=0,bid_id=0,author=author,user=user_id)  
        notification = {
           "event_type": "Post_like",
           "body": message,
           "title" : "iMarket",
           "image": target_user.image_url,
           "user_id": target_user.id,
           "name": target_user.username
           }
        pusher(notification,registration_id)

        return jsonify(likes.to_json())





"""
------------------   UNLIKE POST --------------------

"""       

@posts_bp.route('/api/v1/unlike_post', methods=('GET', 'POST'))
@jwt_required
def unlike_post():
    """
    unlike post by user_id and post_id
    
    """
    #deffinations
    data = request.json
    post_id = data.get('post_id')
    user_id = data.get("user_id")
    warning =[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()
    
    #handle empty_input
    if not user_id:      
        warning.append(" user_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)

    if not post_id:      
        warning.append("post_id is missing")
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
 

    if db.session.query(Likes).filter(and_(Likes.post_id == post_id, Likes.liker == user_id)).first() is None:
        warning.append(" like_id doesnt exist")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return jsonify(response_object)
    

        
    #get like by like_id and user_id and delet it
    likes= db.session.query(Likes).filter(and_(Likes.post_id == post_id,Likes.liker == user_id)).first()
    if likes:
        db.session.delete(likes)
        db.session.commit()
        response_object ={
           'message': 'unlike successfull',
           'status': 200,
           'post_id': post_id,
           'user_id' : user_id,
           'user_url': url_for("accounts.get_user",user_id=user_id),
           'post_url': url_for("posts.get_post",post_id=post_id)
            }
         
        unliker = Users.query.filter_by(id=user_id).first()

        t_post= Posts.query.filter_by(id = post_id).first()
        activity = "unliked your post"
        timestamp = sasa
        data_url= url_for("posts.get_post",post_id=post_id)
        user_data_url= url_for("accounts.get_user",user_id=user_id)
        post_id = post_id
        user = user_id
        author = t_post.author_id
        job_id = "0"
        bid_id = "0"
        story_id= "0"
        status_code = 0
        if status_code == 0:
           status_code = "Unread"
        elif status_code == 1:
           status_code = "read"
    

        #get liked post
        target_post = Posts.query.filter_by(id=post_id).first()
        #get user_id from post
        id_=target_post.author_id
        target_user =Users.query.filter_by(id=id_).first()
    
        #get device_id from user_id 
        dev_id = target_user.device_id
        registration_id= str(dev_id)

        message = ("{} unliked your post").format(unliker.username)
        notifier(activity,timestamp,message,data_url,user_data_url,status_code,post_id,story_id,job_id,bid_id)
        notification = {
           "event_type": "Post_unlike",
           "body": message,
           "title" : "iMarket",
           "image":unliker.image_url,
           "user_id":unliker.id,
           "name": unliker.username
           }
        pusher(notification,registration_id)



        return jsonify(response_object)
    if not likes:
        response_object ={
           'message': 'you have already unliked post',
           'status': 201
            }

        return jsonify(response_object)





"""

------------------------- GET USER_POSTS --------------------------

"""
@posts_bp.route('/api/v1/user_posts' ,methods=('GET','POST'))
@jwt_required
def get_posts():
    #definations
    data = request.json
    user_id = data.get("user_id")
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #snitize 
    if not user_id:
       response_object = {"status":201, "error":"user_id missing!"}
       return jsonify(response_object)
    if db.session.query(Users).filter(and_(Users.id == user_id,Users.status ==0)).first() is None:
       response_object ={"status" : 201,"error": "invalid user id!"}
       return jsonify(response_object)
    #get posts
    posts = db.session.query(Posts).filter(and_(Posts.author_id == user_id,Posts.status ==0)).all()
    if not posts:
       response_object = {"status": 200, "message":"no post under this user_id"}
       return jsonify(response_object)

    return  jsonify([post.to_json() for post in posts])





"""
------------------   GET POST --------------------

"""       


@posts_bp.route('/api/v1/get_post', methods=('GET', 'POST'))
@jwt_required
def get_post():
    #definations 
    data = request.json
    post_id = data.get("post_id")
    user_id = data.get("user_id")
    existing_user_ids = []
    existing_post_ids = []
    user_posts = [] 
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
    
    if Posts.query.filter_by(id= post_id).first() is None: 
        warning.append("post_id doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
        
    #get post_data   
    posts= db.session.query(Posts).filter(and_(Posts.author_id == user_id,Posts.id == post_id)).first()
    
    if posts:
       return jsonify(posts.to_json())
    elif not posts:
       response_object = {
       "status" : 201,
       "error" : "post not available."
        }
       return jsonify(response_object)


"""
-------------------- POST LIKES --------------------

"""
@posts_bp.route('/api/v1/all_post_likes', methods=("GET","POST"))
@jwt_required
def all_post_likes():
     data= request.json
     user_id = data.get('user_id')
     if not user_id:
         return ('user_id missing')
     device_id =data.get('device_id')

     if not device_id:
       return jsonify('device_id missing')

     #update users device id
     username = get_jwt_identity()
     user_data = Users.query.filter_by(username = username).first()
     user_data.device_id = device_id
     db.session.commit()

     #validate existance

     if Users.query.filter_by(id = user_id).first() is None:
        warning.append(" user_id is invalid")
        response_object = {
          "status": 201,
          "errors": warning
        }
        return jsonify(response_object)
     like_data =Likes.query
     return jsonify ([like.to_json() for like in like_data])



"""
------------------    CREATE COMMENT  --------------------

""" 

@posts_bp.route('/api/v1/comments', methods=('GET', 'POST'))        
@jwt_required
def create_comment():
    #deffinations
    data=request.json
    current_time = time.localtime()
    saa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    post_id = data.get('post_id')
    body= data.get("post_comment")
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

    if not post_id:      
        warning.append(" post_id is missing")
        response_object = {
          "status":201,
          "errors": warning
        }        
        return jsonify(response_object)
    
    if not body:      
        warning.append(" post_comment is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
         
    #verify user_id
    if Users.query.filter_by(id = user_id).first() is None : 
        warning.append("user_id : {} doesn't exist !".format(user_id))
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    
    if Posts.query.filter_by(id= post_id).first() is None: 
        warning.append("post_id doesn't exist !")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)
    #target a post to like by post_id and user_id
    exist= db.session.query(Posts).filter(and_(Posts.id == post_id,Posts.status == 0)).first()
    
    #post missing
    if not exist:
        response_object = {
          "status": 201,
          "errors": " invalid post id."
        }
        return jsonify(response_object)

         
    #prepare comment_data
    comment = Comments(  
         
        post_id = post_id,
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
        activity = "commented on your post"
    elif to_notify != user_id:
        activity = "commented on a post"

    usa_ = Comments.query.order_by(desc(Comments.timestamp)).filter_by(post_id = post_id).limit(1).one()
    user_=Users.query.filter_by(id = user_id).first()
    comments = []
    if usa_:

        data_url= url_for("posts.get_comment",comment_id=usa_.id)
        user_data_url= url_for("accounts.get_user",user_id=user_id)
        post_id = post_id
        user = user_id
        author = usa_.author_id
        job_id = "0"
        bid_id = "0"
        story_id= "0"
 
        status_code=  0
        if status_code == 0:
            status_code = "Unread"
        elif status_code ==1:
            status_code = "read"

        #notify post owner and followers done in response_object
        message = ("{} {} ").format(user_.username, activity)
        notifier(activity,timestamp,message,data_url,user_data_url,status_code,post_id,story_id,job_id,bid_id,author,user) 
        print(message)
        #push notification
        p= Posts.query.filter_by(id=post_id).first()
        p_comm = p.author_id
        pcommenter  = Users.query.filter_by(id=p_comm).first()
        Post_owner =pcommenter.device_id
        registration_id = str(Post_owner)
        notification = {
              "event_type": "post_comment",
              "body" :message,
              "title" : "iMarket",
              "image":user_.image_url,
              "link":data_url,
              "post_id": post_id,
              "user_id":user_.id,
              "name": user_.username
               }
        pusher(notification,registration_id)

            
    #return comment
    return jsonify(usa_.to_json())


"""
------------------   UPDATE COMMENT --------------------

"""


@posts_bp.route('/api/v1/update_comment', methods=('GET', 'POST', 'PUT'))
@jwt_required
def update_comments():
    
    #deffinations
    data = request.json
    
    body =data.get('post_comment')
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
         return jsonify(response_object)
    
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
    return jsonify(exist.to_json())    





"""
------------------   GET COMMENT --------------------

"""       
   

@posts_bp.route('/api/v1/comment', methods=('GET', 'POST'))
@jwt_required
def get_comment():
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
        return warning
  

    comment = Comments.query.filter_by(id = comment_id).first()
     
    if Comments.query.filter_by(id = comment_id).first() is None :
        response_object = {
        "status": 201,
        "message" : "no comment identified by id {}! ".format(comment_id)
        }
        return response_object

 
    
    if not comment : 
        response_object = {
        " status" : 201,
        "error" : " comment doesn't exists "

        }
        return response_object
    response_object ={
        "status":200,
        "content":comment.body,
        "commenter":comment.author_id,
        "comment_id" : comment.id,
        "post_id": comment.post_id

                  }
    return  comment.to_json()


"""
------------------   GET POST COMMENTS --------------------

"""
@posts_bp.route('/api/v1/post_comments', methods=('GET', 'POST'))
@jwt_required
def post_comments():
    data = request.json
   # post_id =data.get("post_id")
    warning= []
    post_comments =[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()
    
    comments =db.session.query(Comments).filter(and_(Comments.status ==0, Comments.post_id >=1 )).all()
    for comment in comments: 
        dead_posts= Posts.query.filter_by(status = 1).all()
        for dead_post in dead_posts:
           if  comment.post_id != dead_post.id:
               post_comments.append(comment)
    return jsonify ([comment.to_json() for comment in post_comments])
    if not comments:
        response_object ={
         " error": "comments doesn't exist",
         "status" :201
           }
        return jsonify(reponse_object)





"""
------------------  SHARE POST --------------------

"""

@posts_bp.route('/api/v1/post_share', methods=('GET', 'POST'))
@jwt_required
def create_post_share():

        #variable diclaration and definations
        current_time = time.localtime()
        sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        data= request.json
        post_id = data.get('post_id')
        user_id = data.get('user_id'),
        status = 0,
        timestamp =sasa
        warning = []
        device_id =data.get('device_id')
        if not device_id:
             return jsonify({"status":201, "message":'device_id missing'})
        #update users device id
        username = get_jwt_identity()
        user_data = Users.query.filter_by(username = username).first()
        user_data.device_id = device_id
        db.session.commit()


        #data validation
        # check for data presence
        if not post_id :      
            warning.append(" post_id is missing") 
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
        if Posts.query.filter_by(id= post_id).first() is None: 
            warning.append("post_id : {} doesn't exist !".format(post_id))
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
        exist = db.session.query(Share).filter(and_(Share.user == user_id,Share.post_id == post_id)).first() 

        new_share = Share(
            post_id = post_id,
            status = status,           
            user=user_id,
            )      
        if not exist:  
            db.session.add(new_share)
            db.session.commit()

        created_shared =db.session.query(Share).filter(and_(Share.user == user_id,Share.post_id == post_id)).first() 

        #Share.query.order_by(desc(Share.timestamp)).filter_by(post_id = post_id).limit(1).one()
        print(created_shared)
        user = Users.query.filter_by(id= user_id).first()
        activity = 'shared a post'
        timestamp = sasa
        post_sharer = user.username
        data_url= url_for("posts.get_post", post_id = post_id)
        user_data_url= url_for("accounts.get_user" ,user_id=user_id)
        status_code=  0
        if status_code == 0:
              status_code = "Unread"
        elif status_code ==1:
              status_code = "read"

        #notify post owner and followers done in response_object
        post_sharer = user.username
  
        message = ("{} {} ").format(post_sharer,activity)
        print(message)
        notifier(activity,timestamp,message,data_url, user_data_url, status_code, post_id = post_id ,job_id = 0, story_id=0, bid_id =0)
       
        p= Posts.query.filter_by(id=post_id).first()
        p_comm = p.author_id
        pcommenter  = Users.query.filter_by(id= p_comm).first()
        Post_owner = pcommenter.device_id
        registration_id =str(Post_owner)
        notification = {
              "event_type": "post_share",
              "body" :message,
              "title" : "iMarket",
              "image":user.image_url,
              "link": url_for("posts.get_post",post_id = post_id),
              "post_id":post_id,
              "user_id":user.id,
              "name":post_sharer
               }
        pusher(notification,registration_id)
        #return share_data
        
        print(message)
        return jsonify(created_shared.post_json())     







"""
------------------   DELETE COMMENT --------------------

""" 


@posts_bp.route('/api/v1/delete_comment', methods=('GET', 'POST'))
@jwt_required
def delete_comment():
    #deffinations
    data = request.json
    comment_id = data.get('comment_id')
    user_id = data.get('user_id')
    warning =[]
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()
                       
    #check for empty inputs                  
    if not comment_id:
        warning.append("comment_id missing!")
        response_object = {
          "status": 201,
          "errors": warning
           }        
        return jsonify(response_object)

    if not user_id:
        warning.append("user_id missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
                       
    #verify inputs
    if Users.query.filter_by(id = user_id).first() is None:          
              warning.append(" user_id is invalid")                 
              #return response
              response_object = {
                  "status":201,
                  "errors" : warning
                }  
              return jsonify(response_object)
                       
    if Comments.query.filter_by(id = comment_id).first() is None:          
              warning.append(" comment_id is invalid")                 
              #return response
              response_object = {
                  "status":201,
                  "errors" : warning
                }  
              return jsonify(response_object)
    if db.session.query(Comments).filter(and_(Comments.id ==comment_id, Comments.author_id == user_id)).first() is None:
       response_object = {"status":201,"error":"this comment doesn't exist!"}
       return jsonify(response_object)
    #remove deleted comment from display
    deleted_= Comments.query.filter_by(id = comment_id).first()
    if deleted_.status == 1:
       response_object = {"status":201,"error":"this comment doesn't exist!"}
       return jsonify(response_object)

    #get comment data and replace status to 1 for deleted
    comment_deleted = db.session.query(Comments).filter(and_(Comments.author_id == user_id,Comments.id == comment_id)).first()
    comment_deleted.status = 1
    db.session.add(comment_deleted)
    db.session.commit()
    #fetch comment data
    response_object = {
        "status" : 200,
        "message": "comment deleted!",
        "comment_id": comment_id,
        "user_id" : user_id
    }
    return jsonify(response_object)





"""
------------------   FLAG POST --------------------

"""

@posts_bp.route('/api/v1/flag_post', methods=('GET', 'POST'))
@jwt_required
def flag ():
        """
        Creates a new post flag.
        """
        #deffinations
        current_time = time.localtime()
        saa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        data =request.json
        warning = []
        post_id = data.get('post_id')
        user_id = data.get('user_id')
        device_id =data.get('device_id')
        if not device_id:
          return jsonify('device_id missing')
        #update users device id
        username = get_jwt_identity()
        user_data = Users.query.filter_by(username = username).first()
        user_data.device_id = device_id
        db.session.commit()

        #check data
        if not user_id:
            warning.append("user_id missing")
            response_object = {
              "status": 201,
              "errors": warning
            }        
            return jsonify(response_object)
                       
        if not post_id:      
            warning.append(" post_id is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }        
            return jsoonify(response_object)

        #verify inputs
        if Users.query.filter_by(id = user_id).first() is None:          
                  warning.append(" user_id is invalid")                 
                  #return response
                  response_object = {
                      "status":201,
                      "errors" : warning
                    }  
                  return jsonify(response_object) 
                       
        if Posts.query.filter_by(id = post_id).first() is None:          
                  warning.append(" post_id is invalid")                 
                  #return response
                  response_object = {
                      "status":201,
                      "errors" : warning
                    }  
                  return jsonify(response_object)
                       
        #target a post to like by post_id and user_id
        exist= db.session.query(Posts).filter(and_(Posts.id ==post_id,Posts.status == 0)).first()

        #post missing
        if not exist:
            response_object = {
              "status": 201,
              "errors": "post doesnt exist! check inputs and try again"
            }
            return jsonify(response_object)
        

        #check if post is private or public
        if exist.status == 2:
                response_object = {
                "status": 201,
                "message": "post not available"
                }
                return jsonify(response_object)

        #check if post is already flaged by same user
        user =  Users.query.filter_by(id = user_id).first()
        flagged_post= db.session.query(flags_).filter(and_(flags_.user == user.id,flags_.post_id == post_id)).first()
        if flagged_post:
          
            response_object = {
                'status': 201,
                'message': "you have already flagged this post"
                }
            return jsonify(response_object)
       
                       
        #create new post flag if current user hasnt flaged the same post before
        if not flagged_post:
            flaged_post = flags_(
                user = user_id,
                post_id = post_id
            )

            db.session.add(flaged_post)
            db.session.commit()
           
         
            activity = 'flagged your post'
            timestamp = saa
            flagger =user.username
                       
            post = Posts.query.filter_by(id = post_id).first()          

            ptf = flags_.query.filter_by(post_id = post_id).first()
            data_url= url_for("posts.get_post", post_id = post_id)
            
            status_code=  0
            if status_code == 0:
                status_code = "Unread"
            elif status_code ==1:
                status_code = "read"

            #notify post owner and followers done in response_object
            message = ("{} {}").format(flagger,activity)
            
            #get liked post
            target_post = Posts.query.filter_by(id=post_id).first()
            #get user_id from post
            id_=target_post.author_id
            target_user =Users.query.filter_by(id=id_).first()
    
            #get device_id from user_id 
            dev_id = target_user.device_id
            registration_id= str(dev_id)

            post_id = target_post.id
            job_id=0
            story_id=0
            bid_id=0
            status_code="Unread"
            user_data_url=url_for("accounts.get_user",user_id=target_user.id)
            message = ("{} flagged your post").format(flagger)
            notifier(activity,timestamp,message,data_url, user_data_url, status_code,post_id,story_id,job_id,bid_id) 
            notification = {
                 "event_type": "Post Flag",
                 "body": message,
                 "title" : "iMarket",
                 "image":user.image_url,
                 "user_id":user_id,
                 "name": flagger
                 }
            pusher(notification,registration_id)
           
            print(message)
            flagged_= db.session.query(flags_).filter(and_(flags_.user == user.id,flags_.post_id == post_id)).first()
            return jsonify(flagged_.to_json())



"""
------------------   UNFLAG POST --------------------

"""

@posts_bp.route('/api/v1/unflag_post', methods=('GET', 'POST'))
@jwt_required
def delete():
        """
        Deletes post flag by flag id.
        """
        #deffinations
        current_time = time.localtime()
        saa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

        data = request.json
        flag_id = data.get("flag_id")
        user_id = data.get("user_id")
        flagged_post= flags_.query.filter_by(id = flag_id).first()
        warning=[]              
        device_id =data.get('device_id')
        if not device_id:
           return jsonify('device_id missing')
        #update users device id
        username = get_jwt_identity()
        user_data = Users.query.filter_by(username = username).first()
        user_data.device_id = device_id
        db.session.commit()
    
        #check data
        if not user_id:
            warning.append("user_id missing")
            response_object = {
              "status": 201,
              "errors": warning
            }        
            return jsonify(response_object)
                       
        if not flag_id:      
            warning.append(" flag_id is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }        
            return jsonify(response_object)

        #verify inputs
        if Users.query.filter_by(id = user_id).first() is None:          
                  warning.append(" user_id is invalid")                 
                  #return response
                  response_object = {
                      "status":201,
                      "errors" : warning
                    }  
                  return jsonify(response_object)
                       
        if flags_.query.filter_by(id = flag_id).first() is None:          
                  warning.append(" flag_id is invalid")                 
                  #return response
                  response_object = {
                      "status":201,
                      "errors" : warning
                    }  
                  return jsonify(response_object) 
        #target a flag to delete by flag_id and user
        exist = db.session.query(flags_).filter(flags_.id ==flag_id).first()

        #flag missing
        if not exist:
            response_object = {
              "status": 201,
              "errors": "post flag doesnt exist! check inputs and try again"
            }
            return jsonify(response_object)

        user = Users.query.filter_by(id =user_id).first()
        if exist or exist.user == session['current_user']:

            db.session.delete(exist)
            db.session.commit()
            post_url= url_for("posts.get_post",post_id=flagged_post.post_id)
            user_profile_url= url_for("accounts.get_user",user_id=user_id)
            response_object = {

                'status' : 200,
                'post_id': flagged_post.post_id,
                'post_url': post_url,
                'user_id': user_id,
                'user_profile_url': user_profile_url,
                'message' : 'The post has been unflagged.'
                 }

            activity = 'unflagged your post'
            timestamp = saa
            flagger =user.username

            post = Posts.query.filter_by(id = exist.post_id).first()

            data_url= url_for("posts.get_post", post_id = exist.post_id)
            user_data_url= url_for("accounts.get_user",user_id = user_id)
             
            status_code=  0
            if status_code == 0:
                status_code = "Unread"
            elif status_code ==1:
                status_code = "read"

            #get user from flagged post
            post_owne =Users.query.filter_by(id= post.author_id).first()
            post_owner= post_owne.username

            #get device_id from user_id 
            dev_id = post_owne.device_id
            registration_id= str(dev_id)
            
             
            message = ("{} Unflagged your post").format(user.username)
            notifier(activity,timestamp,message,data_url, user_data_url, status_code,post_id=flagged_post.post_id,story_id=0,job_id=0,bid_id=0)  
            notification = {
                 "event_type": "Post Unflag",
                 "body": message,
                 "title" : "iMarket",
                 "image":user.image_url,
                 "user_id":user_id,
                 "name": user.username
                 }
            pusher(notification,registration_id)
            return jsonify(response_object)

        elif  not exist or  exist.user != session['current_user']:
            response_object = {

                 'status' : 201,
                 'post_id':flagged_post.post_id,
                 'user_id': user_id,
                 'message' : 'you have not flagged this post yet'
            }
            return jsonify(response_object)
  



           
"""
------------------ POST_LIKERS --------------------
"""


@posts_bp.route('/api/v1/post_likers', methods=("GET","POST"))
@jwt_required
def post_likers():
    #get request_data 
    data=request.json
    post_id = data.get('post_id')
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
    if not post_id :      
        warning.append(" post_id is missing") 
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    if not user_id:
        warning.append(" post_id is missing") 
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
    if  Posts.query.filter_by(id =post_id).first() is None:
        warning.append(" invalid post_id") 
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    


    likers_list =[]

    Post = Posts.query.filter_by(id = post_id).first()
    post_liker = Likes.query.filter_by(id =post_id).all()
    x=[]
    y = []
    for post_like in  post_liker:
        x.append(post_like.liker
        )
    for item in x:
        user_ = Users.query.filter_by(id = x).first()
        if user_.username not in y:
            y.append(str(user_.username))

    if not y:
       y="0 likes for this post"
    response_object ={
                      "status": 200,
                      "liker" :  y,
                      "post_id" : post_id,
                         }
    return jsonify(response_object)





         
"""
------------------  DELETE POST  --------------------

"""
@posts_bp.route('/api/v1/delete_post', methods=('GET', 'POST'))
@jwt_required
def delete_post():

    #get request_data 
    data=request.json
    post_id = data.get('post_id')
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
    if not post_id :      
        warning.append(" post_id is missing") 
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

    #verify data validity    
    if Posts.query.filter_by(id = post_id).first() is None:
        warning.append(" post doesnt exist!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)
                           
    if Users.query.filter_by(id = user_id).first() is None:
        warning.append(" user_id doesnt exist!")
        response_object = {
          "status": 201,
          "errors": warning
          }
        return jsonify(response_object)

   
    #target a post to delete by post_id and user_id
    exist= db.session.query(Posts).filter(and_(Posts.id == post_id,Posts.author_id == user_id)).first()
    if not exist:
       response_object = {"status":200, "error":"post missing under that user_id and post_id"}                
       return jsonify(response_object)           

    #remove deleted postt from display

    if exist.status == 1:
       response_object = {"status":201,"error":"this post doesn't exist!"}
       return jsonify(response_object)



    #check where post_auther is the current_user
    user = Users.query.filter_by(id=user_id).first()
    if exist.author_id == user_id or exist.status !=1:
        post_target = exist
        post_target.status = 1
        #db.session.add(post_target)
        db.session.commit()
 
        response_object = {
            'status' : 200,
            'message' : 'The post has been deleted.',
            
                }
        return jsonify(response_object)


    if  exist.author_id != user.id:
        response_object = {

            'status' : 201,
            'message' : 'REQUEST DECLINED!, you can only delete a post you have authored!.'

                }

        return jsonify(response_object)






"""
------------------------ MY POSTS --------- ------
"""

@posts_bp.route('/api/v1/my_posts',methods=('GET','POST'))
@jwt_required
def my_posts():
    #definations
    my_posts = []
    current_user = get_jwt_identity()
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

    if  not  user_id:
        response_object = {
                              "error" : "Invalid user_id",
                               "status" : 201
                           }
        return jsonify(response_object)

    if  Users.query.filter_by(id = user_id).first() is None:
         response_object = {
                              "error" : "Invalid user_id",
                               "status" : 201
                           }      
         return jsonify(response_object)

    if Posts.query.filter_by(author_id =user_id).first() is None:
         response_object = {
                              "error" : "No posts for user_id {}". format(user_id),
                               "status" : 201
                           }      
         return jsonify(response_object)

    posts = db.session.query(Posts).filter(and_(Posts.author_id == user_id, Posts.status ==0)).all()
    u_id =db.session.query(Users).filter(and_(Users.username == current_user,Users.status ==0)).first()
    if not posts:
        return jsonify({"error":"no post found for user_id {}".format(user_id), "status":201, "user_id":user_id})

    return jsonify([post.to_json() for post in  posts])


"""
------------------------ TIMELINE POSTS ---------------
"""

@posts_bp.route('/api/v1/timeline_posts',methods=('GET','POST'))
@jwt_required
def timeline_posts():
    #definations
    timeline_posts = []
    current_user = get_jwt_identity()
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

    if  not  user_id:
        response_object = {
                              "error" : "user_id missing",
                               "status" : 201
                           }
        return jsonify(response_object)

    if  Users.query.filter_by(id = user_id).first() is None:
         response_object = {
                              "error" : "Invalid user_id",
                               "status" : 201
                           }      
         return jsonify(response_object)

    
    postz = db.session.query(Posts).filter(and_(Posts.status ==0)).all()
    u_id =db.session.query(Users).filter(and_(Users.username == current_user,Users.status ==0)).first()
    liked = Likes.query.filter_by(liker= user_id).all()
    shared = Share.query.filter_by(user = user_id).all()
    
   #filter posts by user activity.
    like_data = []
    share_data=[]
    for post in postz:
        if post.post_category == u_id.proffession:
           timeline_posts.append(post)
    for like in liked:
        if like.post_id:
           like_data.append(like.post_id)
    for id in like_data:
        post_ = Posts.query.filter_by(id =id).first()

        p= post_.post_category
        post_data = Posts.query.filter_by(post_category = p).all()
        if not post_data:
           pass
        if post_data:
           for post in post_data:
               timeline_posts.append(post)

    for share in shared:
        if share.post_id:
           share_data.append(share.post_id)
    for id in share_data:
        post_ = Posts.query.filter_by(id =id).first()

        p= post_.post_category
        post_data = Posts.query.filter_by(post_category = p).all()
        if not post_data:
           pass
        if post_data:
           for post in post_data:
             timeline_posts.append(post)


    return   jsonify([post.to_json() for post in timeline_posts])    #jsonify({"post_url" :([url_for("posts.get_post",post_id=post.id) for post in timeline_posts]), "status":200})



"""
------------------   HIDE POST --------------------

"""
@posts_bp.route('/api/v1/hide_post', methods=('GET', 'POST'))        
@jwt_required
def hide_post():
    #deffinations
    data= request.json
    user_id = data.get('user_id')
    post_id = data.get('post_id')
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

    if not post_id:      
        warning.append(" post_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    hidden_post = db.session.query(Posts).filter(and_(Posts.status == 0, Posts.id == post_id)).first()
    if not hidden_post:
       return jsonify({"status": 201, "message":"no active post identified by post_id:  {} ".format(post_id)})
    elif  hidden_post:
       hidden_post.status = 3
       if hidden_post.author_id != user_id:
         return jsonify({"status" : 201, "message": "Permission denied! edith wht you've authored."})
       db.session.commit()
       return jsonify({"status" : 200, "message":"post data is now hidden", "post_data" : hidden_post.to_json()})
 

"""
------------------  UNHIDE POST --------------------

"""       


@posts_bp.route('/api/v1/unhide_post', methods=('GET', 'POST'))        
@jwt_required
def unhide_post():
    #deffinations
    data= request.json
    user_id = data.get('user_id')
    post_id = data.get('post_id')
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

    if not post_id:      
        warning.append(" post_id is missing")
        response_object = {
          "status": 201,
          "errors": warning
        }        
        return jsonify(response_object)
    hidden_post = db.session.query(Posts).filter(and_(Posts.status == 3, Posts.id == post_id)).first()
    if not hidden_post:
       return jsonify({"status": 201, "message":"no hidden post identified by post_id: {} ".format(post_id)})
    elif  hidden_post:
       hidden_post.status = 0
       if hidden_post.author_id != user_id:
         return jsonify({"status" : 201, "message": "Permission denied! edit what you've authored."})
       db.session.commit()
       return jsonify({"status" : 200, "message":"post data is now visible", "post_data" : hidden_post.to_json()})

