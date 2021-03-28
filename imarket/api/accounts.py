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

accounts_bp = Blueprint('accounts', __name__)
conn = create_engine('mysql+pymysql://root:sword@localhost/imarket_deploy')



"""
------------------  PUSH NOTIFICATION --------------------

""" 
@jwt_required
def pusher(notification,registration_id):
    current_usa = get_jwt_identity()

    from pyfcm import FCMNotification

    reg_id = jsonify(str(registration_id))

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
------------------  RECCOMEND --------------------

""" 

@accounts_bp.route('/api/v1/recommend',  endpoint='recommender',methods=( 'GET','POST'))
def recommender():
    """
    Accepts a list of commma separated contacts and
    returns that match with contacts in database
    
    """
    #get request_data with a list of contacts
    data = request.json
    raw_no = data.get('contact_list')
    recomend = []
    cont = []
    all =[]    
    #check for empty input
    if not raw_no:
        response_object = {
        "status" : 1,
        "error" : "contacts list is missing"
        }
        return jsonify(response_object)
    #ensure the input is a list
    if type(raw_no) is not list:

        response_object = {
        "status" : 1,
        "error" : "this Api requies a list of contacts eg. "["","",""]
        }
        return jsonify(response_object)

    #get all user_data from registered users
    contact = conn.execute("select * from users")

    #compare submited contacts and the registered users contacts 
    for row in contact:
        cont.append(row.contact)
        
        #get matching contacts into found
        found = list(set(raw_no) & set(cont))
    
        #match all the found contacts with user data from user regestry
        for item in found:

            user = db.session.query(Users).filter(and_(Users.contact == item, Users.status ==0)).all()
            
            x=([u.to_intro() for u in user])
            if x not in all:
                all.append(x)

    if not all:
        #pass status and message
        response_object = {
           "status": 201,
           "message": "Recomendations not found!"           
            }
        return jsonify(response_object)

    else:
         return jsonify(all)




"""
------------------  REGISTER --------------------

