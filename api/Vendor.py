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

Vendor_bp = Blueprint('Vendor', __name__)
conn = create_engine('mysql+pymysql://root:sword@localhost/MyBlock')







"""
------------------  PRODUCTS--------------------

""" 
@Vendor_bp.route('/products',methods = ["POST","GET"])  
def products():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
       business_data = Business.query.filter_by(owner = user_data.username).first()
       product_data = Products.query.filter_by(status = 0).all()
      
       return render_template("products.html", user_data=user_data, product_data=product_data, business_data=business_data)



"""
------------------ GET PRODUCTS--------------------

""" 
@Vendor_bp.route('/product_data',methods = ["GET","POST"])  
def get_product():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")
    
    if request.method =="POST":
        featured_product = []
        data= request.form
        product_id = data.get('product_id')
        user_data = Users.query.filter_by(username=session["current_user"]).first()
        products = Products.query.filter_by(id = product_id).first()
        product_data = Products.query.filter_by(author_id = user_data.id).all() 
        business_data = Business.query.filter_by(owner = user_data.username).first()   
        featured_ = Products.query.filter(and_(Products.product_category == products.product_category, Products.id != products.id, Products.status == 0 )).all() 
        for f in featured_:
            if f not in featured_product:
                featured_product.append(f)


        return render_template("shop-detail.html", user_data=user_data, product=products, product_data=product_data, featured_product=featured_product,business_data=business_data ) 
     


"""
------------------PRODUCT UPDATE-------------------

""" 




@Vendor_bp.route("/checkout", methods=('GET', 'POST'))
def checkout():
   
      
 
        data =request.form
        item_id = data.get("item_id")
        quantity = data.get("quantity")

        
        product_data = Products.query.filter_by(id = item_id).first()
        user_data = Users.query.filter_by(username = session['current_user']).first()

        item_name= product_data.product_title   
        item_cost = product_data.price    
        timestamp = sasa,
        author_id = user_data.id
        image_url = product_data.image_url

        total0 = float(quantity) * float((int(item_cost)))
        Total = total0
       
        new_buy = Cart(
              item_id =item_id,
              quantity =quantity,
              item_name =item_name,
              item_cost = item_cost,
              timestamp= timestamp,
              Total = Total,
              image_url = image_url,
              author_id = author_id

            )
        bought =Cart.query.filter(and_(Cart.quantity == quantity, Cart.author_id == author_id, Cart.image_url ==image_url)).first()
       
        if bought:

            user_data = Users.query.filter_by(username = session['current_user']).first()
            cart_data = Cart.query.filter_by(author_id = user_data.id).all()
            #flash("Ops Something went wrong!")
            return render_template('cart.html', user_data=user_data, cart_data=cart_data)

        if not bought:
            db.session.add(new_buy)
            db.session.commit() 
            user_data = Users.query.filter_by(username = session['current_user']).first()
 
            cart_data = Cart.query.filter_by(author_id = user_data.id).all()
            return render_template('cart.html', user_data=user_data, cart_data=cart_data)



      
           
        
    
"""


------------------ remove from cart -------------


"""
@Vendor_bp.route('/cart_update',methods = ["POST","GET"])
def delete_entry():

    if "logged_in"  not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")


    if request.method =="POST":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
       business_data = Business.query.filter_by(owner = user_data.id).first()
       cart_data = Cart.query.filter_by(author_id = user_data.id).all()
       
       data = request.form
       item = data.get("item_id")
    cart_entry = Cart.query.filter(and_(Cart.id == item, Cart.author_id == user_data.id)).first()
    if cart_entry: 
    
       try:
          db.session.delete(cart_entry)
          db.session.commit()
          #flash(" Cart updated successfully !")
          cart_data = Cart.query.filter_by(author_id = user_data.id).all()
          return render_template('cart.html', cart_data=cart_data)  

       except Exception as e:
           db.session.rollback()
           flash("Opperation failed. Kindly retry!")
           cart_data = Cart.query.filter_by(author_id = user_data.id).all()
           return render_template('cart.html', cart_data=cart_data)  

    cart_data = Cart.query.filter_by(author_id = user_data.id).all()
    return render_template('cart.html', cart_data=cart_data)

       
   
"""
------------------ payment --------------------

""" 
@Vendor_bp.route('/payment',methods = ["POST","GET"])  
def malipo():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
       cart_data = Cart.query.filter_by(author_id = user_data.id).all()
       product = Products.query.filter_by(status= 0).all() 
       business_data = Business.query.filter_by(owner = user_data.username).first()

       return render_template('payment.html',user_data=user_data,featured_product=cart_data, business_data =business_data) 
      


    #get cart total payable ammount
    #schedule payment api call que
    #report
     




