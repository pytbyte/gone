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
from flask_mail import Mail, Message
from . import mail
from random import *
#from twilio.rest import Client, TwilioException

otp = randint(000000,999999) 
    
current_time = time.localtime()
sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

accounts_bp = Blueprint('accounts', __name__)
conn = create_engine('mysql+pymysql://root:sword@localhost/MyBlock')



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

@accounts_bp.route('/recommend', endpoint='recommender', methods=( 'GET','POST'))
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
@accounts_bp.route('/verify',methods = ["POST","GET"])  
def verify():
   if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

   user_data = Users.query.filter_by(username=session["current_user"]).first()  
   phone = user_data.contact

   email = user_data.email
   msg = Message('#MyBlock Account Verification Code',sender ="heretolearn1@gmail.com", recipients = [email])  
   msg.body = str('Jambo, use this code to confirm your account' + (str(otp)))  
   mail.send(msg)  
   
   

   """

  ------------------- attempt sms OTP sending ----------------------

  
  def _get_twilio_verify_client():
      return Client(
          current_app.config['TWILIO_ACCOUNT_SID'],
          current_app.config['TWILIO_AUTH_TOKEN']).verify.services(
              current_app.config['TWILIO_VERIFY_SERVICE_ID'])


  def request_verification_token(phone):
      verify = _get_twilio_verify_client()
      try:
          verify.verifications.create(to=phone, channel='sms')
      except TwilioException:
          verify.verifications.create(to=phone, channel='call')

  """    
   return render_template('validate.html',user_data = user_data)  


@accounts_bp.route('/confirm_account',methods=["GET","POST"])   
def validate():  
    if "logged_in" not in session:
      flash(" your session has expired ! kindly login")
      return render_template("login.html")

    if request.method =="GET":
        user_data= Users.query.filter(and_(Users.username == session["current_user"], Users.status ==0)).first()
        flash(" submit code sent to {{}}".format(user_data.email))
        return render_template('validate.html', user_data=user_data)
    
    user_data = Users.query.filter_by(username=session["current_user"]).first() 

    user_otp = request.form['otp']

    """

    token = request.form['otp']
    phone = user_data.contact

    #attempt to confirm otp

    def check_verification_token(phone, token):
      verify = _get_twilio_verify_client()
      try:
          result = verify.verification_checks.create(to=phone, code=token)
      except TwilioException:
          return False
      if result.status == 'approved':
         user_data.authenticated = 1
           db.session.add(user_data)
           db.session.commit()

  """
    if otp == int(user_otp):  
       user_data.authenticated = 1
       db.session.add(user_data)
       db.session.commit()

       product_data = products.query.filter_by(status =0).all()
       service_data =services.query.filter_by(status =0).all()
       #message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()
       message="too late to turn back now!"

       if not  product_data:
          return render_template("user-profile.html",user_data=user_data)#, service_data=service_data,message_data=message_data)

       if not  service_data:
          return render_template("user-profile.html",user_data=user_data)#,product_data=product_data,message_data=message_data)

       if not  product_data or service_data or message_data:
          flash("there are no products/services yet.")
          return render_template("user-profile.html",user_data=user_data)

       return render_template("user-profile.html",user_data=user_data)#,product_data=product_data, service_data=service_data)#message_data=message_data)

   
    return render_template('validate.html',user_data=user_data)