""" 

@accounts_bp.route('/api/v1/register', methods=("GET","POST"))
def register():
    #variable diclaration and definations    
    data= request.json
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    contact = data.get('contact')
    proffession = data.get("proffession"),
    bio = data.get("bio"),
    interests = data.get('interests'),
    status = 0,
    admin = 1 ,
    last_seen =sasa
    registered_on =sasa
    warning = []
  
   # check for data presence   
    if not name:      
        warning.append("name is missing")  
        response_object = {
            "status" : 201,
            "error": warning
            }
        return response_object
    if not username:      
        warning.append(" username is missing")  
        response_object = {
            "status" : 201,
            "error": warning
            }
        return response_object
    
    if not email:
          warning.append(" email is missing")
          response_object = {
            "status" : 201,
            "error": warning
            }
          return response_object
    regex= '^.+@[^\.].*\.[a-z]{2,}$'      
    if  (re.search(regex,email)):
        email=email
    else:  
        response_object={"status":1,"error":"invalidd email"}
        return  response_object
    if not contact:
        warning.append(" contact is missing")
        response_object = {
            "status" : 0,
            "error": warning
            }
        return response_object
    
    #check contact length
    if len(contact) < 10 or  len(contact) >13:
        warning.append(" contact is invalid! min =10, max = 13")
        response_object = {
            "status" : 201,
            "error": warning
            }
        return response_object    

    if not all(bio):      
        warning.append(" bio is missing")  
        response_object = {
            "status" : 201,
            "error": warning
            }
        return  jsonify(response_object)
    if not all(proffession):      
        warning.append(" proffession is missing")  
        response_object = {
            "status" : 201,
            "error": warning
            }
        return  jsonify(response_object)

    if not all(interests):      
        warning.append(" interest is missing")  
        response_object = {
            "status" : 201,
            "error": warning
            }
        return  jsonify(response_object)

    #check email for correctness,
                  
    
    # duplicate value error handling 

    _user = Users.query.filter_by(status = 0).all()
    existing_usernames = []
    existing_emails = []
    existing_contacts = []
        

    for _user_ in _user:
        existing_usernames.append(_user_.username)
        existing_emails.append(_user_.email)
        existing_contacts.append(_user_.contact)   
  
        if  _user_.email ==email and _user_.contact == contact and _user_.username ==username:
                response_object = {
                    "status": 201,
                    "message" :"This user_data exists. login.",
                    }
                return  jsonify(response_object)

        #response creation  
        if  username in existing_usernames :          
                warning.append(" username : {} already exists".format(username))
                #return response
                response_object = {
                    "status":201,
                    "errors" : warning
                }  
                return  jsonify(response_object) 
         
              
        if  email in existing_emails :           
                warning.append(" email : {} already exists!".format(email))
                #return response
                response_object = {
                    "status":201,
                    "errors" : warning
                }  
                return  jsonify(response_object) 
         
          
        if  contact in existing_contacts :           
                warning.append(" contact : {} already exists!".format(contact))          
                #return response
                response_object = {
                    "status":201,
                    "errors" : warning
                }  
                return  jsonify(response_object)      

    #user creation
    new_user = Users(
        username = username,
        name =name,
        email = email,
        password_hash = password,
        contact = contact,
        proffession = proffession,
        bio = bio,
        interests = interests,
        status = 0,
        admin = 1 ,
        last_seen = last_seen,
        registered_on = registered_on            
    )   

    empty_users = Users.query.filter_by(status = 0).count()
    if empty_users == 0:
        db.session.add(new_user)
        db.session.commit()
       
    # check new_user existance
    for _user_ in _user:
        if  _user_.email ==email and _user_.contact == contact and _user_.username ==username:
                response_object = {
                    "status": 201,
                    "message" :"This user_data exists",
                    }
                return jsonify(response_object)
        elif  _user_ != new_user:
        #save new user
               
            db.session.add(new_user)
            db.session.commit()

            user_data = Users.query.filter_by(contact = contact).first()
            #return  user_data.to_json()  
    created_user = Users.query.filter_by(contact = contact).one()
    f = Follows(
            follower_id=created_user.id,
            followed_id=created_user.id,
            timestamp =sasa
            )
    db.session.add(f)
    db.session.commit()
 
    if created_user.status == 0 :
        # create photo directory

        dest = created_user.id
        UPLOAD_ = '/root/Imarket/imarket/static/images/profile' #/root/imarket_deploy/api/static/images/profile
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
            os.chdir(BASE_DIR)

        # create post photo directory
        UPLOAD_ = '/root/Imarket/imarket/static/images/posts'  #'/root/imarket_deploy/api/static/images/posts'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
            os.chdir(BASE_DIR)
        
        # create jobs photo directory
        UPLOAD_ = '/root/Imarket/imarket/static/images/jobs' #'/root/imarket_macro/api/static/images/jobs'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
            os.chdir(BASE_DIR)

        # create Story photo directory
        UPLOAD_ = '/root/Imarket/imarket/static/images/story' #'/root/imarket_macro/api/static/images/story'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
            os.chdir(BASE_DIR)


        #return user_data
        return created_user.to_json()




"""
------------------  LOGIN --------------------

""" 


@accounts_bp.route('/api/v1/login', methods=('GET', 'POST'))
def login():
        #variable diclaration and definations    
        current_time = time.localtime()
        sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        data = request.json
        email = data.get("email")
        password = data.get("password")
        device_id = data.get("device_id")
        warning = []

        # check for data presence           
        if not password:
            warning.append(" password is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
        
        if Users.query.filter_by(password_hash =password).first() is None:
            warning.append(" Wrong password")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object

        if not email:
            warning.append(" email is missing")
            response_object = {
              "status":201,
              "errors": warning
            }            
            return response_object

        if Users.query.filter_by(email =email).first() is None:
            warning.append(" Wrong email address")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
           
        if not device_id:
            warning.append(" device_id is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
        
        #check email for correctness,
                  
        regex = '^.+@[^\.].*\.[a-z]{2,}$'
             
        if (re.search(regex,data['email'])):
            warning.append(" email ( {}) is invalid".format(email))
        else:
            response_object = {
              "status": 201,
              "errors": warning
            }
            
            return response_object
        if (re.search(regex,data['email'])):    
            user = Users.query.filter_by(email=email).first()              
        password_hash = user.password_hash        
        if password !=password_hash:
            return jsonify("wrong credentials","401")
        if password == password_hash :
            current_time = time.localtime()
            sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
            user = Users.query.filter_by(email=email).first()
            if user.status !=1:
                login_user(user)  
             
            
            session['logged_in'] = True
            session["current_user"] = user.username
            targeted_user = user
            targeted_user.last_seen = sasa
            db.session.add(targeted_user)
            db.session.commit()
            username =user.username
            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=username,expires_delta=expires) 
            return jsonify(user_id=user.id,access_token=access_token), 200






"""
------------------  UPDATE USER --------------------

