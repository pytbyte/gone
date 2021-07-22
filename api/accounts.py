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

   """
    create email template
    handle email send  quing for scaling

   """
   msg = Message('#MyBlock sVerification Code',sender ="heretolearn1@gmail.com", recipients = [email])  
   msg.body = str('Jambo, use this code to confirm your account' + (str(otp))) 
   print(otp)
    
   #mail.send(msg)  
   return render_template('validate.html',user_data = user_data) 
   

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
    


@accounts_bp.route('/confirm_account',methods=["GET","POST"])   
def validate():  
    if "logged_in" not in session:
      flash(" your session has expired ! kindly login")
      return render_template("login.html")

    if request.method =="GET":
        user_data= Users.query.filter(and_(Users.username == session["current_user"], Users.status ==0)).first()
        flash(" submit code sent to "+ user_data.email) 
        return render_template('validate.html', user_data=user_data)
    
    user_data = Users.query.filter_by(username=session["current_user"]).first() 

    user_otp = request.form['otp']

    """
    SMS otp via Twillo/Africanstalking API

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

       product_data = Products.query.filter_by(status =0).all()
       service_data =Services.query.filter_by(status =0).all()
       business_data = Business.query.filter_by(owner = user_data.username).first()
       #message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()
       
       return render_template("user-profile.html",user_data=user_data, business_data=business_data)#,product_data=product_data, service_data=service_data)#message_data=message_data)

    flash(" The OTP code is either Invalidor expired! \nrequest a new one or retry")
    return render_template('validate.html',user_data=user_data)




@accounts_bp.route("/", methods=('GET', 'POST'))
def slash():
    if request.method == 'GET': 
       

       return render_template('index.html')




@accounts_bp.route("/marketplace", methods=('GET', 'POST'))
def marketplace():
    if request.method == 'GET':
       product_data = Products.query.filter_by(status =0).all()
       service_data =Services.query.filter_by(status =0).all()
       user_data = Users.query.filter_by(username = session['current_user']).first()
       business_data = Business.query.filter_by(owner = user_data.username).first()
       business = Business.query.filter_by(owner=user_data.username).first()

       categories = []
       
       for product in product_data:
          if product.product_category not in categories:
             categories.append(product.product_category)
       
       return render_template('shop.html', user_data = user_data, product_data= product_data, business_data= business_data, categories=categories,business=business)


@accounts_bp.route("/create", methods=('GET', 'POST'))
def register():
    if request.method == 'GET':      
       return render_template('user.html')

    #variable diclaration and definations  
    data=request.form
    name = request.form['full_name'] 
    username = request.form['user_name']
    password = request.form['password']
    contact = request.form['contact'] 
    email = request.form["email"]
    contact = data['contact']
    #full_name = data['full_name'] 
    #interests = data.get('interests'),
    status = 0,
    admin = 1 ,
    last_seen =sasa
    registered_on =sasa
    warning = []
 
    
    #check contact length
    if len(contact) < 10 or  len(contact) >13:
        flash(" Invalid phone number.\n Check and try again.")
        return render_template('user.html')    

    #check email for correctness,
    if Users.query.filter_by(email= email).first():
          flash("email address  registered already!")
          return render_template("user.html")

    regex= '^.+@[^\.].*\.[a-z]{2,}$'      
    if  (re.search(regex,email)):
        email=email
    else:  
        flash("invalid email address!")
        return  render_template("user.html")
    

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
                return render_template('user.html') 
         
          
        if  contact in existing_contacts :           
               flash(" contact : {}is  already registered before!".format(contact))          
               return render_template('user.html')      


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
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/media/personal/profile'
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
            flash("contact is not registerd in this system!")
            return render_template('login.html')

        #confirm credentials and login  user
        user = Users.query.filter(and_(Users.contact == contact, Users.status == 0)).first()
        if user is None or not user.check_password(password):
             flash(' INVALID ACCOUNT CREDNTIALS !')
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
              #verify()
              return redirect(url_for("accounts.verify")) 

        user_data = Users.query.filter_by(username = session['current_user']).first()
        business_data =Business.query.filter_by(status = 0).all()
        product_data =Products.query.filter_by(status = 0).all()
        business = Business.query.filter_by(owner=user_data.username).first()
        categories = []
       
        for product in product_data:
          if product.product_category not in categories:
             categories.append(product.product_category)


        

        return render_template('shop.html',user_data =user_data , product_data = product_data, categories=categories, business_data=business_data,business=business)

"""

----------------------------- logout ---------------------------

"""
@accounts_bp.route('/logout', methods=('GET', 'POST'))
def logout():
        if request.method == 'GET':
          logout_user()
          return render_template('login.html')

"""

