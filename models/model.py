
from flask import current_app as app
from flask import g , Flask, jsonify, url_for
import time
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask_login import UserMixin,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


login_manager = LoginManager()
db = SQLAlchemy()
db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)


#messages


class messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient = db.Column(db.Integer, db.ForeignKey('users.id'))
    image_url = db.Column(db.VARCHAR(200), nullable=True)
    status = db.Column(db.Integer, default=0)
    content = db.Column(db.VARCHAR(2000), nullable=True)
    timestamp = db.Column(db.VARCHAR(200))
    

#################################### PRODUCT ###################################################


class Products(db.Model):
   
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.VARCHAR(200))
    product_description = db.Column(db.VARCHAR(200))
    product_category = db.Column(db.VARCHAR(200))
    image_url = db.Column(db.VARCHAR(200))
    image_url1 = db.Column(db.VARCHAR(200))
    image_url2 = db.Column(db.VARCHAR(200)) 
    image_url3 = db.Column(db.VARCHAR(200))
    image_url4 = db.Column(db.VARCHAR(200))
    price = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    timestamp =db.Column(db.VARCHAR(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))    
    views =db.Column(db.VARCHAR(200))
    







################################## businesss ###################################
#users Registration
class user_status:
    active:0
    deleted: 1
    blocked: 2

class Users( db.Model, UserMixin):
 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.VARCHAR(200), unique=True)
    email = db.Column(db.VARCHAR(200), unique=True, nullable=False)
    contact = db.Column(db.VARCHAR(200), unique=True)    
    authenticated = db.Column(db.Boolean, default=False) 
    password_hash = db.Column(db.VARCHAR(200))
    latlon = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    last_seen  = db.Column(db.VARCHAR(200))
    image_url = db.Column(db.VARCHAR(200), nullable=True)
    status = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=False)
 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        """True, as all businesss are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.contact

    def is_authenticated(self):
        """Return True if the business is authenticated."""
        return self.authenticated 

    def is_anonymous(self):
        """False, as anonymous businesss aren't supported."""
        return False

   

    @login_manager.user_loader
    def get_user(user_id):
        try:
           return Users.query.get(int(id))
        except:
           return None

    

    def to_json(self):
        if  not self.image_url :
            image_url =  ('static/all_images/default/default.jpg')
        elif  self.image_url:
            image_url =self.image_url
        json_user = {  
            'image': image_url,
            'username':self.username,
            'contact':self.contact,
            'id':self.id,
            'registered_on': self.registered_on,
            'last_seen': self.last_seen,
            
            }

        return jsonify(json_user)
   



################################## businesss ###################################
#users Registration
class user_status:
    active:0
    deleted: 1
    blocked: 2

class Business( db.Model, UserMixin):
 
    __tablename__ = "business"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    businessname = db.Column(db.VARCHAR(200), unique=True)
   
    businesscontact = db.Column(db.VARCHAR(200), unique=True)    
    authenticated = db.Column(db.Boolean, default=False) 
    businesscategory = db.Column(db.VARCHAR(200))
    businesslocation = db.Column(db.VARCHAR(200))
    owner = db.Column(db.VARCHAR(200))
    businessdsc = db.Column(db.VARCHAR(200))
    workinghours = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    last_seen  = db.Column(db.VARCHAR(200))
    logo_url = db.Column(db.VARCHAR(200), nullable=True)
    latlng = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
   
 
   
    

    def to_json(self):
        if  not self.love_url :
            logo_url =  ('static/all_images/default/default.jpg')
        elif  self.image_url:
            logo_url =self.logo_url
        json_user = {  
            'logo': logo_url,
            'businessname':self.businessname,
            'businesscontact':self.businesscontact,
            'businesscategory':self.businesscategory,
            'workinghours': self.workinghours,
            'businessdescription':self.businessdescription,
            'latlng': self.latlng,
            'id':self.id,
            'registered_on': self.registered_on,
            'last_seen': self.last_seen,
            
            }

        return jsonify(json_user)
   