"""


@accounts_bp.route('/api/v1/update_user', methods=('GET', 'PUT'))
@jwt_required
def update_user():
      
        #variable diclaration and definations
        data= request.json
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        contact = data.get('contact')
        proffession = data.get("proffession"),
        bio = data.get("bio"),
        interests = data.get('interests'),
        admin = 1 ,
        last_seen =sasa
        registered_on =sasa
        warning = []
        name =data.get("name")
        device_id = data.get("device_id")
        if not device_id:
           return jsonify('missing device_id')
       
        x = get_jwt_identity()
            
         
       


        # check for data presence
        if not all(username):      
            warning.append(" username is missing") 
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
           
        if not all(email):
            warning.append(" email is missing")
            response_object = {
              "status":201,
              "errors": warning
            }            
            return response_object

        if not contact:
            warning.append(" contact is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
        
        #check contact length
        if len(contact) <10 and len(contact) >13:
            warning.append(" contact is invalid! min =10, max = 13")
            response_object = {
                "status" :201,
                "error": warning
                }
            return response_object
        
        if not all(proffession):
            warning.append(" proffession is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object

        if not interests:
            warning.append(" interests is missing")
            response_object = {
              "status":201,
              "errors": warning
            }            
            return response_object

        if not all(bio):
            warning.append(" bio is missing")
            response_object = {
              "status":201,
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

        if Users.query.filter_by(id =user_id).first() is None:
            warning.append("user_id isnt registered with us!")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object
           
        #check email for correctness,
                      
        regex = '^.+@[^\.].*\.[a-z]{2,}$'
             
        if (re.search(regex,data['email'])):
           email = email
        else:
            response_object = {
              "status": 201,
              "errors": "invalid email"
            }            
            return response_object

        
        #check contact length
        if len(contact) < 10 or  len(contact) >13:
            warning.append(" contact is invalid! min =10, max = 13")
            response_object = {
              "status" :201,
               "error": warning
              }
            return response_object    

        # duplicate value error handling 

        _user = Users.query.filter_by(status = 0).all()
        existing_usernames = []
        existing_emails = []
        existing_contacts = []
        original_email =[]  
        original_contact =[]
        original_username =[]    

        for _user_ in _user:
            if _user_.id != user_id:
                existing_usernames.append(_user_.username)
                existing_emails.append(_user_.email)
                existing_contacts.append(_user_.contact)   
               

        user_data = Users.query.filter_by(id =user_id).first() 
        if user_data.id == user_id:
                original_email =user_data.email 
                original_username =user_data.username
                original_contact =user_data.contact

        #preserve unchanged fileds
        if  username == user_data.username :          
                warning.append(" username : {} already exists".format(username))                
        if username != user_data.username:
            user_data.username = username

        if  email == user_data.email:           
                warning.append(" email : {} already exists!".format(email))
        if email != user_data.email:
            user_data.email = email 
            
        if  contact in user_data.contact :           
                warning.append(" contact : {} already exists!".format(contact))
        if contact != user_data.contact:
            user_data.contact = contact
        if name in  user_data.name:
            warning.append("same name")         
        if name !=user_data.contact:
           user_data.name =name
        if user_data.username != x:
           warning.append("Error: you are not allowed to edit this data")
           return jsonify(warning)
        user_data.user_id=user_id ,
        user_data.last_seen = sasa,
        user_data.proffession = proffession,
        user_data.bio = bio,
        user_data.interests = interests,
        user_data.device_id = device_id,
        user_data.name = name,  
        # update user_data        
        try:
            db.session.commit()
            
        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
            print(e) 
        if user_data.username == x:
            #respond        
            return user_data.to_json()

        if user_data.username != x:
           warning= {"Error": "you are not allowed to edit this data", "status":201}
           return jsonify(warning)




"""
------------------  PROFILE PHOTO --------------------

""" 


@accounts_bp.route('/api/v1/profile_pic',  methods=('GET', 'POST'))
@jwt_required
def upload_prof_pic():
    """
    uploads profile picture to session['current_user'].
    
    """
    #get current_user
    current_user = get_jwt_identity()
    user_data = Users.query.filter_by(username =current_user).first()
    
    if request.method == 'POST':
        id = user_data.id
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('static/images/profile/'+str(user_data.id)+"/", f_name))
        user_data.image_url = ('static/images/profile/'+str(user_data.id)+"/"+f_name)
        db.session.commit()
        activity = "updated profile picture"
        timestamp = sasa
        data_url= url_for('accounts.get_user' ,id = id),
        user_data_url=  id,
        status_code=  0

        if status_code == 0:
            status_code = "Unread"
        elif status_code ==1:
            status_code = "read"

        #notify post owner and followers done in response_object
        message = ("{} updated profile picture").format(user_data.username)
        print(message)
        notifier(activity,timestamp,message,data_url, user_data_url, status_code)
        #prepare and push notification 
        notification = {
           "event_type": "profile_picture_update",
           "body" :message,
           "title" : "iMarket",
           "image":user_data.image_url,
           "link":user_data.image_url,
           "user_id":user_data.id,
           "name": user_data.username
           }
        
        #pusher(notification)
        #respond
        response_object = {
           'status' : 200,
           'user_id' : user_data.id,
           'timestamp': timestamp,
           'message' : 'profile picture updated',
           'image_url' : user_data.image_url,
           'user_url' : url_for('accounts.get_user', id = id),
            }
        
    return jsonify(response_object)





"""
------------------  FOLLOW --------------------

