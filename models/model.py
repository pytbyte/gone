
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
    








################################## businesss ###################################
#businesss Registration
class business_status:
    active:0
    deleted: 1
    blocked: 2

class Business( db.Model, UserMixin):
    """ 
    business Model for storing business related details 
    """
  
    
    __tablename__ = "business"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    businessname = db.Column(db.VARCHAR(200), unique=True)
    businessemail = db.Column(db.VARCHAR(200), unique=True, nullable=False)
    businesscontact = db.Column(db.VARCHAR(200), unique=True)
    
    authenticated = db.Column(db.Boolean, default=False) 
    businesscategory = db.Column(db.VARCHAR(200))
    businesslocation = db.Column(db.VARCHAR(200))
    businesswhatsapp = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    last_seen  = db.Column(db.VARCHAR(200))
    owner  = db.Column(db.VARCHAR(200))
    logo_url = db.Column(db.VARCHAR(200), nullable=True)
    status = db.Column(db.Integer, default=0)
    businessdsc = db.Column(db.VARCHAR(500))
    admin = db.Column(db.Boolean, nullable=True, default=0)
    
    is_active = db.Column(db.Boolean, default=False)
    """
    products = db.relationship('products', backref='author', lazy='dynamic', cascade="all, delete-orphan")
    followed = db.relationship('Follows',
                               foreign_keys=[Follows.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follows',
                                foreign_keys=[Follows.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',    
                                cascade='all, delete-orphan')

    comments = db.relationship('Comments', backref='author', lazy='dynamic',cascade="all, delete-orphan")
    """
    def is_active(self):
        """True, as all businesss are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

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
        if  not self.logo_url :
            logo_url =  ('static/images/default/default.jpg')
        elif  self.logo_url:
            logo_url =self.logo_url
        json_business = {  
            'logo': logo_url,
            'businessname':self.businessname,
            'businessemail':self.businessemail,
            'businessscontact':self.businesscontact,
            'businessswatsapp':self.businesswhatsapp,
            'businessstype':self.businesstype,
            'businessscategory':self.businesscategory,
            'businessid':self.id,
            'registered_on': self.registered_on,
            'last_seen': self.last_seen,
            #'followers':self.followers.count(),
            #'following': self.followed.count(),
            'business_profile': url_for('business.get_business',businessname = self.businessname),
            
            }

        return jsonify(json_business)
   



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

#messages




################################## users ###################################
#users Registration
class user_status:
    active:0
    deleted: 1
    blocked: 2

class Users( db.Model, UserMixin):
    """ 
    user Model for storing user related details 
    """
  
    
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.VARCHAR(200), unique=True)
    email = db.Column(db.VARCHAR(200), unique=True)
    contact = db.Column(db.VARCHAR(200), unique=True)
    whatsapp = db.Column(db.VARCHAR(200), unique=True)
    bio = db.Column(db.VARCHAR(200))
    name = db.Column(db.VARCHAR(200))
    authenticated = db.Column(db.Boolean, default=False) 
    password_hash = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    last_seen  = db.Column(db.VARCHAR(200))
    interests = db.Column(db.String(300))
    image_url = db.Column(db.VARCHAR(200), nullable=True)
    status = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, nullable=True, default=0)
    device_id = db.Column(db.VARCHAR(300), unique = True)
    is_active = db.Column(db.Boolean, default=False)
    latlon = db.Column(db.String(300))
    followed = db.relationship('Follows',
                               foreign_keys=[Follows.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follows',
                                foreign_keys=[Follows.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',    
                                cascade='all, delete-orphan')

    comments = db.relationship('Comments', backref='author', lazy='dynamic',cascade="all, delete-orphan")
    
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated 

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def load_user(id):
        return users(id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)






     
    def to_json(self):
        if  not self.image_url :
            image_url =  ('static/images/default/default.jpg')
        elif  self.image_url:
             image_url =self.image_url
        json_user = {  
            'profile_image': image_url,
            'username':self.username,
            'email':self.email,
            'contact':self.contact,
            'user_id':self.id,
            'registered_on': self.registered_on,
            'last_seen': self.last_seen,
            'followers':self.followers.count(),
            'following': self.followed.count(), 
            'user_profile': url_for('accounts.get_user',user_id = self.id),
            'authenticated':self.authenticated,
            'status': 200
            }

        return jsonify(json_user)
    def to_intro(self):
        if not self.image_url:
             self.image_url =  ('static/images/default/default.jpg')
        elif self.image_url :
             image_url =self.image_url
        data_ ={   "image_url" : self.image_url,
                   "username":self.username,
                   "user_profile" :url_for('accounts.get_user',user_id=self.id),
                   "registered_on":self.registered_on, 
                    "user_id":self.id
                   }
        return data_



################################# comments ###########################################################


class comment_status:
    Active: 0
    deleted: 1
    updated : 2
    
class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.VARCHAR(200))
    timestamp= db.Column(db.VARCHAR(200))
    disabled = db.Column(db.Boolean, default=0)
    status= db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
   
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))    
    service_body = db.Column(db.VARCHAR(300))
   
    def to_json(self):
        comm = Users.query.filter_by(id = self.author_id).first()
        commenter = comm.username
        product_data = products.query.filter_by(id =self.product_id).first()
        user_data = Users.query.filter_by(id = self.author_id).first()
        if self.status == 0:
                json_comment = {
                    'product_url': url_for('products.get_product', product_id=self.product_id),
                    'comment_body': self.body,
                    'timestamp': self.timestamp,
                    'author_url': url_for('accounts.get_user', id=self.author_id),
                    'comment_id': self.id,
                    'comment_url': url_for('products.get_comment', comment_id=self.id),
                    'product_author_id': product_data.author_id,
                    'commenter': commenter,
                    'user_id':self.author_id,
                    'product_id':self.product_id,
                    'comment_author_image': user_data.image_url,
                    'status':200
                 }
            
                return json_comment


    def service_json(self):
        comm = Users.query.filter_by(id = self.author_id).first()
        commen = comm.username

        service_j ={
                          "status":200,
                          "service_url":url_for('services.get_service', service_id=self.service_id),
                          "comment_body":self.body,
                          "service_id":self.service_id,
                          "author_id" :self.author_id,
                          "comment_id" : self.id,
                          "timestamp": self.timestamp,
                          "user_id": self.author_id,
                          "author_url": url_for('accounts.get_user', id=self.author_id),
                          'user_id':self.author_id,
                          'author_image': comm.image_url,
                          'service_comment_url': url_for('services.single_service_comment', comment_id=self.id)
                          }
        return service_j


        if self.status ==1:
            return jsonify("this comment doesn't exist")

  


class flags_(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.VARCHAR(100))
    product_id = db.Column(db.VARCHAR(100))
    
   
    def to_json(self):
        json_flag = {
            'product_id': self.product_id,
            'user_id' : self.user,
            'flag_id': self.id,
            'product_url': url_for('products.get_product', product_id=self.product_id),
            'user_url': url_for('accounts.get_user', user_id=self.user),
            'status':200
        }
        return json_flag

#################################### PRODUCT ###################################################


class Products(db.Model):
   
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.VARCHAR(200))
    product_description = db.Column(db.VARCHAR(200))
    product_category = db.Column(db.VARCHAR(200))
    price = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    timestamp =db.Column(db.VARCHAR(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    share = db.Column(db.Integer, db.ForeignKey('share.id'))
    views =db.Column(db.VARCHAR(200))

    image_url = db.Column(db.VARCHAR(200))
    image_url1 = db.Column(db.VARCHAR(200))
    image_url2 = db.Column(db.VARCHAR(200)) 
    image_url3 = db.Column(db.VARCHAR(200))
    image_url4 = db.Column(db.VARCHAR(200))


    
    
################################### services ########################################################
class services(db.Model):
   
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    service_title = db.Column(db.VARCHAR(200))
    service_description = db.Column(db.VARCHAR(200))
    service_category = db.Column(db.VARCHAR(200))
    price = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    timestamp =db.Column(db.VARCHAR(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    share = db.Column(db.Integer, db.ForeignKey('share.id'))
    service_views =db.Column(db.VARCHAR(200))
    
    image_url = db.Column(db.VARCHAR(200))
    image_url1 = db.Column(db.VARCHAR(200))
    image_url2 = db.Column(db.VARCHAR(200)) 
    image_url3 = db.Column(db.VARCHAR(200))
    image_url4 = db.Column(db.VARCHAR(200))
    
    
    
################################### events ########################################################
class events(db.Model):
   
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event_title = db.Column(db.VARCHAR(200))
    event_venue= db.Column(db.VARCHAR(200))
    event_date= db.Column(db.VARCHAR(200))
    event_time = db.Column(db.VARCHAR(200))
    event_description = db.Column(db.VARCHAR(200))
    event_category = db.Column(db.VARCHAR(200))
    price = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    timestamp =db.Column(db.VARCHAR(200))
    author_id = db.Column(db.VARCHAR(200))
    share = db.Column(db.VARCHAR(200))
    event_views =db.Column(db.VARCHAR(200))
    
    image_url = db.Column(db.VARCHAR(200))
    image_url1 = db.Column(db.VARCHAR(200))
    image_url2 = db.Column(db.VARCHAR(200)) 
    image_url3 = db.Column(db.VARCHAR(200))
    image_url4 = db.Column(db.VARCHAR(200))




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

    
#################################### interests ##########################################   

class Interests(db.Model):
    __tablename__ = 'interests'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    interest_ = db.Column(db.VARCHAR(200))
    
   
    def to_json(self):
        products = products.query.filter_by(product_category=self.interest_).count()
        services = services.query.filter_by(service_product_category=self.interest_).count()
        json_interests = {
            'interest_id':self.id,
            'interest':self.interest_,
            'products': products,
            'services': services,
            'status':200

        }
        return json_interests


################################# shares ###########################################################

class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
   
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    status = db.Column(db.Integer)

   
   
    def product_json(self):
         
         if self.product_id is not None:
            shared_product =products.query.filter_by(id = self.product_id).first()
            json_share = {
                'share_id':self.id,
                'product_url': url_for('products.get_product',product_id=self.product_id),
                'user_url': url_for('accounts.get_user', user_id=self.user),
                'user_id' :self.user,
                'shared_product' :shared_product.body, 
                'product_image_url': shared_product.product_image_url,
                'product_id' : self.product_id, 
                'status': 200
            }
            return json_share
            
    def service_json(self):
        if self.service_id  is  not None:
            shared_service =services.query.filter_by(id = self.service_id).first()
            json_share = {
                'share_id':self.id,
                'service_url': url_for('services.get_service',service_id=self.service_id),
                'user_url': url_for('accounts.get_user', user_id=self.user),
                'user_id':self.user,
                'shared_service': shared_service.service_body,
                'service_image_url': shared_service.service_image_url,
                'service_id':self.service_id,
                'status': 200
            }
            return json_share


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