----------------------------- student ---------------------------

"""
@accounts_bp.route('/students', methods=('GET', 'POST'))
def students():
        if request.method == 'GET':
          
          user_data = Users.query.filter_by(username = session['current_user']).first()
          business_data= Business.query.filter_by(owner = session['current_user']).first()
          product_data =Products.query.filter_by(status = 0).all()
          business = Business.query.filter_by(owner=user_data.username).first()
          categories = []
         
          for product in product_data:
            if product.product_category not in categories:
               categories.append(product.product_category)

          
          return render_template('student2.html',user_data=user_data, business_data=business_data,categories=categories,product_data=product_data)#, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

          



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
        full_name= data.get('full_name')
        email = data.get('email')
        username = data.get('username')
        contact = data.get('contact')
        
        admin = 1 ,
        last_seen =sasa
        

        x = session['current_user'] #get_jwt_identity()

        #check contact length and usage
        if contact:
            if len(contact) <10 and len(contact) >13:
              flash(" contact length is invalid !")
         
              return render_template("user-profile.html",user_data=user_data)


        if Users.query.filter(and_(Users.contact ==contact,Users.status==0)).first() is not None:
            user_ =Users.query.filter(and_(Users.contact ==contact, Users.status==0)).first()
            if user_.username != session["current_user"]:
              flash("contact is already registered by other user !")
            
              return render_template("user-profile.html",user_data=user_data)

            return render_template('user-profile.html',users_=users_)#, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

               

        #check email for correctness and usage,
        if  Users.query.filter(and_(Users.email == email,Users.status ==0)).first() is not  None:
            user_=Users.query.filter(and_(Users.email == email, Users.status==0)).first()      
            flash("email is registered to other user")  
            
            return render_template("user-profile.html",user_data=user_data)


        
        regex = '^.+@[^\.].*\.[a-z]{2,}$'
        if email and (re.search(regex,data['email'])):
           email = email
        else:
            if email:
              flash("email format is invalid!")
                
              return render_template("user-profile.html",user_data=user_data)



        #  maintain values
        user_=Users.query.filter(and_(Users.email == email,Users.status ==0)).first()
        _user = Users.query.filter_by(status = 0).all()
  
        existing_emails = []
        existing_full_name = []
        existing_contacts = []
        original_email =[]  
        original_contact =[]
        original_full_name =[]
     
        
               
        if user_data.username == session['current_user']: 
                existing_emails.append(user_data.email)
                existing_contacts.append(user_data.contact) 
                existing_full_name.append(user_data.name)


        if user_data.username == session["current_user"]:
                original_email =user_data.email 
                original_username =user_data.username
                original_contact =user_data.contact
                original_full_name =user_data.name

        #preserve unchanged fileds
        if not email:
           email =user_data.email
        if not contact:
           contact = user_data.contact
        
        if not username:
          username =user_data.username
        if not full_name:
          full_name =user_data.name
         
        user_data.email = email
        user_data.contact = contact
        user_data.username = username
        user_data.name = full_name

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
        business_data= Business.query.filter_by(owner = session['current_user']).first()
        product_data =Products.query.filter_by(status = 0).all()
        business = Business.query.filter_by(owner=user_data.username).first()
        categories = []
       
        for product in product_data:
          if product.product_category not in categories:
             categories.append(product.product_category)

        
        return render_template('user-profile.html',user_data=user_data, business_data=business_data,categories=categories,product_data=product_data)#, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

        

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
                        
            flash(" InvalidCurrent password ")
            
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
        file.save(os.path.join('/home/pato/myblock-01/api/static/media/personal/profile/'+str(user_data.id)+"/", f_name))
        if  not request.files["file"]:
           user_data.image_url=old_image
        if request.files["file"]:
           user_data.image_url = ('static/media/personal/profile/'+str(user_data.id)+"/"+f_name)
        db.session.commit()
   
    user_data =Users.query.filter_by(username=session["current_user"]).first()
    business_data = Business.query.filter_by(owner = user_data.id).first()
    return render_template('user-profile.html',user_data=user_data,business_data=business_data)




@accounts_bp.route("/business", methods=('GET', 'POST'))
def register_business():
    if request.method == 'GET':
      user_data = Users.query.filter_by(username = session["current_user"]).first()
      business_data = Business.query.filter_by(owner = user_data.id).first()
      product_data = Products.query.filter_by(status = 0).all()
      return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)


    #variable diclaration and definations  
    data=request.form
    businessname = request.form['business_name'] 
    owner = session["current_user"]
    business_category = request.form['business_category']
    
    businessemail = request.form["email"]
    businesscontact = request.form['phone']
    currency = request.form['currency']
    businesslocation= request.form['location']
    businessdsc = request.form['business_description']
    status = 0,
    admin = 1 ,
    last_seen =sasa
    registered_on =sasa
  
 
    user_data = Users.query.filter_by(username = session["current_user"]).first()
    #check contact length
    if len(businesscontact) < 10 or  len(businesscontact) >13:
        flash(" wrong phone number.Check and try again.")
        user_data = Users.query.filter_by(username = session["current_user"]).first()
        business_data = Business.query.filter_by(owner = user_data.id).first()
        product_data = Products.query.filter_by(status = 0).all()
        return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)   

    #check email for correctness,
    if Business.query.filter_by(businessemail = businessemail).first():
        flash("email address  registered already!")
        user_data = Users.query.filter_by(username = session["current_user"]).first()
        business_data = Business.query.filter_by(owner = user_data.id).first()
        product_data = Products.query.filter_by(status = 0).all()
        return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)

    regex= '^.+@[^\.].*\.[a-z]{2,}$'      
    if  (re.search(regex,businessemail)):
        businessemail=businessemail
    else:  
        flash("invalid email address!")
        user_data = Users.query.filter_by(username = session["current_user"]).first()
        business_data = Business.query.filter_by(owner = user_data.id).first()
        product_data = Products.query.filter_by(status = 0).all()
        return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)
    

    # duplicate value error handling 

    _business = Business.query.filter_by(status = 0).all()
    existing_businessnames = []
    existing_contacts = []
        

    for _business_ in _business:
        existing_businessnames.append(_business_.businessname)
        existing_contacts.append(_business_.businesscontact)   
  
    
        #response creation  
        if  businessname in existing_businessnames :          
                flash(" business_name : {} already taken. Try a unique one".format(business_name))
                user_data = Users.query.filter_by(username = session["current_user"]).first()
                business_data = Business.query.filter_by(owner = user_data.id).first()
                product_data = Products.query.filter_by(status = 0).all()
                return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)
         
          
        if  businesscontact in existing_contacts :           
               flash(" contact : {}is  already registered before!".format(businesscontact)) 
               user_data = Users.query.filter_by(username = session["current_user"]).first()
               business_data = Business.query.filter_by(owner = user_data.id).first()
               product_data = Products.query.filter_by(status = 0).all()
               return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)         
                  


    #user creation
    new_business = Business(
        businessname = request.form['business_name'] ,
        owner = session["current_user"],
        businesscategory = request.form['business_category'],
        businessemail = request.form["email"],
        businesscontact = data['phone'],
        currency =data['currency'],
        businesslocation= data['location'],
        businessdsc = data['business_description'],
        status = 0,
        admin = 1 ,
        last_seen =sasa,
        registered_on =sasa 
        )   

    # check new_business existance
    business_data =  Business.query.filter(and_(Business.businessemail == businessemail , Business.businesscontact == businesscontact ,Business.businessname ==businessname)).first() 
    if business_data:
        flash("Account data belongs to {{}}, kindly login.".fomart(business_data.businessname))
        user_data = Users.query.filter_by(username = session["current_user"]).first()
        business_data = Business.query.filter_by(owner = user_data.id).first()
        product_data = Products.query.filter_by(status = 0).all()
        return render_template('business.html', user_data=user_data , business_data=business_data, product_data=product_data)

    #save new user
    if not business_data:
       db.session.add(new_business)
       db.session.commit()
 
    created_business =   Business.query.filter(and_(Business.businessemail ==businessemail , Business.businesscontact == businesscontact ,Business.businessname ==businessname)).first() 
    if created_business.status == 0 :





        dest1 = created_business.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/media/business/logo'
        os.chdir(UPLOAD_)
        dest = dest1
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest1):
            os.mkdir("%s" % dest1)
        

        db.session.commit()
        return redirect(url_for('accounts.marketplace'))  








"""
------------------  LOGO PHOTO --------------------