@accounts_bp.route("/", methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
      Product_data = Products.query.filter_by(status=0).all()
      if Product_data:
         return render_template('index.html', product_data=Product_data)
      else:
         return render_template('index.html')


    #variable diclaration and definations  
    data=request.form
    name = request.form['full_name'] 
    username = request.form['user_name']
    password = request.form['password']
    contact = request.form['contact'] 
    email = request.form["email"]
    contact = data['contact']
    whatsapp = data['whatsapp'] 
    #interests = data.get('interests'),
    status = 0,
    admin = 1 ,
    last_seen =sasa
    registered_on =sasa
    warning = []
 
    
    #check contact length
    if len(contact) < 10 or  len(contact) >13:
        flash(" wrong phone number.Check and try again.")
        return render_template('user-profile.html')    

    #check email for correctness,
    if Users.query.filter_by(email= email).first():
          flash("email address  registered already!")
          return render_template("user-profile.html")

    regex= '^.+@[^\.].*\.[a-z]{2,}$'      
    if  (re.search(regex,email)):
        email=email
    else:  
        flash("invalid email address!")
        return  render_template("user-profile.html")
    

    # duplicate value error handling 

    _user = Users.query.filter_by(status = 0).all()
    existing_usernames = []
    existing_contacts = []
        

    for _user_ in _user:
        existing_usernames.append(_user_.username)
        existing_contacts.append(_user_.contact)   
  
    
        #response creation  
        if  username in existing_usernames :          
                flash(" username : {} already taken. Try a unique one".format(username))
                return render_template('user-profile.html') 
         
          
        if  contact in existing_contacts :           
               flash(" contact : {}is  already registered before!".format(contact))          
               return render_template('user-profile.html')      


    #user creation
    new_user = Users(
        username = username,
        name =name,
        email = email,
        password_hash = generate_password_hash(password),
        contact = contact,        
        status = 0,
        admin = 1 ,
        last_seen = last_seen,
        registered_on = registered_on            
    )   

    # check new_user existance
    user_data =  Users.query.filter(and_(Users.email ==email , Users.contact == contact ,Users.username ==username)).first() 
    if user_data:
        flash("Account data belongs to {{}}, kindly login.".fomart(user_data.username))
        return render_template('login.html')

    #save new user
    if not user_data:
       db.session.add(new_user)
       db.session.commit()
 
    created_user =   Users.query.filter(and_(Users.email ==email , Users.contact == contact ,Users.username ==username)).first() 
    if created_user.status == 0 :

        dest = created_user.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/all_images/personal/profile'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
        return redirect(url_for('accounts.login'))  




"""
------------------  LOGIN --------------------

""" 


@accounts_bp.route('/login', methods=('GET', 'POST'))
def login():
        if request.method == 'GET':
          return render_template('login.html')

        #variable diclaration and definations    
        current_time = time.localtime()
        sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        data = request.form
        contact = data.get('contact')
        password = data.get("password")

        #check contact length and existance
        if len(contact) <10 and len(contact) >13:
            flash("invalid phone number: {{}} !".format(contact))
            return render_template('login.html')

        if  Users.query.filter(and_(Users.contact==contact, Users.status==0)).first() is None:
            flash("contact {{}} is unregisterd!".format(contact))
            return render_template('login.html')

        #confirm credentials and login  user
        user = Users.query.filter(and_(Users.contact == contact, Users.status == 0)).first()
        if user is None or not user.check_password(password):
             flash(' WRONG ACCOUNT CREDNTIALS !. try again!')
             return render_template('login.html')


        login_user(user)

        current_time = time.localtime()
        sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
        session['logged_in'] = True
        session["current_user"] = user.username
        targeted_user = user
        targeted_user.last_seen = sasa

        db.session.add(targeted_user)
        db.session.commit()



        username =user.username
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=username,expires_delta=expires) 
        user_data = Users.query.filter_by(contact=contact).first() 
      
 
        if not user_data.authenticated :
              
              flash("Jambo  {} ,Enter OTP code sent to {}.".format(user.username,user.email))
              verify()
              return redirect(url_for("accounts.verify")) #render_template('user-profile.html',user_id=user.id,access_token=access_token,user_data =user_data, product_data = product_data)
        user_data = Users.query.filter_by(username = session['current_user']).first()
      



        

        return render_template('user-profile.html',user_data =user_data)#product_data = product_data,service_data=service_data,message_data=message_data)




"""
------------------  UPDATE USER --------------------

"""