"""

################################# folows ###########################################################

class Follows(db.Model):
    __tablename__ = 'follow_ups'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    
    timestamp = db.Column(db.VARCHAR(200))
    
    def to_json(self):
        user = Users.query.filter_by(id =self.followed_id).first()
        response_object ={
        "status": 200,
        "follower_id" : self.follower_id,
        "followed_id" : self.followed_id,
        "message": "you are now following {}".format(user.name)
        }
        return jsonify(response_object)


"""

#################################### BIKES ###################################################


class Bikes(db.Model):
   
    __tablename__ = 'bikes'
    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.VARCHAR(200))
    owner= db.Column(db.VARCHAR(200))
    contact= db.Column(db.VARCHAR(200))
    make = db.Column(db.VARCHAR(200))
    route = db.Column(db.VARCHAR(200))
    last_seen =db.Column(db.VARCHAR(200))
    image_url = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    

    

#################################### TAXIS ###################################################


class Taxis(db.Model):
   
    __tablename__ = 'taxis'
    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.VARCHAR(200))
    owner= db.Column(db.VARCHAR(200))
    contact= db.Column(db.VARCHAR(200))
    make = db.Column(db.VARCHAR(200))
    route = db.Column(db.VARCHAR(200))
    last_seen =db.Column(db.VARCHAR(200))
    image_url = db.Column(db.VARCHAR(200))
    seater = db.Column(db.VARCHAR(200), default=3)
    registered_on = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    

    #################################### TRUCKS ###################################################


class Trucks(db.Model):
   
    __tablename__ = 'trucks'
    id = db.Column(db.Integer, primary_key=True)
    registration_no = db.Column(db.VARCHAR(200))
    owner= db.Column(db.VARCHAR(200))
    contact= db.Column(db.VARCHAR(200))
    make = db.Column(db.VARCHAR(200))
    route = db.Column(db.VARCHAR(200))
    last_seen =db.Column(db.VARCHAR(200))
    image_url = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    






################################### services ########################################################
class Bids(db.Model):
   
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.VARCHAR(200))
    budget = db.Column(db.VARCHAR(200))
    quantity = db.Column(db.VARCHAR(200))
    details = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    origin  =db.Column(db.VARCHAR(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    requesttime =db.Column(db.VARCHAR(200))
    request_views =db.Column(db.VARCHAR(200))


################################# service_bids ###########################################################


class service_bid(db.Model):
    """
     service bid  Model for storing service related details 
        
    """
    __tablename__ = 'service_bid'
    id = db.Column(db.Integer, primary_key=True)
    bid_body = db.Column(db.VARCHAR(200))
    bid_ammount= db.Column(db.VARCHAR(100))
    timestamp = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    author_id = db.Column(db.VARCHAR(200))
    service_id = db.Column(db.VARCHAR(200))



    def to_json(self):
        services_ = services.query.filter_by(id=self.service_id).first()
        json_bid = {
            'service_url': url_for('services.get_service', service_id=self.service_id),
            'service_data': services_.service_body,
            'bid_url': url_for('services.get_bid', bid_id=self.id),
            'bid_body': self.bid_body,           
            'timestamp': self.timestamp,
            'bid_ammount': self.bid_ammount,
            'bid_id' : self.id,
            'bid_author': self.author_id,
            'author_url': url_for('accounts.get_user', id=self.author_id),
            'status' : 200,
        }
        return json_bid

   

################################# Notifications ###########################################################
#drop column status from database

current_time = time.localtime()
sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.VARCHAR(200))
    notified_user = db.Column(db.VARCHAR(200))
    timestamp = db.Column(db.VARCHAR(200), index=True, default=time)
    author = db.Column(db.VARCHAR(200))
    message =db.Column(db.VARCHAR(400))
    data_url = db.Column(db.VARCHAR(200))
    user_data_url = db.Column(db.VARCHAR(200))
    status_code = db.Column(db.VARCHAR(200))
   
    def to_json(self):
         json_note = {
                "status": 200,
                "notification_id" : self.id,
                "message": self.message,
                "author_id" : self.author,
                "timestamp": self.timestamp,
                'data_url' : self.data_url,
                'user_url': url_for('accounts.get_user',user_id =self.user),
                "status_code" : self.status_code
                   }
         return json_note


