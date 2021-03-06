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
#from flask_mysqldb import MySQL # sudo apt install default-libmysqlclient-dev  b4 installing flask-mysqldb
from flask_sqlalchemy import SQLAlchemy
from models.model import db
import urllib.request
from sqlalchemy import create_engine, exc,desc,or_,and_
from flask import Flask, request, redirect, jsonify,make_response,json,Blueprint
from werkzeug.utils import secure_filename
from flask_jwt_extended import ( JWTManager, jwt_required, create_access_token,get_jwt_identity)
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.model import *
from itsdangerous.url_safe import URLSafeTimedSerializer
from flask_mail import Mail, Message
from . import mail
from random import *
#from twilio.rest import Client, TwilioException

otp = randint(000000,999999) 

current_time = time.localtime()
sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

accounts_bp = Blueprint('accounts', __name__)
#conn = create_engine('mysql+pymysql://root:TheBl0cK!*@localhost/MyBlock')




"""
------------------  PUSH NOTIFICATION --------------------

""" 
#@jwt_required
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


def notifier(activity,timestamp,message,data_url, user_data_url, status_code,notified_user,author):
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

@accounts_bp.route('/api/v1/recommend', methods=( 'GET','POST'))
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



def  send_email(user_email, html):
    email = user_email
    msg = Message('Confirm Email', sender='heretolearn1@gmail.com', recipients=[email])

    msg.body = html

    mail.send(msg)
    return "mail sent"

"""
------------------  LOGGED CHECKER --------------------

""" 
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('To enjoy our services , kindly login!')
            return render_template('login.html')
    return wrap




"""
-----------  REGISTER --------------------

"""
@accounts_bp.route('/verify',methods = ["POST","GET"])  
def verify():
   if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

   user_data = Users.query.filter_by(username=session["current_user"]).first()  
   phone = user_data.contact

   email = user_data.email
   msg = Message('#MyBlock Account Verification Code',sender ="noreply@MyBlock.com", recipients = [email])  
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
       message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()


       if not  product_data:
          return render_template("user.html",user_data=user_data, service_data=service_data,message_data=message_data)

       if not  service_data:
          return render_template("user.html",user_data=user_data,product_data=product_data,message_data=message_data)

       if not  product_data or service_data or message_data:
          flash("there are no products/services yet.")
          return render_template("user.html",user_data=user_data)

       return render_template("user.html",user_data=user_data,product_data=product_data, service_data=service_data,message_data=message_data)

   
    return render_template('validate.html',user_data=user_data)

@accounts_bp.route('/', methods=("GET","POST"))
def landing():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
      return render_template('index.html')


@accounts_bp.route('/logout', methods=("GET","POST"))
def logout():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
      logout_user()
      session.clear()
      return render_template('login.html')




@accounts_bp.route('/rides', methods=("GET","POST"))
def rides():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")
    if request.method == 'GET':
      bike_data =  Bikes.query.filter(and_(Bikes.owner ==session['current_user'], Bikes.status !=1)).first()
      user_data = Users.query.filter_by(username=session["current_user"]).first() 
      if bike_data:
      	return render_template('bike_data.html',bike_data = bike_data, user_data =	user_data )

      return render_template('block.html')



@accounts_bp.route('/ride', methods=("GET","POST"))
def ride():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")
    if request.method == 'GET':
      bikes =  Bikes.query.filter(Bikes.status !=1).all()
      user_data = Users.query.filter_by(username=session["current_user"]).first() 
      if bikes :
      	return render_template('block.html',bikes = bikes, user_data =	user_data )

      return render_template('block.html', bikes = bikes, user_data =	user_data )


@accounts_bp.route('/Taxis', methods=("GET","POST"))
def taxiz():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")
    if request.method == 'GET':
      taxis =  Taxis.query.filter(Taxis.status !=1).all()
      taxi_data =  Taxis.query.filter(Taxis.owner == session['current_user']).first()
      user_data = Users.query.filter_by(username=session["current_user"]).first() 
      if taxis :
      	return render_template('taxi_data.html',taxi_data = taxi_data, user_data =	user_data )

      return render_template('block1.html', Taxis = Taxis, user_data =	user_data )


@accounts_bp.route('/Truck', methods=("GET","POST"))
def truckz():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")
    if request.method == 'GET':
      TRUCK =  Trucks.query.filter(Trucks.status !=1).all()
      truck_data =  Trucks.query.filter(Trucks.owner == session['current_user']).first()
      user_data = Users.query.filter_by(username=session["current_user"]).first() 
      if truck_data :
      	return render_template('truck_data.html',truck_data = truck_data, user_data =	user_data )

      return render_template('block1.html', Trucks = TRUCK, user_data =	user_data )

@accounts_bp.route('/cabs', methods=("GET","POST"))
def drivers():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
      taxis =  Taxis.query.filter(Taxis.status !=1).all()
      return render_template('block1.html', taxi_data = taxis)


@accounts_bp.route('/trucks', methods=("GET","POST"))
def trucks():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
      truck_data =Trucks.query.filter(Trucks.status !=1).all()
      return render_template('truck.html', truck_data = truck_data)




