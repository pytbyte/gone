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

business_bp = Blueprint('business', __name__)
conn = create_engine('mysql+pymysql://root:sword@localhost/MyBlock')





@business_bp.route("/business", methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
      user_data = Users.query.filter_by(username = session["current_user"]).first()
      return render_template('business_profile.html', user_data=user_data)


    #variable diclaration and definations  
    data=request.form
    businessname = request.form['business_name'] 
    owner = session["current_user"]
    business_category = request.form['business_category']
    
    businessemail = request.form["email"]
    businesscontact = data['phone']
    businesswhatsapp = data['whatsapp'] 
    businesslocation= data['location']
    businessdsc = data['business_description']
    status = 0,
    admin = 1 ,
    last_seen =sasa
    registered_on =sasa
  
 
    user_data = Users.query.filter_by(username = session["current_user"]).first()
    #check contact length
    if len(businesscontact) < 10 or  len(businesscontact) >13:
        flash(" wrong phone number.Check and try again.")
        return render_template('business_profile.html')    

    #check email for correctness,
    if Business.query.filter_by(businessemail = businessemail).first():
          flash("email address  registered already!")
          return render_template("business_profile.html", user_data=user_data)

    regex= '^.+@[^\.].*\.[a-z]{2,}$'      
    if  (re.search(regex,businessemail)):
        businessemail=businessemail
    else:  
        flash("invalid email address!")
        return  render_template("business_profile.html", user_data=user_data)
    

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
                return render_template('business_profile.html',user_data=user_data) 
         
          
        if  businesscontact in existing_contacts :           
               flash(" contact : {}is  already registered before!".format(businesscontact))          
               return render_template('business_profile.html', user_data=user_data)      


    #user creation
    new_business = Business(
        businessname = request.form['business_name'] ,
        owner = session["current_user"],
        businesscategory = request.form['business_category'],
        businessemail = request.form["email"],
        businesscontact = data['phone'],
        businesswhatsapp = data['whatsapp'],
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
        return render_template('business_profile.html', user_data=user_data)

    #save new user
    if not business_data:
       db.session.add(new_business)
       db.session.commit()
 
    created_business =   Business.query.filter(and_(Business.businessemail ==businessemail , Business.businesscontact == businesscontact ,Business.businessname ==businessname)).first() 
    if created_business.status == 0 :

        dest = created_business.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/all_images/personal/business'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
        return redirect(url_for('accounts.dashboard',user_data=user_data))  








"""
------------------  LOGO PHOTO --------------------

""" 


@business_bp.route('/business_upload',  methods=('GET', 'POST'))

def upload_logo():
    """
    uploads profile picture to session['current_user'].
    """
    if 'logged_in' not in session:
        flash("your session has expired! kindly login")
        return render_template("login.html")
 
    #get current_user
    username = session['current_user']
    business_data = Business.query.filter_by(owner =username).first()

    if business_data.status == 0 :

        dest = business_data.id
       
        UPLOAD_ = '/home/pato/myblock-01/api/static/all_images/business/logo'
        os.chdir(UPLOAD_)
        dest = dest
        UPLOAD_FOLDER =UPLOAD_+str(dest)
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if not os.path.isdir("%s" % dest):
            os.mkdir("%s" % dest)
        



    
    if request.method == 'POST':
        id = business_data.id
    
        if not request.files["file"]:
            flash(" no file selected for upload. ")            
            return render_template("business_profile.html",business_data=business_data)

            
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/all_images/business/logo/'+str(business_data.id)+"/", f_name))
        business_data.image_url = ('static/all_images/business/logo/'+str(business_data.id)+"/"+f_name)
        

        db.session.commit()
 
    business_data = Business.query.filter_by(owner =session["current_user"]).first()
    return render_template('business.html',business_data=business_data)





"""
------------------  UPDATE USER --------------------

"""


@business_bp.route('/update_business', methods=('GET', 'POST'))
def update_business():
        if "logged_in" not in session:
           flash(" your session has expired! kindly login")
           return render_template("login.html")

        business_data = Business.query.filter_by(owner= session['current_user']).first()


        data= request.form
        _businessid = business_data.id
        name= data.get('full_name')
        businessemail = data.get('businessemail')
        businessname= data.get('businessname')
        businesscontact = data.get('businesscontact')
        businesswhatsapp = data.get('businesswhatsapp')
        
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
        existing_businesswhatsapp = []
        existing_businesscontacts = []
        original_businessemail =[]  
        original_businesscontact =[]
        original_businesswhatsapp =[]
     
        if not business_data.businesswhatsapp:
                # update _businessdat 
                business_data.businesswhatsapp = businesswhatsapp
                try:
                    db.session.commit()

                #handle error and retain pre edit data (rollback)
                except exc.IntegrityError as e :
                    db.session.rollback()

               
        if business_data.businessname== session['current_user']: 
                existing_businessemails.append(business_data.businessemail)
                existing_businesscontacts.append(business_data.businesscontact) 
                existing_businesswhatsapp.append(business_data.businesswhatsapp)


        if business_data.businessname== session["current_user"]:
                original_businessemail =business_data.businessemail 
                original_businessname=business_data.businessname
                original_businesscontact =business_data.businesscontact
                original_businesswhatsapp =business_data.businesswhatsapp

        #preserve unchanged fileds
        if not businessemail:
           businessemail =business_data.businessemail
        if not businesscontact:
           businesscontact = business_data.businesscontact
        
        if not businessname:
          businessname=business_data.businessname
        if not businesswhatsapp:
          businesswhatsapp =business_data.businesswhatsapp

        business_data.businessemail = businessemail
        business_data.businesscontact = businesscontact
        business_data.businessname= businessname
        business_data.businesswhatsapp = businesswhatsapp

        #check who is saving
        if business_data.businessname!= session["current_user"]:
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
        return render_template('business.html',business_data=business_data)#, business_data =business_data, product_data = product_data,service_data=service_data,message_data=message_data)

        