@accounts_bp.route('/update_user', methods=('GET', 'POST'))
def update_user():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")

        user_data = Users.query.filter_by(username = session['current_user']).first()


        data= request.form
        user_id = user_data.id
        name= data.get('full_name')
        email = data.get('email')
        username = data.get('username')
        contact = data.get('contact')
        whatsapp = data.get('whatsapp')
        admin = 1 ,
        last_seen =sasa
        

        x = session['current_user'] #get_jwt_identity()

        #check contact length and usage
        if contact:
            if len(contact) <10 and len(contact) >13:
              flash(" contact {{}} is invalid !".format(contact))
         
              return render_template("user-profile.html",user_data=user_data)


        if Users.query.filter(and_(Users.contact ==contact,Users.status==0)).first() is not None:
            user_ =Users.query.filter(and_(Users.contact ==contact, Users.status==0)).first()
            if user_.username != session["current_user"]:
              flash("contact {{}} is registered by {{}}!".format(contact,user_.username))
            
              return render_template("user-profile.html",user_data=user_data)

            return render_template('user-profile.html',users_=users_)#, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

               

        #check email for correctness and usage,
        if  Users.query.filter(and_(Users.email == email,Users.status ==0)).first() is not  None:
            user_=Users.query.filter(and_(Users.email == email, Users.status==0)).first()      
            flash("email {{}} is registered to {{}}.".format(email,user_.username))  
            
            return render_template("user-profile.html",user_data=user_data)


        
        regex = '^.+@[^\.].*\.[a-z]{2,}$'
        if email and (re.search(regex,data['email'])):
           email = email
        else:
            if email:
              flash("email {{}} is invalid!".format(email))
                
              return render_template("user-profile.html",user_data=user_data)



        #  maintain values
        user_=Users.query.filter(and_(Users.email == email,Users.status ==0)).first()
        _user = Users.query.filter_by(status = 0).all()
  
        existing_emails = []
        existing_whatsapp = []
        existing_contacts = []
        original_email =[]  
        original_contact =[]
        original_whatsapp =[]
     
        if not user_data.whatsapp:
                # update user_dat 
                user_data.whatsapp = whatsapp
                try:
                    db.session.commit()

                #handle error and retain pre edit data (rollback)
                except exc.IntegrityError as e :
                    db.session.rollback()

               
        if user_data.username == session['current_user']: 
                existing_emails.append(user_data.email)
                existing_contacts.append(user_data.contact) 
                existing_whatsapp.append(user_data.whatsapp)


        if user_data.username == session["current_user"]:
                original_email =user_data.email 
                original_username =user_data.username
                original_contact =user_data.contact
                original_whatsapp =user_data.whatsapp

        #preserve unchanged fileds
        if not email:
           email =user_data.email
        if not contact:
           contact = user_data.contact
        
        if not username:
          username =user_data.username
        if not whatsapp:
          whatsapp =user_data.whatsapp

        user_data.email = email
        user_data.contact = contact
        user_data.username = username
        user_data.whatsapp = whatsapp

        #check who is saving
        if user_data.username != session["current_user"]:
            flash("you are not allowed to edit this data")
            
            return render_template("user-profile.html",user_data=user_data)

        user_data.last_seen = sasa,
        
        # update user_dat 
        try:
            db.session.commit()

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
      
        user_data = Users.query.filter_by(username = session['current_user']).first()
        return render_template('user-profile.html',user_data=user_data)#, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

        

"""
------------------  UPDATE PASSWORD--------------------

"""


@accounts_bp.route('/update_password', methods=('GET', 'POST'))
def update_password():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")

        user_data = Users.query.filter_by(username = session['current_user']).first()


        data= request.form
        user_id = user_data.id
        password = data.get('current-password')
        new_password = data.get('new_password')
        
        
        x = session['current_user'] #get_jwt_identity()

        user = Users.query.filter_by(username = session['current_user']).first()
        if user is None or not user.check_password(password):
                        
            flash(" wrong Current password ")
            
            return render_template("user-profile.html",user_data=user_data)

        
        user_data.password_hash= generate_password_hash(new_password)
        # update user_dat 
        try:
            db.session.commit()

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
        user_data = Users.query.filter_by(username = session['current_user']).first()
        flash('Password updated successfully, you will use it on next login')
        return render_template('user-profile.html',user_data=user_data)


"""
------------------  PROFILE PHOTO --------------------

""" 


@accounts_bp.route('/profile_upload',  methods=('GET', 'POST'))