@accounts_bp.route('/business', methods=("GET","POST"))
def biz():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
       # check newbusiness existance
       if 'logged_in' in session:
       	 business_data =  Business.query.filter(and_(Business.owner ==session['current_user'], Business.status !=1)).first()
         if business_data:
            return render_template('panel.html',businessdata = business_data)

     
       return render_template('businesses.html')

    #variable declaration
    latlng = request.form['latlng']
    businessname = request.form['businessname']
    businesscontact = request.form['contact']
    businesscategory = request.form['businesscategory']
    businessdsc = request.form['businessdsc']
    workinghours = request.form['workinghours']
      
    status = 0,
    last_seen =sasa
    registered_on =sasa
  
    
    # duplicate value error handling 

    busines = Business.query.filter_by(status = 0).all()
    existing_business = []
   
        

    for business_ in busines:
        existing_business.append(business_.businessname)
        
    
 
    user_data =Users.query.filter_by(username = session['current_user']).first()
    #business_data =Business.query.filter_by(owner = session['current_user']).first()
             

    #user creation
    newbusiness = Business(
        businessname = businessname, 
        businesscontact =businesscontact,
        businesscategory = businesscategory,
        businessdsc = businessdsc,
        workinghours = workinghours,
        owner = session['current_user'],
        status = 0,
        last_seen = last_seen,
        latlng = latlng,
        registered_on = registered_on            
    )   
          
    # check newbusiness existance
    business_data =  Business.query.filter(and_(Business.businesscontact == businesscontact ,Business.businessname ==businessname)).first() 
    if business_data:
        flash(" {}, is already registered here try other contacts ".format(business_data.businessname))
        return render_template('business.html',businessdata=business_data)


     # check newbusiness existance
    business_data =  Business.query.filter(and_(Business.businesscontact ==businesscontact ,Business.status ==0)).first() 
    if business_data:
        flash(" {}, is already registered here try other contacts ".format(business_data.businesscontact))
        return render_template('business.html',businessdata=business_data)



    #save newbusiness
    if not business_data:
    
       db.session.add(newbusiness)
       db.session.commit()
 
    createdbusiness =   Business.query.filter(and_( Business.businesscontact == businesscontact ,Business.businessname ==businessname)).first() 
    if createdbusiness.status == 0 :

        dest = createdbusiness.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/images/Business/profile'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
        flash("Welcome  {}.".format(createdbusiness.businessname))
        return render_template('panel.html', businessdata = createdbusiness)  








@accounts_bp.route('/dashboard', methods=("GET","POST"))
def dashboard():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)


    if request.method == 'GET':
      return render_template('dashboard.html')






@accounts_bp.route('/riders', methods=("GET","POST"))
def enroll():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if "logged_in" not  in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method == 'GET':
      return render_template('rider.html')

  
    #variable diclaration and definations    
    
    registration_no = request.form['registration_no']
    model = request.form['motorcycle_model']
    route = request.form['route']
    status = 0,
    last_seen =sasa
    registered_on =sasa
  
    
    # duplicate value error handling 

    bike = Bikes.query.filter_by(status = 0).all()
    existing_reg_no = []
   
        

    for bike_ in bike:
        existing_reg_no.append(bike_.registration_no)
        
    
        #response creation  
        if  registration_no in existing_reg_no :          
                flash(" registration_no : {} already enrolled".format(registration_no))
                return render_template('rider.html') 
         
    user_data = Users.query.filter_by(username = session['current_user']).first()
             

    #user creation
    newbike = Bikes(
        registration_no = registration_no, 
        make = model,       
        contact = user_data.contact,
        owner = user_data.username,
        status = 0,
        last_seen = last_seen,
        registered_on = registered_on,
        route = route   

    )   

          
    # check newbike existance
    bike_data =  Bikes.query.filter(and_(Bikes.owner ==user_data.username , Bikes.contact == user_data.contact ,Bikes.registration_no ==registration_no)).first() 
    if bike_data:
        flash(" {{}}, is already registered here".format(bike_data.registration_no))
        return render_template('rider.html')

    #save new user
    if not bike_data:
       db.session.add(newbike)
       db.session.commit()
 
    createdbike =   Bikes.query.filter(and_( Bikes.contact == user_data.contact ,Bikes.registration_no ==registration_no)).first() 
    
    flash("Welcome  {}.".format(createdbike.registration_no))
    return render_template('bike_data.html', bike_data = createdbike, user_data =user_data)  



"""
------------------  UPDATE USER --------------------

"""