"""  


@accounts_bp.route('/api/v1/follow_user', methods=('GET', 'POST'))

def follow_user():
        #deffinations
        timestamp = sasa  
        data = request.json
        to_user = data.get("followed_id")
        from_user = data.get("user_id")
        device_id = data.get("device_id")
        warning = []
        existing =[]

        #check data
        if not device_id:
            response_object = {
            "status": 201,
            "error": "device_id missing"
            }
            return jsonify(response_object)
        if not to_user:
            response_object = {
            "status": 201,
            "error": "followed user_id missing"
            }
            return  jsonify(response_object)
        
        if not from_user:
            response_object = {
            "status": 201,
            "error": "following user_id missing"
            }
            return  jsonify(response_object)

        #verify data
        if Users.query.filter_by(id =to_user).first() is None:
            response_object = {
            "status":201,
            "error": " user_id invalid!"
            }
            return  jsonify(response_object)

        if Users.query.filter_by(id =from_user).first() is None:
            response_object = {
            "status": 201,
            "error": " follower user_id invalid!"
            }
            return  jsonify(response_object)
        ###if Follows.query.filter_by(followed_id =to_user).first() is None:
        ### return jsonify("follow_id invalid")

        #initialize follow
        userz=Users.query.filter_by(id = from_user).first()
        followed_users = Follows.query.filter_by(followed_id = to_user).all()

        for user in followed_users:
            if user.follower_id == from_user:
                existing.append(from_user)

        #tacle duplicates
        rv=conn.execute('SELECT * FROM follow_ups WHERE followed_id=%s and follower_id=%s'%(to_user,from_user)).fetchone()
        if rv:
            followed_user = Users.query.filter_by(id =to_user).first()
            response_object = {
            "status": 201,
            "error": " you are already following {}!".format(followed_user.name)
            }
            return  jsonify(response_object)


        #create follow
        if from_user not in existing:                                       
                f = Follows(
                    follower_id=from_user,
                    followed_id=to_user,
                    timestamp =sasa
                    )
                db.session.add(f)
                db.session.commit()
        #capture and delete self follow:
        follow_data= db.session.query(Follows).filter(and_(Follows.follower_id ==from_user ,Follows.followed_id ==from_user)).first()
        if follow_data:
            db.session.delete(follow_data)
            db.session.commit()


        #update users device id
        user_data = Users.query.filter_by(id = from_user).first()
        user_data.device_id = device_id
        db.session.commit()

        #prepare notification   
        activity = "follwed"
        timestamp = sasa
        data_url= from_user,
        user_data_url= url_for('accounts.get_user' ,id = from_user),
        status_code=  0
        if status_code == 0:
            status_code = "Unread"
        elif status_code ==1:
            status_code = "read"
       #notify post owner and followers done in response_object
        to_=Users.query.filter_by(id= to_user).first()
        to_usr =to_.device_id
        registration_id = str(to_usr)
        message = message = ("{} is now following you").format(userz.username)
        notifier(activity,timestamp,message,data_url, user_data_url, status_code) 
        notification = {
           "event_type": "follow",
           "body": message,
           "title" : "iMarket",
           "image":user_data.image_url,
           "user_id":user_data.id,
           "name": user_data.username
           }

      #  pusher(notification,registration_id)
      #  print(registration_id)
        #get this follow
        follow_ =Follows.query.filter_by(followed_id = to_user).all()
        for f_ in follow_:
            if f_.follower_id == from_user:
                created_follow = f_
        #respond
        return f_.to_json()


"""
------------------  UNFOLLOW  --------------------