def upload_prof_pic():
    """
    uploads profile picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindly login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    user_data = Users.query.filter_by(username =username).first()
    
    if request.method == 'POST':
        id = user_data.id
    
        if not request.files["file"]:
            flash(" no file selected for upload. ")            
            return render_template("user-profile.html",user_data=user_data)

            
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/all_images/personal/profile/'+str(user_data.id)+"/", f_name))
        if  not request.files["file"]:
           user_data.image_url=old_image
        if request.files["file"]:
           user_data.image_url = ('static/all_images/personal/profile/'+str(user_data.id)+"/"+f_name)
        db.session.commit()
 
    user_data =Users.query.filter_by(username=session["current_user"]).first()
    return render_template('user-profile.html',users_=user_data)








"""
------------------  DASHBOARD--------------------

""" 
@accounts_bp.route('/dashboard',methods = ["POST","GET"])  
def dashboard():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
      
       return render_template("dashboard.html", user_data=user_data)






"""
------------------  PRODUCTS--------------------

""" 
@accounts_bp.route('/products',methods = ["POST","GET"])  
def products():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
      
       return render_template("products.html", user_data=user_data)





"""
------------------  PRODUCT-LIST --------------------

""" 
@accounts_bp.route('/product_list',methods = ["POST","GET"])  
def product_list():
    if "logged_in"  not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()       
       return render_template("product_list.html", user_data=user_data)

    username =session["current_user"]
    user_data =Users.query.filter_by(username= username).first()

    # create product  photo directory
    UPLOAD_ = '/home/pato/myblock-01/api/static/all_images/business/products/'
    os.chdir(UPLOAD_)
    dest = user_data.id
    UPLOAD_FOLDER =UPLOAD_+str(dest)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isdir("%s" % dest):
        os.mkdir("%s" % dest)
        os.chdir(BASE_DIR)

    if request.method == 'POST':
          
        #get  userdata
        username =session["current_user"]
        user_data =Users.query.filter_by(username= username).first()    
        
        data= request.form
        author_id = user_data.id
        product_title= data.get('product_name')
        product_description = data.get('product_description')
        product_category = data.get('product_category')
        price = data.get('product_cost')
        status = 0
        timestamp =sasa

         
        new_product = Products(
            product_title = product_title,
            product_description = product_description,
            author_id = author_id,            
            product_category = product_category,
            price = price,
            status = 0,
            timestamp = sasa
            )
        
        db.session.add(new_product)
        db.session.commit()

      
        product_data = db.session.query(Products).filter(and_(Products.product_title == product_title, Products.price ==price)).first()
        username =session["current_user"]
        user_data =Users.query.filter_by(username= username).first()


        id = user_data.id
        links =[]
        if "files[]" not in request.files:
           flash(" missing product image")
           return render_template("product_list.html", user_data=user_data)

        count = 0
        upfile = request.files.getlist('files[]')
        for file in upfile:
            if file.filename != '':
               extension = os.path.splitext(file.filename)[1]
               f_name = str(uuid.uuid4()) + extension
               file.save(os.path.join('/home/pato/myblock-01/api/static/all_images/business/products/'+str(user_data.id)+"/", f_name))
               image_url= ('static/all_images/business/products/'+str(user_data.id)+"/"+f_name)
              
               links.append(image_url)
        
        stack = [string for string in links if string != ""]

        if len(links) == 1:  #<  str(range(len(stack))) :
               product_data.image_url=links[0]  
               db.session.commit()            
               
        if len(links) >= 1:  #<  str(range(len(stack))) :
               product_data.image_url=links[0]
               db.session.commit() 
               

        if len(links) >= 2: #< str(range(len(stack))) :
               product_data.image_url1= links[1]
               db.session.commit() 
              
        if len(links) >= 3: #< str(range(len(stack))):
               product_data.image_url2= links[2]
               db.session.commit() 
               
        if len(links) >= 4: #< str (rartnge(len(stack))):
               product_data.image_url3= links[3]
               db.session.commit() 
               
        if len(links) >= 5: #<=  str(range(len(stack))):
               product_data.image_url4= links[4]
               db.session.commit() 
              
    return render_template("product_list.html", user_data=user_data) 




"""
------------------  SERVICES--------------------

""" 
@accounts_bp.route('/services',methods = ["POST","GET"])  
def services():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
      
       return render_template("services.html", user_data=user_data)




"""
------------------  events--------------------

""" 
@accounts_bp.route('/events',methods = ["POST","GET"])  
def events():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
      
       return render_template("events.html", user_data=user_data)