@accounts_bp.route('/bike_edit', methods=('GET', 'POST', 'PUT'))
def update_bike():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")
        
        if request.method == 'GET':
           user_data = Users.query.filter_by(username = session['current_user']).first()
           bike_data = Bikes.query.filter_by(owner = session['current_user']).first()

           return render_template('bike_data.html', bike_data=bike_data, user_data =user_data)


        user_data = Users.query.filter_by(username = session['current_user']).first()
        bike_data = Bikes.query.filter_by(owner = session['current_user']).first()




        #update user location

        #latlon = request.form('latlon')
        #user_data.latlon = latlon
        #db.session.add(user_data)
        #db.session.commit()      
        #variable diclaration and definations
        data= request.form
        bike_id = bike_data.id
        
        registration_no = request.form['registration_no']
        model = request.form['motorcycle_model']
        route = request.form['route']
        
        last_seen =sasa
        

        x = session['current_user'] #get_jwt_identity()

         

        #  maintain values
        bike_data=Bikes.query.filter(and_(Bikes.status == 0, Bikes.owner ==session['current_user'])).first()
        _bike = Bikes.query.filter_by(status = 0).all()
  
        existing_route = []
        existing_registration = []
        original_route =[]  
        original_registration =[]
        if bike_data:

	        if bike_data.registration_no == registration_no: 
	                existing_registration.append(bike_data.registration_no)
	                existing_route.append(bike_data.route) 
	        if bike_data.owner == session["current_user"]:
	                original_registration =bike_data.registration_no
	                original_route =bike_data.route
             

	        #preserve unchanged fileds
	        if not registration_no:
	           registration_no =bike_data.registration_no
	        if not route:
	           route = ride_data.route
            
        # update user_dat 
        try:
          bike_data.registration_no = registration_no
          bike_data.route = route
          
          db.session.commit()
          session["active_bike"] = bike_data.registration_no

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
        

        #check who is saving
        if not session["current_user"]:
            flash("you are not allowed to edit this data")
            bike_data=Bikes.query.filter(and_(Bikes.registration_no == registration_no, Bikes.owner ==0)).first()
            return render_template('bike_data.html', bike_data =bike_data,user_data =user_data)

          

        
       
        
      
       
        return render_template('bike_data.html', bike_data =bike_data,user_data =user_data)
        



"""
------------------  PROFILE PHOTO --------------------

""" 


@accounts_bp.route('/bike_upload',  methods=('GET', 'POST'))

def upload_bike_pic():
    """
    uploads profile picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindlg login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    bike_data = Bikes.query.filter_by(owner =username).first()
 
        

    
    if request.method == 'POST':


        id = bike_data.id
    
        if not request.files["file"]:
            flash(" no file seldcted for upload. ")
            return render_template('bike_edit.html', bike_data =bike_data)

        

        dest = bike_data.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/images/bikes/'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)


        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/images/bikes/'+str(bike_data.id)+"/", f_name))
        if  not request.files["file"]:
           user_data.image_url=old_image
        if request.files["file"]:
           bike_data.image_url = ('static/images/bikes/'+str(bike_data.id)+"/"+f_name)
        db.session.commit()
 
    bike_data = Bikes.query.filter_by(owner =username).first()
    
    user_data = Users.query.filter_by(username = session['current_user']).first()
    return render_template('bike_data.html', bike_data =bike_data, user_data =	user_data)









@accounts_bp.route('/taxis', methods=("GET","POST"))
def enroll_taxi():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method == 'GET':
      return render_template('taxis.html')


    #variable diclaration and definations    
    
    registration_no = request.form['registration_no']
    model = request.form['taxi_model']
    seater = request.form['taxi_seater']
    route = request.form['taxi_route']
    status = 0,
    last_seen =sasa
    registered_on =sasa
  
    
    # duplicate value error handling 

    taxi = Taxis.query.filter_by(status = 0).all()
    existing_reg_no = []
   
        

    for taxi_ in taxi:
        existing_reg_no.append(taxi_.registration_no)
        
    
        #response creation  
        if  registration_no in existing_reg_no :          
                flash(" registration_no : {} already enrolled".format(registration_no))
                return render_template('taxis.html') 
         
    user_data = Users.query.filter_by(username = session['current_user']).first()
             

    #user creation
    newtaxi = Taxis(
        registration_no = registration_no, 
        make = model,       
        contact = user_data.contact,
        owner = user_data.username,
        status = 0,
        last_seen = last_seen,
        seater = seater,
        route = route,
        registered_on = registered_on            
    )   

          
    # check newtaxi existance
    taxi_data =  Taxis.query.filter(and_(Taxis.owner ==user_data.username , Taxis.contact == user_data.contact ,Taxis.registration_no ==registration_no)).first() 
    if taxi_data:
        flash(" {{}}, is already registered here".format(taxi_data.registration_no))
        return render_template('taxis.html')

    #save new user
    if not taxi_data:
       db.session.add(newtaxi)
       db.session.commit()
 
    createdtaxi =   Taxis.query.filter(and_( Taxis.contact == user_data.contact ,Taxis.registration_no ==registration_no)).first() 
    
    flash("Welcome  {}.".format(createdtaxi.registration_no))
    return render_template('taxi_data.html', taxi_data = createdtaxi, user_data= user_data)



"""
------------------  UPDATE TAXIS --------------------