""" 


@accounts_bp.route('/api/v1/unfollow', methods=('GET', 'POST'))

def unfollow():

        #deffinations
        data = request.json
        followed_id = data.get('followed_id')
        unfollower = data.get('user_id')

        warning = []
        existing =[]

        #check data
        if not followed_id:
            response_object = {
            "status": 201,
            "error": "followed_id is missing"
            }
            return jsonify(response_object)
        
        if not unfollower:
            response_object = {
            "status": 201,
            "error": "user_id is missing"
            }
            return jsonify(response_object)

        #verify data
        if Users.query.filter_by(id =followed_id).first() is None:
            response_object = {
            "status": 201,
            "error": " followed_id invalid!"
            }
            return jsonify(response_object)

        if Users.query.filter_by(id =unfollower).first() is None:
            response_object = {
            "status": 201,
            "error": "user_id invalid!"
            }
            return jsonify(response_object)

        #get specific follow object and delete it
        rv=conn.execute('DELETE FROM follow_ups WHERE followed_id=%s and follower_id=%s'%(followed_id,unfollower))

        #fetch unfollowed user name  
        user = Users.query.filter_by(id =followed_id).first()
        unfollo_= Users.query.filter_by(id = unfollower).first()
        #prepare notification   
        activity = "unfollwed"
        timestamp = sasa
        data_url=unfollower,
        user_data_url= url_for('accounts.get_user' ,id =unfollower),
        status_code=  0
        if status_code == 0:
            status_code = "Unread"
        elif status_code ==1:
            status_code = "read"



        #notify post owner and followers done in response_object
        to_=Users.query.filter_by(id= followed_id).first()
        to_usr =to_.device_id
        registration_id = str(to_usr)
        message = message = ("{} has unfollowed you").format(unfollo_.username)
        notifier(activity,timestamp,message,data_url, user_data_url, status_code) 
        notification = {
           "event_type": "follow",
           "body": message,
           "title" : "iMarket",
           "image":unfollo_.image_url,
           "user_id":unfollo_.id,
           "name": unfollo_.username
           }
       #pusher(notification,registration_id)



        #respond
        response_object ={
        "followed_id":followed_id,
        "unfollower_id":unfollower,
        "status": 200,
        "message": "you have unfollowed {}".format(user.name)
        }
        return jsonify(response_object)



"""
--------------------------- GET FOLLOWERS  ------------------

"""


@accounts_bp.route('/api/v1/get_followers',methods=('GET','POST'))
@jwt_required
def get_followers():
    data = request.json
    user_id = data.get('user_id')
    
    if Users.query.filter_by(id = user_id).first() is None:
        return jsonify('invalid user_id')
    if  not user_id :
        return jsonify('user_id  missing')
    followers = Follows.query.filter_by(followed_id = user_id).all()
    if Follows.query.filter_by(followed_id = user_id).first() is None:
        return jsonify('user_id has no followers yet!')
    r =[]
    for  follower in followers:
       f_id = follower.follower_id
       foll_id = follower.followed_id
       username = get_jwt_identity()
       user = Users.query.filter_by(id = f_id).first() 
       followed_data = Users.query.filter_by(id = foll_id).first()
       follower_= user.username
       if  f_id != user_id:
            f_url =  url_for('accounts.get_user', user_id =follower.follower_id)
            flwd_url =  url_for('accounts.get_user', user_id =follower.followed_id)
            res ={"status" : 200, "follower_id":f_id, "follower_profile":f_url,"followed_user_image":followed_data.image_url,
           "follower_user_image":user.image_url, "followed_id":user_id, "followed_user_profile":flwd_url}

            r.append(res)
       if  not r:
          report = {"status": 200,
                    "followers": 0
                    }
          return report

    return jsonify(r)





"""
---------------------------- GET FOLLOWING ----------------------
"""



@accounts_bp.route('/api/v1/get_following',methods =("GET","POST") )
@jwt_required
def get_following():
    flwn = []
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
      return jsonify("missing user_id")
    if Users.query.filter_by(id = user_id).first() is None:
      return jsonify("invalid user_id")
    if Follows.query.filter_by(follower_id = user_id).first() is None:
      return jsonify("user_id hasn't followed anyone yet")
    following =Follows.query.filter_by(follower_id = user_id).all()
    for f in following:
     followed = f.followed_id
     if followed != user_id:
         followed_data = Users.query.filter_by(id = followed).first()
         followed_prof = url_for('accounts.get_user', user_id = followed)
     res = {"status":200, "following_user_url": url_for('accounts.get_user', user_id = user_id), 
           "followed_id":followed, "followed_user_url":followed_prof, 
           "followed_user_image":followed_data.image_url,
           "following_user_image":user_data.image_url,
           "follower_id" :user_id
            }
     flwn.append(res)
    return jsonify(flwn)




"""