""" 


@accounts_bp.route('/business_upload',  methods=('GET', 'POST'))

def upload_logo_pic():
    """
    uploads logo picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindly login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    business_data =Business.query.filter_by(owner =username).first()
    
    if request.method == 'POST':
        id = business_data.id
    
        if not request.files["file"]:
            flash(" no file selected for upload. ")            
            return render_template("business_profile.html",business_data=business_data)

            
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/media/business/logo/'+str(business_data.id)+"/", f_name))

        user_data =Users.query.filter_by(username=session["current_user"]).first()
        business_data = Business.query.filter_by(owner = session["current_user"]).first()
        business_data.logo_url = ('static/media/business/logo/'+str(business_data.id)+"/"+f_name)
        db.session.commit()

    user_data =Users.query.filter_by(username=session["current_user"]).first()
    business_data = Business.query.filter_by(owner = session["current_user"]).first()
    return render_template('business.html',business_data=business_data,user_data=user_data)





"""
------------------  UPDATE USER --------------------

"""


@accounts_bp.route('/update_business', methods=('GET', 'POST'))
def update_business():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")

        business_data = Business.query.filter_by(owner= session['current_user']).first()
        if request.method == 'GET':
            user_data = Users.query.filter_by(username = session["current_user"]).first()
            business_data = Business.query.filter_by(owner = user_data.username).first()
            product_data = Products.query.filter_by(status = 0).all()
            return render_template('business_profile.html', user_data=user_data , business_data=business_data, product_data=product_data)

        data= request.form
        _businessid = business_data.id
        
        businessemail = data.get('businessemail')
        businessname= data.get('businessname')
        businesscontact = data.get('businesscontact')
       
        
        admin = 1 ,
        last_seen =sasa
        

        x = session['current_user'] #get_jwt_identity()

        #check businesscontact length and usage
        if businesscontact:
            if len(businesscontact) <10 and len(businesscontact) >13:
              flash(" businesscontact {{}} is invalid !".format(businesscontact))
         
              return render_template("business.html",business_data=business_data)


        if Business.query.filter(and_(Business.businesscontact ==businesscontact,Business.status==0)).first() is not None:
            _business =Business.query.filter(and_(Business.businesscontact ==businesscontact, Business.status==0)).first()
            if _business.businessname!= session["current_user"]:
              flash("businesscontact {{}} is registered by {{}}!".format(businesscontact,_business.businessname))
            
              return render_template("business.html",business_data=business_data)

            return render_template('business.html',Business_=Business_)#, business_data =business_data, product_data = product_data,service_data=service_data,message_data=message_data)

               

        #check businessemail for correctness and usage,
        if  Business.query.filter(and_(Business.businessemail == businessemail,Business.status ==0)).first() is not  None:
            _business=Business.query.filter(and_(Business.businessemail == businessemail, Business.status==0)).first()      
            flash("businessemail {{}} is registered to {{}}.".format(businessemail,_business.businessname))  
            
            return render_template("business.html",business_data=business_data)


        
        regex = '^.+@[^\.].*\.[a-z]{2,}$'
        if businessemail and (re.search(regex,data['businessemail'])):
           businessemail = businessemail
        else:
            if businessemail:
              flash("businessemail {{}} is invalid!".format(businessemail))
                
              return render_template("business.html",business_data=business_data)



        #  maintain values
        _business=Business.query.filter(and_(Business.businessemail == businessemail,Business.status ==0)).first()
        _user = Business.query.filter_by(status = 0).all()
  
        existing_businessemails = []
       
        existing_businesscontacts = []
        original_businessemail =[]  
        original_businesscontact =[]
        
     
        

               
        if business_data.businessname== session['current_user']: 
                existing_businessemails.append(business_data.businessemail)
                existing_businesscontacts.append(business_data.businesscontact) 
            


        if business_data.businessname== session["current_user"]:
                original_businessemail =business_data.businessemail 
                original_businessname=business_data.businessname
                original_businesscontact =business_data.businesscontact
                

        #preserve unchanged fileds
        if not businessemail:
           businessemail =business_data.businessemail
        if not businesscontact:
           businesscontact = business_data.businesscontact
        
        if not businessname:
          businessname=business_data.businessname
       

        business_data.businessemail = businessemail
        business_data.businesscontact = businesscontact
        business_data.businessname= businessname
        

        #check who is saving
        if request.method == 'POST':
            if business_data.owner!= session["current_user"]:
                flash("you are not allowed to edit this data")
                
                return render_template("business.html",business_data=business_data)

        business_data.last_seen = sasa,
        
        # update _businessdat 
        try:
            db.session.commit()

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
      
        business_data = Business.query.filter_by(businessname= session['current_user']).first()
        user_data = Users.query.filter_by(username=session["current_user"]).first()
        return render_template('map.html',business_data=business_data,user_data=user_data)#, business_data =business_data, product_data = product_data,service_data=service_data,message_data=message_data)

        










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
       business = Business.query.filter_by(owner = user_data.username).first() 
       product_data = Products.query.filter(and_(Products.status ==0,Products.author_id ==business.id)).all()

       categories = []
       
       for product in product_data:
          if product.product_category not in categories:
             categories.append(product.product_category)


      
       return render_template("dashboard.html", user_data=user_data, product_data=product_data, business=business,categories=categories)