"""


@accounts_bp.route('/taxi_edit', methods=('GET', 'POST', 'PUT'))
def update_taxi():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")
        
        if request.method == 'GET':
           user_data = Users.query.filter_by(username = session['current_user']).first()
           taxi_data = Taxis.query.filter_by(owner = session['current_user']).first()

           return render_template('taxi_data.html', taxi_data=taxi_data, user_data =user_data)


        user_data = Users.query.filter_by(username = session['current_user']).first()
        taxi_data = Taxis.query.filter_by(owner = session['current_user']).first()




        #update user location

        #latlon = request.form('latlon')
        #user_data.latlon = latlon
        #db.session.add(user_data)
        #db.session.commit()      
        #variable diclaration and definations
        data= request.form
        taxi_id = taxi_data.id
        
        registration_no = request.form['registration_no']
        model = request.form['taxi_model']
        seater = request.form['taxi_seater']
        route = request.form['taxi_route']
        

        
        last_seen =sasa
        

        x = session['current_user'] #get_jwt_identity()

         

        #  maintain values
        taxi_data=Taxis.query.filter(and_(Taxis.status == 0, Taxis.owner ==session['current_user'])).first()
        _taxi = Taxis.query.filter_by(status = 0).all()
  
        existing_route = []
        existing_registration = []
        original_route =[]  
        original_registration =[]
        if taxi_data:

	        if taxi_data.registration_no == registration_no: 
	                existing_registration.append(taxi_data.registration_no)
	                existing_route.append(taxi_data.route) 
	        if taxi_data.owner == session["current_user"]:
	                original_registration =taxi_data.registration_no
	                original_route =taxi_data.route
             

	        #preserve unchanged fileds
	        if not registration_no:
	           registration_no =taxi_data.registration_no
	        if not route:
	           route = taxi_data.route
            
        # update user_dat 
        try:
          taxi_data.registration_no = registration_no
          taxi_data.route = route
          taxi_data.make = model
          taxi_data.seater = seater
          
          db.session.commit()
          session["active_taxi"] = taxi_data.registration_no

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
        

        #check who is saving
        if not session["current_user"]:
            flash("you are not allowed to edit this data")
            taxi_data=Taxis.query.filter(and_(Taxis.registration_no == registration_no, Taxis.owner ==user_data.session['current_user'])).first()
            return render_template('taxi_data.html', taxi_data =taxi_data,user_data =user_data)

          

        
       
        
      
       
        return render_template('taxi_data.html', taxi_data =taxi_data,user_data =user_data)
        



"""
------------------  PROFILE PHOTO --------------------

""" 


@accounts_bp.route('/taxi_upload',  methods=('GET', 'POST'))

def upload_taxi_pic():
    """
    uploads profile picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindlg login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    taxi_data = Taxis.query.filter_by(owner =username).first()
 
        

    
    if request.method == 'POST':


        id = taxi_data.id
    
        if not request.files["file"]:
            flash(" no file seldcted for upload. ")
            return render_template('taxi_edit.html', taxi_data =taxi_data)

        

        dest = taxi_data.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/images/taxis/'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)


        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/images/taxis/'+str(taxi_data.id)+"/", f_name))
        if  not request.files["file"]:
           user_data.image_url=old_image
        if request.files["file"]:
           taxi_data.image_url = ('static/images/taxis/'+str(taxi_data.id)+"/"+f_name)
        db.session.commit()
 
    taxi_data = Taxis.query.filter_by(owner =username).first()
    
    user_data = Users.query.filter_by(username = session['current_user']).first()
    return render_template('taxi_data.html', taxi_data =taxi_data, user_data =	user_data)






@accounts_bp.route('/truck', methods=("GET","POST"))
def enroll_truck():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
   
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")



   
    if request.method == 'GET':
      return render_template('trucks.html')


    #variable diclaration and definations    
    
    registration_no = request.form['registration_no']
    model = request.form['Truck_model']
    route = request.form['Truck_route']
    
    status = 0,
    last_seen =sasa
    registered_on =sasa
  
    
    # duplicate value error handling 

    truck = Trucks.query.filter_by(status = 0).all()
    existing_reg_no = []
   
        

    for truck_ in truck:
        existing_reg_no.append(truck_.registration_no)
        
    
        #response creation  
        if  registration_no in existing_reg_no :          
                flash(" registration_no : {} already enrolled".format(registration_no))
                return render_template('trucks.html') 
         
    user_data = Users.query.filter_by(username = session['current_user']).first()
             

    #user creation
    newtruck = Trucks(
        registration_no = registration_no, 
        make = model,       
        contact = user_data.contact,
        owner = user_data.username,
        status = 0,
        last_seen = last_seen,
        route = route,
        registered_on = registered_on            
    )   

          
    # check newtruck existance
    truck_data =  Trucks.query.filter(and_(Trucks.owner ==user_data.username , Trucks.contact == user_data.contact ,Trucks.registration_no ==registration_no)).first() 
    if truck_data:
        flash(" {{}}, is already registered here".format(truck_data.registration_no))
        return render_template('trucks.html')

    #save new user
    if not truck_data:
       db.session.add(newtruck)
       db.session.commit()
 
    createdtruck =    Trucks.query.filter(and_(Trucks.owner ==user_data.username , Trucks.contact == user_data.contact ,Trucks.registration_no ==registration_no)).first() 
    
    flash("Welcome  {}.".format(createdtruck.registration_no))
    return render_template('truck_data.html', truck_data = createdtruck, user_data = user_data) 






"""
------------------  UPDATE truckS --------------------

"""