------------------------------ ALL  USER DATA --------------------

"""


@accounts_bp.route("/api/v1/all_users", methods =("GET","POST"))
def all_users():
    user_data=[]
    users = Users.query.filter_by(status = 0).all()
    for user in users:
       followers = Follows.query.filter_by(followed_id = user.id).count()
       following = Follows.query.filter_by(follower_id = user.id).count()
       
       response = {
                    "status": 200,
                    "name" : user.name,
                    "userid": user.id,
                    "interests": user.interests,
                    "followers": followers,
                    "following": following,
                    "profile_image" :user.image_url,
                    "profile_url" : url_for('accounts.get_user',user_id =user.id)
                  } 
       user_data.append(response)
    return jsonify(user_data)




    
"""
------------------  GET USER --------------------

"""    

@accounts_bp.route('/api/v1/get_user', methods=('GET', 'POST'))
@jwt_required
def get_user():
    
    #definations 
    data = request.json
    user_id = data.get('user_id')
    existing_user_ids = []
    warning = []
    _user = Users.query.filter_by(status = 0).all()

    #check for empty values
    
    if not user_id:
        warning.append("user_id : user_id is missing!")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return response_object
    
    #collect existing user_id(s)
    for _user_ in _user:
        existing_user_ids.append(_user_.id)    
        
    #respond if user_id is non existant
    if Users.query.filter_by(id=user_id).first() is None: 
        warning.append("user_id : {} doesn't exist !".format(user_id))
        response_object = {
        "status": 201,
        "errors": warning
        }
        return response_object
    
    #get user_data    
    targeted_user = Users.query.filter_by(id = user_id).first()
    return targeted_user.to_json()




"""
------------------ PROTOFOLIO   --------------------

"""   

@accounts_bp.route('/api/v1/protofolio', methods=('GET', 'POST'))
@jwt_required
def protofolio():
    #definations 
    data = request.json
    
    user_id = data.get("user_id")
    warning = []

    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    #check user_id:
    _user = Users.query.filter_by(status = 0).all()
    if not user_id:
        warning.append("user_id : user_id is missing!")
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)

    #check if user exists
    if Users.query.filter_by(id= user_id).first() is None: 
        warning.append("user_id : {} doesn't exist !".format(user_id))
        response_object = {
        "status": 201,
        "errors": warning
        }
        return jsonify(response_object)

    user = Users.query.filter_by(id =user_id).first()

    my_jobs = db.session.query(Jobs).filter(and_(Jobs.author_id ==user_id,Jobs.status ==0)).count()
    if not my_jobs :
        my_jobs = 0

    my_bids = db.session.query(job_bid).filter(and_(job_bid.author_id ==user_id, job_bid.status == 0)).count()
    if not my_bids :
        my_bids = 0
    
    user_posts  = Posts.query.filter_by(author_id=user.id).count(),
    if not user_posts :
       user_posts = 0

    response_object = {            
            'user' : user.username,
            'Bio': user.bio,
            'my_jobs': my_jobs,
            'my_bids': my_bids,
            'followers' :user.followers.count(),
            'following' : user.followed.count(),
            'user_posts' : user_posts,
            'proffession':  user.proffession,
            'user_image_url': user.image_url,
            'status': 200           
            }
    return jsonify(response_object)





"""
------------------  DEACTIVATE USER --------------------

"""  

@accounts_bp.route('/api/v1/delete_users', methods=( 'GET','POST'))
@jwt_required
def delete_account():
    """
      change the status code of the account to 1 to avoid future selections
      the account is deemed inactive

    """
    #deffinations
    data = request.json
    user_id = data.get("user_id")

    #check data_input and validate existance
    if not user_id:
            warning.append(" user_id is missing")
            response_object = {
              "status": 201,
              "errors": warning
            }            
            return response_object

    if Users.query.filter_by(id =user_id).first() is None:
        warning.append("user_id isnt registered with us!")
        response_object = {
          "status": 201,
          "errors": warning
        }            
        return response_object
           
    #get user account 
    to_delete = Users.query.filter_by(id =user_id).first()

    #check permission to delete
    allowed_user = session['current_user']
    if to_delete.username == allowed_user:
        #change account status to 1 for deleted accounts
        to_delete.status =1
        db.session.commit()
        #respond
        response_object = {
          "status": 201,
          "errors": "user account deactivated . Kindly request an activation or sign_up afresh"
        }            
        return response_object

    #reject attempt if not account owner
    elif to_delete.username != allowed_user:
        #respond
        response_object = {
          "status": 201,
          "errors": "user account deactivated Failed! you can only deactivate your personal account!"
        }            
        return response_object




"""
------------------   CREATE INTEREST --------------------