"""
------------------  PRODUCT-LIST --------------------

""" 
@Vendor_bp.route('/product_list',methods = ["POST","GET"])  
def product_list():
    if "logged_in"  not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
       if Business.query.filter_by(owner = user_data.username).first() is None:
          
          user_data = Users.query.filter_by(username=session["current_user"]).first()  
          business_data = Business.query.filter_by(owner = user_data.username).first()
          product_data = Products.query.filter_by(status = 0).all()
          flash(" Register your business to showcase products !")
          return render_template('business.html', user_data=user_data,business_data=business_data, product_data=product_data)     
       
       return render_template("product_list.html", user_data=user_data)

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
          return render_template("product_list.html", user_data=user_data)

          
         
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
    return render_template("shop-detail.html", user_data=user_data, product=products, product_data=product_data, business_data = business_data) 




"""
------------------  PRODUCT update --------------------

""" 
@Vendor_bp.route('/product_update',methods = ["POST","GET"])  
def product_update():
    if "logged_in"  not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first() 
       data = request.form
       product_id = data["product_id"] 

       product_data = Products.query.filter_by(id = product_id).first()
       business_data = Business.query.filter_by(owner = user_data.username).first()       
       return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data)     
       

    
    
    if request.method == 'POST':
          
        #get  userdata
        user_data = Users.query.filter_by(username=session["current_user"]).first() 
        data =request.form
        product_id = data["product_id"] 
        product_data = Products.query.filter_by(id = product_id).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()       
        
        
        
        author_id = business_data.id
        product_title= data.get('product_name')
        product_description = data.get('product_description')
        product_category = data.get('product_category')
        price = data.get('product_cost')
        status = 0
        timestamp =sasa

        product_data = db.session.query(Products).filter(and_(Products.id == product_id, Products.status ==0)).first()
    
        original_title = product_data.product_title
        original_description = product_data.product_description
        original_category = product_data.product_category
        original_price = product_data.price

        if not product_title:
            product_title = original_title

        if not product_description:
           product_description = original_description

        if product_category == "Choose...":
           product_category = original_category

        if product_category == "None":
           product_category = original_category

        if not product_category :
           product_category = original_category

        if not price:
          price = original_price

       
        product_data.product_title = product_title,
        product_data.product_description = product_description,
        product_data.author_id = author_id,            
        product_data.product_category = product_category,
        product_data.price = price,
        product_data.status = 0,
        product_data.timestamp = sasa

        try:
            print(product_category)
            db.session.commit()
            user_data = Users.query.filter_by(username=session["current_user"]).first() 
            data =request.form
            product_id = data["product_id"] 
            product_data = Products.query.filter_by(id = product_id).first()
            business_data = Business.query.filter_by(owner = user_data.username).first()       
            return render_template('product_update.html', user_data=user_data,business_data=business_data, product=product_data) 

        except Exception as e:
            db.session.rollback()
            user_data = Users.query.filter_by(username=session["current_user"]).first() 
            data =request.form
            product_id = data["product_id"] 
            product_data = Products.query.filter_by(id = product_id).first()
            business_data = Business.query.filter_by(owner = user_data.username).first()       
            return render_template('product_update.html', user_data=user_data,business_data=business_data, product=product_data)  

        product_data = db.session.query(Products).filter(and_(Products.product_title == product_title, Products.price ==price, Products.status==0)).first()
        username =session["current_user"]
        user_data =Users.query.filter_by(username= username).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()


        
    return render_template("shop-detail.html", user_data=user_data, product=product_data, business_data = business_data) 


"""
------------------  SERVICES--------------------

""" 
@Vendor_bp.route('/services',methods = ["POST","GET"])  
def services():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="GET":
       user_data = Users.query.filter_by(username=session["current_user"]).first()  
      
       return render_template("services.html", user_data=user_data)


"""
------------------ Delete product -------------------

""" 
@Vendor_bp.route('/remove_products',methods = ["POST","GET"])  
def remove_product():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

    if request.method =="POST":
      data= request.form
      product_id = data['product_id']
      product_data = Products.query.filter_by(id=product_id).first()

      product_data.status = 1
       
      try:
       db.session.commit()
       user_data = Users.query.filter_by(username=session["current_user"]).first() 
       business = Business.query.filter_by(owner = user_data.username).first() 
       product_data = Products.query.filter(and_(Products.status ==0,Products.author_id ==business.id)).all()

       categories = []
       
       for product in product_data:
          if product.product_category not in categories:
             categories.append(product.product_category)
      
       return render_template("dashboard.html", user_data=user_data, product_data=product_data, business=business,categories=categories)

      except Exception as e:
        user_data = Users.query.filter_by(username=session["current_user"]).first() 
        business = Business.query.filter_by(owner = user_data.username).first() 
        product_data = Products.query.filter(and_(Products.status ==0, Products.author_id ==business.id)).all()

        categories = []
       
        for product in product_data:
          if product.product_category not in categories:
             categories.append(product.product_category)
        flash('something went wrong! kindly retry.')      
        return render_template("dashboard.html", user_data=user_data, product_data=product_data, business=business,categories=categories)