@accounts_bp.route('/truck_edit', methods=('GET', 'POST', 'PUT'))
def update_truck():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")
        
        if request.method == 'GET':
           user_data = Users.query.filter_by(username = session['current_user']).first()
           truck_data = Trucks.query.filter_by(owner = session['current_user']).first()

           return render_template('truck_data.html', truck_data=truck_data, user_data =user_data)


        user_data = Users.query.filter_by(username = session['current_user']).first()
        truck_data = Trucks.query.filter_by(owner = session['current_user']).first()




        #update user location

        #latlon = request.form('latlon')
        #user_data.latlon = latlon
        #db.session.add(user_data)
        #db.session.commit()      
        #variable diclaration and definations
        data= request.form
        truck_id = truck_data.id
        
        registration_no = request.form['registration_no']
        model = request.form['Truck_model']
        route = request.form['Truck_route']
        

        
        last_seen =sasa
        

        x = session['current_user'] #get_jwt_identity()

         

        #  maintain values
        truck_data=Trucks.query.filter(and_(Trucks.status == 0, Trucks.owner ==session['current_user'])).first()
        _truck = Trucks.query.filter_by(status = 0).all()
  
        existing_route = []
        existing_registration = []
        original_route =[]  
        original_registration =[]
        if truck_data:

	        if truck_data.registration_no == registration_no: 
	                existing_registration.append(truck_data.registration_no)
	                existing_route.append(truck_data.route) 
	        if truck_data.owner == session["current_user"]:
	                original_registration =truck_data.registration_no
	                original_route =truck_data.route
             

	        #preserve unchanged fileds
	        if not registration_no:
	           registration_no =truck_data.registration_no
	        if not route:
	           route = truck_data.route
            
        # update user_dat 
        try:
          truck_data.registration_no = registration_no
          truck_data.route = route
          truck_data.make = model
          
          
          db.session.commit()
          session["active_truck"] = truck_data.registration_no

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
        

        #check who is saving
        if not session["current_user"]:
            flash("you are not allowed to edit this data")
            truck_data=Trucks.query.filter(and_(Trucks.registration_no == registration_no, Trucks.owner ==user_data.session['current_user'])).first()
            return render_template('truck_data.html', truck_data =truck_data,user_data =user_data)

          

        
       
        
      
       
        return render_template('truck_data.html', truck_data =truck_data,user_data =user_data)
        



"""
------------------  PROFILE PHOTO --------------------

""" 


@accounts_bp.route('/truck_upload',  methods=('GET', 'POST'))

def upload_truck_pic():
    """
    uploads profile picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindlg login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    truck_data = Trucks.query.filter_by(owner =username).first()
 
        

    
    if request.method == 'POST':


        id = truck_data.id
    
        if not request.files["file"]:
            flash(" no file seldcted for upload. ")
            return render_template('truck_edit.html', truck_data =truck_data)

        

        dest = truck_data.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/images/trucks'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)


        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/images/trucks/'+str(truck_data.id)+"/", f_name))
        if  not request.files["file"]:
           user_data.image_url=old_image
        if request.files["file"]:
           truck_data.image_url = ('static/images/trucks/'+str(truck_data.id)+"/"+f_name)
        db.session.commit()
 
    truck_data = Trucks.query.filter_by(owner =username).first()
    
    user_data = Users.query.filter_by(username = session['current_user']).first()
    return render_template('truck_data.html', truck_data =truck_data, user_data =	user_data)













@accounts_bp.route('/register', methods=("GET","POST"))
def register():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
      return render_template('user.html')


    #variable diclaration and definations    
    
    username = request.form['username']
    password = request.form['password']
    contact = request.form['contact'] 
    email = request.form["email"]
    status = 0,
    admin = 1 ,
    last_seen =sasa
    registered_on =sasa
  
    #check contact length
    if len(contact) < 10 or  len(contact) >13:
        flash(" invalid phone number.Check and try again.")
        return render_template('user.html')    

    #check email for correctness,
    if Users.query.filter_by(email= email).first():
          flash(" {} has been registered before!".format(email))
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
        password_hash =generate_password_hash(password),
        contact = contact,
        email = email,
        status = 0,
        last_seen = last_seen,
        registered_on = registered_on            
    )   

          
    # check new_user existance
    user_data =  Users.query.filter(and_(Users.email ==email , Users.contact == contact ,Users.username ==username)).first() 
    if user_data:
        flash("Welcome back {{}}, kindly login.".format(user_data.username))
        return render_template('login.html')

    #save new user
    if not user_data:
       db.session.add(new_user)
       db.session.commit()
 
    created_user =   Users.query.filter(and_(Users.email ==email , Users.contact == contact ,Users.username ==username)).first() 
    if created_user.status == 0 :

        dest = created_user.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/images/personal/profile'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
        flash("Welcome  {}, kindly login.".format(created_user.username))
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
        #access_token = create_access_token(identity=username,expires_delta=expires) 
        user_data = Users.query.filter_by(contact=contact).first() 
        #product_data= products.query.filter_by(status = 0).all()
        '''
        if not user_data.authenticated :
              
              flash("Jambo  {} ,Enter OTP code sent to {}.".format(user.username,user.email))
              #verify()
              return redirect(url_for("accounts.verify")) #render_template('user.html',user_id=user.id,access_token=access_token,user_data =user_data, product_data = product_data)
        '''
        user_data = Users.query.filter_by(username = session['current_user']).first()
      

        #product_data = products.query.filter_by(status =0).all()
        #service_data =services.query.filter_by(status =0).all()
        #message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()
        
        '''
        if not  product_data:
          return render_template("user.html",user_data=user_data, service_data=service_data,message_data=message_data)

        if not  service_data:
          return render_template("user.html",user_data=user_data,product_data=product_data,message_data=message_data)

        if not  product_data or service_data or message_data:
          flash("there are no products/services yet.")
          return render_template("user.html",user_data=user_data)
        '''

        

        return render_template('dashboard.html', user_data =user_data)# product_data = product_data,service_data=service_data,message_data=message_data)





"""
------------------ PASSWORD RECOVERY --------------------