""" 

@accounts_bp.route('/api/v1/create_interests',  methods=('GET', 'POST'))
@jwt_required
def create_category():
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

    if not user_id:
       r = {"status": 201, "error": "user_id missing!"}
       return jsonify(r)
    if Users.query.filter_by(id = user_id).first() is None :
      r =  {"status":201,"error":"invalid user_id!"}
      return jsonify(r)
    
    target = Users.query.filter_by(id= user_id).first()
   
    interest = data.get('interest')
    interestz = Interests.query.filter_by(interest_ = data.get("interest")).first()
    if not interestz:
        category = Interests(
               user = user_id,
               interest_ = interest
               )
        
        db.session.add(category)
        db.session.commit()
    interestx =db.session.query(Interests).filter(and_(Interests.interest_ == interest, Interests.user == user_id)).first()
    response_object = {
           "status": 200,
           "message" : "interest created!",
           "interest_id": interestx.id,
           "interest" : interestx.interest_,
           "user_id" : user_id,
           
        }
    return jsonify(response_object)



"""
------------------  EDIT INTEREST --------------------

""" 

@accounts_bp.route('/api/v1/edit_interest',  methods=('GET', 'PUT'))
@jwt_required
def update_category():
    data= request.json
    int_id = data.get('interest_id')
    cate = data.get('interest')
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    if not int_id:
     return jsonify("interest id missing")

    if Interests.query.filter_by(id =int_id).first() is None:
     return jsonify("invalid interest_id")
    category = Interests.query.filter_by(id =int_id).first()

    category.interest_ = cate
    db.session.add(category)
    db.session.commit()
    response_object = {
     "status" : 200,
     "interest_id" : int_id,
     "message" : "interest updated!",
     "interest": cate,

    }
    return jsonify(response_object)


"""
------------------   GET INTEREST --------------------

""" 
@accounts_bp.route('/api/v1/get_interests',  methods=('GET', 'POST'))
@jwt_required
def get_interests():
    inter =[]
  
    interests = db.session.query(Interests).all()
    
    return jsonify([interest.to_json() for interest in interests])



"""
------------------   GET PROFFESSIONS --------------------

""" 
@accounts_bp.route('/api/v1/get_proffessions',  methods=('GET', 'POST'))
@jwt_required
def get_proffessions():
   # definations#
   data = request.json
   users_ =Users.query.filter_by(status = 0).all()
   proffessions =[]
   device_id =data.get('device_id')
   if not device_id:
       return jsonify('device_id missing')
   #update users device id
   username = get_jwt_identity()
   user_data = Users.query.filter_by(username = username).first()
   user_data.device_id = device_id
   db.session.commit()

   count = 0
   data = []
   #recursively collect proffessions
   for row in users_:
       pro=row.proffession
              
       x =row.proffession
       #build a list of proffessions
       if x not in proffessions:
            proffessions.append(x)
       
       #get proffetionals count
       y=db.session.query(Users).filter(Users.proffession == pro).count()
       #compose response
       pro =("{}  ({})".format(x,y))
       #building data list with total for proffessional in every profession
       if pro not in  data:
           data.append(pro)
 
       all_pros =  Users.query.filter_by(status = 0).count()
   return jsonify("total proffessionals "+str(all_pros),data)


######################################################## search ##############################################################
"""
preping database for keyword search
alter table jobs add fulltext(job_body,job_post_category)
alter table posts add fulltext(body,post_category)
alter table story add fulltext(body,story_category)