"""
------------------  events--------------------

""" 
@Vendor_bp.route('/update_image',methods = ["POST","GET"])  
def image_updates():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

 
    data =request.form
    id = data['product_id']
    url = data['url']
    user_data = Users.query.filter_by(username=session["current_user"]).first() 
    product_data = Products.query.filter_by(id = id).first()
    business_data = Business.query.filter_by(owner = user_data.username).first() 

    if not request.files["file"]:
        product_id = data["product_id"]
        user_data = Users.query.filter_by(username=session["current_user"]).first() 
        product_data = Products.query.filter_by(id = product_id).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()    
        flash("click on the image to update then save the selected file.")   
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
    
    
      
    product_data = Products.query.filter_by(id = id).first() 
    
    if url == "image_url":
     
      file = request.files["file"]

      if file.filename != '':
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/media/business/products/'+str(business_data.id)+"/", f_name))
        image_urld= ('static/media/business/products/'+str(business_data.id)+"/"+f_name)
      product_data.image_url = image_urld 
      try:
       db.session.commit()
       return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
      except Exception as e:
        flash('something went wrong. please retry!')
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 



@Vendor_bp.route('/update_image1',methods = ["POST","GET"])  
def image_updates1():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

 
    data =request.form
    id = data['product_id']
    url = data['url']
    user_data = Users.query.filter_by(username=session["current_user"]).first() 
    product_data = Products.query.filter_by(id = id).first()
    business_data = Business.query.filter_by(owner = user_data.username).first() 

    if not request.files["file1"]:
        product_id = data["product_id"]
        user_data = Users.query.filter_by(username=session["current_user"]).first() 
        product_data = Products.query.filter_by(id = product_id).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()    
        flash("click on the image to update then save the selected file.")   
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
    
    
      
    product_data = Products.query.filter_by(id = id).first() 
    
    if url == "image_url1":
     
      file = request.files["file1"]

      if file.filename != '':
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/media/business/products/'+str(business_data.id)+"/", f_name))
        image_urld= ('static/media/business/products/'+str(business_data.id)+"/"+f_name)
      product_data.image_url1 = image_urld 
      try:
       db.session.commit()
       return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
      except Exception as e:
        flash('something went wrong. please retry!')
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 

 

@Vendor_bp.route('/update_image2',methods = ["POST","GET"])  
def image_updates2():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

 
    data =request.form
    id = data['product_id']
    url = data['url']
    user_data = Users.query.filter_by(username=session["current_user"]).first() 
    product_data = Products.query.filter_by(id = id).first()
    business_data = Business.query.filter_by(owner = user_data.username).first() 

    if not request.files["file2"]:
        product_id = data["product_id"]
        user_data = Users.query.filter_by(username=session["current_user"]).first() 
        product_data = Products.query.filter_by(id = product_id).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()    
        flash("click on the image to update then save the selected file.")   
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
    
    
      
    product_data = Products.query.filter_by(id = id).first() 
    
    if url == "image_url2":
     
      file = request.files["file2"]

      if file.filename != '':
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/media/business/products/'+str(business_data.id)+"/", f_name))
        image_urld= ('static/media/business/products/'+str(business_data.id)+"/"+f_name)
      product_data.image_url2 = image_urld 
      try:
       db.session.commit()
       return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
      except Exception as e:
        flash('something went wrong. please retry!')
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 


  


@Vendor_bp.route('/update_image3',methods = ["POST","GET"])  
def image_updates3():
    if "logged_in" not in session:
      flash("your session has expired! kindly login")
      return render_template("login.html")

 
    data =request.form
    id = data['product_id']
    url = data['url']
    user_data = Users.query.filter_by(username=session["current_user"]).first() 
    product_data = Products.query.filter_by(id = id).first()
    business_data = Business.query.filter_by(owner = user_data.username).first() 

    if not request.files["file3"]:
        product_id = data["product_id"]
        user_data = Users.query.filter_by(username=session["current_user"]).first() 
        product_data = Products.query.filter_by(id = product_id).first()
        business_data = Business.query.filter_by(owner = user_data.username).first()    
        flash("click on the image to update then save the selected file.")   
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
    
    
      
    product_data = Products.query.filter_by(id = id).first() 
    
    if url == "image_url3":
     
      file = request.files["file3"]

      if file.filename != '':
        extension = os.path.splitext(file.filename)[1]
        f_name = str(uuid.uuid4()) + extension
        file.save(os.path.join('/home/pato/myblock-01/api/static/media/business/products/'+str(business_data.id)+"/", f_name))
        image_urld= ('static/media/business/products/'+str(business_data.id)+"/"+f_name)
      product_data.image_url3 = image_urld 
      try:
       db.session.commit()
       return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
      except Exception as e:
        flash('something went wrong. please retry!')
        return render_template('product_update.html', user_data=user_data, business_data=business_data, product=product_data) 