"""


@accounts_bp.route('/forgot', methods=("GET","POST"))
def remindpassword():
    current_time = time.localtime()
    sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)
    if request.method == 'GET':
      return render_template('recover.html')







"""
------------------  UPDATE USER --------------------

"""


@accounts_bp.route('/settings', methods=('GET', 'POST', 'PUT'))
def update_user():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")
        
        if request.method == 'GET':
           user_data = Users.query.filter_by(username = session['current_user']).first()
           id = user_data.id
           bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()


           return render_template('settings.html', user_data=user_data,bid_data = bids)


        user_data = Users.query.filter_by(username = session['current_user']).first()


        #update user location

        #latlon = request.form('latlon')
        #user_data.latlon = latlon
        #db.session.add(user_data)
        #db.session.commit()      
        #variable diclaration and definations
        data= request.form
        user_id = user_data.id
        
        email = data.get('email')
        username = data.get('username')
        contact = data.get('contact')
        
        last_seen =sasa
        registered_on =sasa

        x = session['current_user'] #get_jwt_identity()

        #check contact length and usage
        if contact:
            if len(contact) <10 and len(contact) >13:
                flash(" contact {{}} is invalid !".format(contact))
                user_data = Users.query.filter_by(username = session['current_user']).first()
                id = user_data.id
                bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()

                return render_template('settings.html', user_data=user_data,bid_data = bids)      

            



        if Users.query.filter(and_(Users.contact ==contact,Users.status==0)).first() is not None:
            user_ =Users.query.filter(and_(Users.contact ==contact, Users.status==0)).first()
            if user_.username != session["current_user"]:
               flash("contact {{}} is registered by {{}}!".format(contact,user_.username))
               user_data = Users.query.filter_by(username = session['current_user']).first()
               id = user_data.id
               bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()

               return render_template('settings.html', user_data =user_data, bid_data = bids)

               

        #check email for correctness and usage,
        if  Users.query.filter(and_(Users.email == email,Users.status ==0)).first() is not  None:
            user_=Users.query.filter(and_(Users.email == email, Users.status==0)).first()
       
            flash("email {{}} is registered to {{}}.".format(email,user_.username))
            user_data = Users.query.filter_by(username = session['current_user']).first()
            id = user_data.id
            bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()

            return render_template('settings.html', user_data =user_data, bid_data=	bids)
  
        
        regex = '^.+@[^\.].*\.[a-z]{2,}$'
        if email and (re.search(regex,data['email'])):
           email = email
        else:
            if email:
                flash("email {{}} is invalid!".format(email))
                
                user_data = Users.query.filter_by(username = session['current_user']).first()
                id = user_data.id
                bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()
                return render_template('settings.html', user_data =user_data)

              

        #  maintain values
        user_=Users.query.filter(and_(Users.email == email,Users.status ==0)).first()
        _user = Users.query.filter_by(status = 0).all()
  
        existing_emails = []
        existing_contacts = []
        original_email =[]  
        original_contact =[]
        if user_data.username == session['current_user']: 
                existing_emails.append(user_data.email)
                existing_contacts.append(user_data.contact) 
        if user_data.username == session["current_user"]:
                original_email =user_data.email 
                original_username =user_data.username
                original_contact =user_data.contact

        #preserve unchanged fileds
        if not email:
           email =user_data.email
        if not contact:
           contact = user_data.contact
       
        if not username:
          username =user_data.username

        

        #check who is saving
        if user_data.username != session["current_user"]:
            flash("you are not allowed to edit this data")
            user_data = Users.query.filter_by(username = session['current_user']).first()
            id = user_data.id
            bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()
            return render_template('settings.html', user_data =user_data)

          

        
       
        # update user_dat 
        try:
          user_data.email = email
          user_data.contact = contact
          user_data.username = username
          user_data.last_seen = sasa
          db.session.commit()
          session["current_user"] = user_data.username

        #handle error and retain pre edit data (rollback)
        except exc.IntegrityError as e :
            db.session.rollback()
      
        user_data = Users.query.filter_by(username = session['current_user']).first()
        id = user_data.id
        bids = Bids.query.filter(and_(Bids.author_id == id, Bids.status == 0 )).all()
        return render_template('settings.html', user_data =user_data)
        



"""
------------------  PROFILE PHOTO --------------------