"""

@accounts_bp.route('/api/v1/search',  methods=('GET', 'POST'))
@jwt_required
def search():
    data= request.json

    posts =[]
    job= []
    story = []

    keyword = "'" + data.get("keyword") +"'"
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    if not keyword:
      resopne_object = {"error":"search keword missing!", "status": 1}
    match = conn.execute( "select  * from posts where  match(body,post_category) against(%s)"%keyword).fetchall()
    if not match:
        posts.append("no post matched that keyword")
        

    for row in match:
        posts.append(url_for("posts.get_post", post_id =row.id))
        if not posts:
           posts.append("no post matching that keyword")

     
    matched = conn.execute( "select  * from jobs where  match(job_body,job_post_category) against(%s)"%keyword).fetchall()
    if not match:
        job.append("no post matched that keyword")
    for row in matched:
        job.append(url_for("jobs.get_job", job_id =row.id))
        if not job: 
           job.append("no job post matched that keyword")
      
    
    match_ = conn.execute( "select  * from story where  match(body,story_category) against(%s)"%keyword).fetchall()
    if not match:
        posts.append("no post matched that keyword")

    for row in match_:
        story.append(url_for("story.get_story", story_id =row.id ))
        if not story:
            story.append("no story matched that keyword")

 
    response_object = {
             "status": 200,

             "job_data_url" : str(job),
             "post_data_url":str(posts),
             "story_data_url" : str(story)
    }

    return jsonify(response_object)


@accounts_bp.route("/api/v1/timeline", methods=('GET','POST'))
@jwt_required
def timeline():
   data = request.json
   user_id = data.get("user_id")
   interest_post = []
   postz =[]
   
   if not user_id:
      response_object ={"status": 201,"error" : "user_id missing"}
      return response_object
   if Users.query.filter_by(id =user_id).first() is None:
      response_object ={"status" : 201, "error" :" invalid user_id!"}
      return  jsonify(response_object)
   
   user_interest = Interests.query.filter_by(user = user_id).first()
   if user_interest:
      
      post_data =db.session.query(Posts).filter(and_ (Posts.post_category == user_interest.interest_, Posts.status ==0)).all()
      posts = db.session.query(Posts).filter(Posts.status ==0).all()
      if post_data:
         return jsonify([p.to_json() for p in post_data])
         
      if not post_data:
          return jsonify([p.to_json() for p in  posts])
   if not user_interest:
      posts = Posts.query.filter_by(status = 0 ).all()
      if posts:
         return jsonify([post.to_json() for post in posts])
            




"""
------------------   GET NOTIFICATIONS --------------------

""" 
@accounts_bp.route('/api/v1/all_notifications',  methods=('GET', 'POST'))
@jwt_required
def all_notifications():
    data = request.json
    
    user_id = data.get("user_id")
    if not user_id:
       r = {"status": 201, "error": "user_id missing!"}
       return jsonify(r)

    notifications = db.session.query(Notification).all()
    if not notifications:
       return jsonify({"status":201, "message" : "no notifications found!"})
    return jsonify([notification.to_json() for notification in notifications])



"""
------------------   GET NOTIFICATIONS --------------------

""" 
@accounts_bp.route('/api/v1/my_notifications',  methods=('GET', 'POST'))
@jwt_required
def my_notifications():
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
       r = {"status": 201, "error": "user_id missing!"}
       return jsonify(r)
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    notifications = db.session.query(Notification).filter(Notification.author == user_id).all() 
    if not notifications:
       return jsonify({"status":201, "message" : "no notifications found! for user_id: {}".format(user_id)})
    return jsonify([notification.to_json() for notification in notifications])

"""
------------------   GET NOTIFICATIONS --------------------

""" 
@accounts_bp.route('/api/v1/single_notification',  methods=('GET', 'POST'))
@jwt_required
def single_notifications():
    data = request.json
    notification_id = data.get("notification_id")
    user_id = data.get("user_id")
    device_id =data.get('device_id')
    if not device_id:
       return jsonify('device_id missing')
    #update users device id
    username = get_jwt_identity()
    user_data = Users.query.filter_by(username = username).first()
    user_data.device_id = device_id
    db.session.commit()

    if  not notification_id:
       return jsonify({"status" : 201, "message" : "no notification_id supplied"})

    if not user_id:
       r = {"status": 201, "error": "user_id missing!"}
       return jsonify(r)

    notification = db.session.query(Notification).filter(Notification.id == notification_id).first() 
    if not notification:
       return jsonify({"status":201, "message" : "no notifications found! fot user_id: {} under notification_id : {}".format(user_id,notification_id)})
    return jsonify(notification.to_json())

"""
------------------   READ ALL NOTIFICATIONS --------------------

""" 
@accounts_bp.route('/api/v1/read_all', methods=('GET', 'POST'))
@jwt_required
def read_all():
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

   
    if not user_id:
       r = {"status": 201, "error": "user_id missing!"}
       return jsonify(r)

    notification = db.session.query(Notification).filter(and_(Notification.status_code == "Unread", Notification.author == user_id)).all() 
    if notification:
        for note in notification:
            note.status_code ="Read"
            db.session.commit()

    if not notification:
       return jsonify({"status":201, "message" : "no unread notifications found! for user_id: {} ".format(user_id)})
    return jsonify([note.to_json() for note in notification])