""" 


@accounts_bp.route('/profile_upload',  methods=('GET', 'POST'))

def upload_prof_pic():
    """
    uploads profile picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindlg login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    user_data = Users.query.filter_by(username =username).first()
    
    if request.method == 'POST':
        id = user_data.id
    
        if not request.files["file"]:
            flash(" no file seldcted for upload. ")
            return render_template('settings.html', user_data =user_data)

            
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/images/personal/profile/'+str(user_data.id)+"/", f_name))
        if  not request.files["file"]:
           user_data.image_url=old_image
        if request.files["file"]:
           user_data.image_url = ('static/images/personal/profile/'+str(user_data.id)+"/"+f_name)
        db.session.commit()
 
    user_data =Users.query.filter_by(username=session["current_user"]).first()
    

    return render_template('settings.html',user_data =user_data)





"""
------------------  REQUEST SERVICE --------------------

"""


@accounts_bp.route('/service_request', methods=('GET', 'POST'))

def request_data():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")

       


        if request.method == 'POST':
	        timestamp = sasa  
	        data = request.form
	        
	        destination = data.get("destination")
	        author_id =  session["current_user"]
	        budget =  data.get("budget")
	        details =  data.get("details")
	       

	        #verify data
	        #existing_requests = Bids.query.filter_by(status = 0).all()
	        user_data = Users.query.filter_by(username = session['current_user']).first()

	        request_data = Bids.query.filter(and_(Bids.author_id == user_data.id ,Bids.details == details, Bids.status == 0)).first()

	        if request_data :
	        	flash(" request is aleady posted and active")
	        	return render_template('dashboard.html', user_data =user_data)

	        f = Bids(
                destination = data.get("destination"),
                author_id =  user_data.id,
                budget =  data.get("budget"),
                details =  data.get("details"),
                requesttime = sasa,
                status = 0,
                request_views = 0,
                quantity = data.get('quantity'),
                origin = data.get('origin')
            )

	        if not request_data :
	        	db.session.add(f)
	        	db.session.commit()
	        user_data = Users.query.filter_by(username = session['current_user']).first()
	        id = user_data.id
	        existing_requests = Bids.query.filter(and_(Bids.author_id == id ,Bids.status == 0)).all()
	        print(existing_requests)
	        return render_template('dashboard.html',user_data =user_data, bid_data=existing_requests)
        return render_template('dashboard.html',user_data =user_data, bid_data=existing_requests)

      
 

"""
------------------  UNFOLLOW  --------------------

""" 


@accounts_bp.route('/messages', methods=('GET', 'POST'))

def messages():
    if "logged_in" not in session:
        return render_template('login.html')
    #deffinations
    user_=Users.query.filter_(and_(Users.username == session["current_user"],Users.status ==0)).first()
    sender =user_.id 
    recipient = request.form["recipient"]
    content = request.form["content"]
    db.session.add(msg)
    db.session.commit()





"""
------------------  UNFOLLOW  --------------------

""" 


@accounts_bp.route('/unfollow', methods=('GET', 'POST'))

def unfollow():
    if "logged_in" not in session:
        return render_template('login.html')
    #deffinations
    user_=Users.query.filter_(and_(Users.username == session["current_user"],Users.status ==0)).first()
    unfollower =user_.id 
    followed = request.form["followed_id"]
    
    f= Follows.query.filter(and_(Follows.follower_id == unfollower,Follows.followed_id==followed)).first()
    db.session.delete(f)
    db.session.commit()

     
"""
--------------------------- GET FOLLOWERS  ------------------

"""


@accounts_bp.route('/get_followers',methods=('GET','POST'))

def get_followers():
   if "logged_in" not in session:
      return render_template("login.html")
   count =0
   followed_id = request.form["followed_id"]
   followed_ = Users.query.filter(and_(Users.username == session["current_user"], Users.status ==0)).first()
   f=Follows.query.filter_by(followed_id = followed_id).all()
   for i in f:
    count=count+1
    follower_id = i.follower_id
    f_user= Users.query.filter(and_(Users.id == follower_id, Users.status ==0)).first()
    product_data = products.query.filter_by(status = 0).all()         
    user_data = Users.query.filter_by(username = session["current_user"]).first()

    product_data = products.query.filter_by(status =0).all()
    service_data =services.query.filter_by(status =0).all()
    message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()


    if not  product_data:
      return render_template("user.html",user_data=user_data, service_data=service_data,message_data=message_data)

    if not  service_data:
      return render_template("user.html",user_data=user_data,product_data=product_data,message_data=message_data)

    if not  product_data or service_data or message_data:
      flash("there are no products/services yet.")
      return render_template("user.html",user_data=user_data)


    

   return render_template('user.html',users_=users_, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

   

"""
---------------------------- GET FOLLOWING ----------------------
"""



@accounts_bp.route('/following',methods =("GET","POST") )
def get_following():
    if "logged_in" not in session:
       return render_template("login.html")
    user_= Users.query.filter_by(username = session["current_user"]).first()
    following = Follows.query.filter_by(follower_id =user_.id).all()
    count=0
    for f in following:
       count=count+1
       followed = f.followed_id
       f_user = Users.query.filter_by(id=followed_id).first()
       
       user_data = Users.query.filter_by(id = user_.id).first()
       product_data = products.query.filter_by(status =0).all()
       service_data =services.query.filter_by(status =0).all()
       message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()


       if not  product_data:
          return render_template("user.html",user_data=user_data, service_data=service_data,message_data=message_data)

       if not  service_data:
          return render_template("user.html",user_data=user_data,product_data=product_data,message_data=message_data)

       if not  product_data or service_data or message_data:
          flash("there are no products/services yet.")
          return render_template("user.html",user_data=user_data)


        

    return render_template('user.html',users_=users_, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)

    


"""

------------------------------ ALL  USER DATA --------------------

"""


@accounts_bp.route("/all_users", methods =("GET","POST"))
def all_users():
    if "logged_in" not in session:
        return render_template("login.html")
    user_data = Users.query.filter_by(status = 0).all()
    for user in users:
       followers = Follows.query.filter_by(followed_id = user.id).count()
       following = Follows.query.filter_by(follower_id = user.id).count()
       product_data = products.query.filter_by(status =0).all()
       service_data =services.query.filter_by(status =0).all()
       message_data = messages.query.filter(and_(messages.recipient == session["current_user"], messages.status == 0)).first()


       if not  product_data:
          return render_template("user.html",user_data=user_data, service_data=service_data,message_data=message_data)

       if not  service_data:
          return render_template("user.html",user_data=user_data,product_data=product_data,message_data=message_data)

       if not  product_data or service_data or message_data:
          flash("there are no products/services yet.")
          return render_template("user.html",user_data=user_data)


        

    return render_template('user.html',users_=users_, user_data =user_data, product_data = product_data,service_data=service_data,message_data=message_data)


"""
------------------  GET USER --------------------

"""    

@accounts_bp.route('/prod', methods=('GET', 'POST'))

def prod():
   
    return render_template("product_list.html")
    
"""
------------------  GET USER --------------------

"""    

@accounts_bp.route('/get_user', methods=('GET', 'POST'))

def get_user():
    if "logged_in" not in session:
        return render_template("login.html")
    user_data =Users.query.filter_by(username= request.form["username"]).first()
    return render_template("user.html",user_data=user_data)
    
   

"""
------------------  PRODUCT-LIST --------------------

""" 
@accounts_bp.route('/product_list',methods = ["POST","GET"])  
def product_list():
    if "logged_in"  not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

   
    username =session["current_user"]
    user_data =Users.query.filter_by(username= username).first()
    business_data = Business.query.filter_by(owner = user_data.username).first()

    
    # create product  photo directory
    UPLOAD_ = '/home/pato/myblock-01/api/static/media/business/products/'
    os.chdir(UPLOAD_)
    dest = business_data.id
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
        author_id = business_data.id
        product_title= data.get('product_name')
        product_description = data.get('product_description')
        product_category = data.get('product_category')
        price = data.get('product_cost')
        status = 0
        timestamp =sasa

        product_data = db.session.query(Products).filter(and_(Products.product_title == product_title, Products.price ==price, Products.status ==0, Products.author_id ==author_id)).first()
        if product_data:
          flash(" Product exists in active state, No need to repost!")
          return render_template("dashboard.html", user_data=user_data)

          
         
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
        business_data = Business.query.filter_by(owner = user_data.username).first()


        id = business_data.id
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
               file.save(os.path.join('/home/pato/myblock-01/api/static/media/business/products/'+str(business_data.id)+"/", f_name))
               image_url= ('static/media/business/products/'+str(business_data.id)+"/"+f_name)
              
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
        products = db.session.query(Products).filter(and_(Products.product_title == product_title, Products.price ==price)).first()  
        product_data = Products.query.filter_by(author_id = user_data.id).all()   
        business_data = Business.query.filter_by(owner = user_data.username).first()
        #return render_template("shop-detail.html", user_data=user_data, product=products, product_data=product_data, business_data = business_data) 

      
    return render_template("dashboard.html", user_data=user_data, product=products, product_data=product_data, business_data = business_data) 












































"""
------------------  DEACTIVATE USER --------------------

"""  

@accounts_bp.route('/deactivate', methods=( 'GET','POST'))
#@jwt_required
def delete_account():
    """
      change the status code of the account to 1 to avoid future selections
      the account is deemed inactive

    """
    if "logged_in" not  in session:
        flash("your session has expired. kindly log in")
        return render_template("login.html")

    #deffinations
    username =  session["current_user"]
    user = Users.query.filter(and_(Users.username == username, users.status ==0)).first()
  
    business_data = business.query.filter(and_(business.owner == user.username, business.status == 0)).first()

    if business_data:
        #change account status to 1 for deleted accounts
        business_data.status =1
        db.session.commit()

    #reject attempt if not account owner
    if  user:
        user.status= 1
        db.session.commit()
        
        #respond
        flash("Account deactivated. we hate to see you go") 
        return render_template("index.html")


######################################################## search ##############################################################
"""
preping database for keyword search
alter table jobs add fulltext(job_body,job_post_category)
alter table posts add fulltext(body,post_category)
alter table story add fulltext(body,story_category)


"""

@accounts_bp.route('/api/v1/search',  methods=('GET', 'POST'))
#@jwt_required
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

"""
------------------   GET NOTIFICATIONS --------------------

""" 
@accounts_bp.route('/api/v1/all_notifications',  methods=('GET', 'POST'))
#@jwt_required
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
#@jwt_required
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
#@jwt_required
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
#@jwt_required
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



