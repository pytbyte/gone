from flask import current_app as app
from flask import g , Flask, jsonify, url_for
import time
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()
db.init_app(app)

from flask_login import UserMixin



################################# Notifications ###########################################################
#drop column status from database

current_time = time.localtime()
sasa=time.strftime('%a, %d %b %Y %H:%M:%S GMT', current_time)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.VARCHAR(200))
    user = db.Column(db.VARCHAR(200), db.ForeignKey('users.id'))
    timestamp = db.Column(db.VARCHAR(200), index=True, default=time)
    author = db.Column(db.VARCHAR(200))
    message =db.Column(db.VARCHAR(400))
    data_url = db.Column(db.VARCHAR(200))
    user_data_url = db.Column(db.VARCHAR(200))
    status_code = db.Column(db.VARCHAR(200))
    post_id = db.Column(db.VARCHAR(200))    
    job_id= db.Column(db.VARCHAR(200))
    bid_id = db.Column(db.VARCHAR(200))
    story_id = db.Column(db.VARCHAR(200))
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
    name =db.Column(db.VARCHAR(200))
    username = db.Column(db.VARCHAR(200), unique=True)
    email = db.Column(db.VARCHAR(200), unique=True, nullable=False)
    contact = db.Column(db.VARCHAR(200), unique=True)
    authenticated = db.Column(db.Boolean, default=False) 
    password_hash = db.Column(db.VARCHAR(200))
    registered_on = db.Column(db.VARCHAR(200))
    last_seen  = db.Column(db.VARCHAR(200))
    proffession = db.Column(db.VARCHAR(200))
    bio = db.Column(db.VARCHAR(300))
    interests = db.Column(db.String(300))
    image_url = db.Column(db.VARCHAR(200), nullable=True)
    status = db.Column(db.Integer, default=0)
    admin = db.Column(db.Boolean, nullable=True, default=0)
    device_id = db.Column(db.VARCHAR(300), unique = True)
    is_active = db.Column(db.Boolean, default=False)

    posts = db.relationship('Posts', backref='author', lazy='dynamic', cascade="all, delete-orphan")
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
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated 

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def load_user(id):
        return users(id)

    
    def to_json(self):
        if  not self.image_url :
            image_url =  ('static/images/default/default.jpg')
        elif  self.image_url:
             image_url =self.image_url
        json_user = {  
            'profile_image': image_url,
            'name':self.name,
            'username':self.username,
            'email':self.email,
            'contact':self.contact,
            'proffession': self.proffession,
            'bio': self.bio,
            'user_id':self.id,
            'registered_on': self.registered_on,
            'last_seen': self.last_seen,
            'followers':self.followers.count(),
            'following': self.followed.count(), 
            'posts':self.posts.count(),
            'user_profile': url_for('accounts.get_user',user_id = self.id),
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
################################# stories ###########################################################
    

class story_status:
    public: 0
    private:2
    deleted:1

class Story(db.Model):
    
    # user Model for storing user story related details 
    
    __tablename__ = 'story'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.VARCHAR(2000))
    story_category = db.Column(db.VARCHAR(200))
    story_image_url = db.Column(db.VARCHAR(200))
    status = db.Column(db.VARCHAR(200))
    timestamp = db.Column(db.VARCHAR(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
   
    

    def to_json(self):
         
        if self.status == 0:
           self.status="public"
        if  self.status == 2:
           self.status="private"
        if  self.status == 1:
           self.tatus="deleted"
        user_data = Users.query.filter_by(id = self.author_id).first()
        json_story = {
            'author_image_url':user_data.image_url,
            'story_id':self.id,
            'author_id': self.author_id,
            'body': self.body,
            'timestamp': self.timestamp,
            'author_url': url_for('accounts.get_user', id=self.author_id),
            'story_url': url_for('story.get_story', id=self.id),
            'story_image_url': self.story_image_url,
            'status': self.status
        }

        return json_story

  

################################# Posts ###########################################################



    


class Posts(db.Model):
    """
     post  Model for storing post related details 
       
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.VARCHAR(2000))
    post_category = db.Column(db.VARCHAR(200))
    post_image_url = db.Column(db.VARCHAR(200))
    status = db.Column(db.VARCHAR(200), default=0)
    timestamp =  db.Column(db.VARCHAR(200))
    author_id = db.Column(db.VARCHAR(200), db.ForeignKey('users.id'))
    comments = db.relationship('Comments', backref='post', lazy='dynamic')
    likes = db.relationship('Likes', backref='like', lazy='dynamic')
    
 

   


    def to_json(self):

        if self.status == 0:
            self.status = 'public'
        elif self.status == 1:
            self.status = 'deleted'
        elif self.status ==2:
            self.status = 'private'
        

        posts_url = url_for('posts.get_post', post_id=self.id),
        author_url = url_for('accounts.get_user' , id= self.author_id)
        share_count = Share.query.filter_by(post_id = self.id).count()

        if self.status !=1 and self.status!=2:
            json_post = {
                'post_id': self.id,
                'posts_url':url_for('posts.get_post', post_id=self.id),
                'body': self.body,
                'timestamp': self.timestamp,
                'category': self.post_category,
                'comment_count': self.comments.count(),
                'like_count': self.likes.count(),
                'author_url' : author_url,
                'post_image_url': self.post_image_url,
                'status': self.status,
                'author_id': self.author_id,
                'post_shares' : share_count,
                'status':200
                }
            return json_post 
            
        if self.status == 1:
            json_post = {
            "status": 201,
            "error": "This is a private post. "
            }
            return jsonify(json_post)

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
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
   
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))    
    job_body = db.Column(db.VARCHAR(300))
   
    def to_json(self):
        comm = Users.query.filter_by(id = self.author_id).first()
        commenter = comm.username
        post_data = Posts.query.filter_by(id =self.post_id).first()
        user_data = Users.query.filter_by(id = self.author_id).first()
        if self.status == 0:
                json_comment = {
                    'post_url': url_for('posts.get_post', post_id=self.post_id),
                    'comment_body': self.body,
                    'timestamp': self.timestamp,
                    'author_url': url_for('accounts.get_user', id=self.author_id),
                    'comment_id': self.id,
                    'comment_url': url_for('posts.get_comment', comment_id=self.id),
                    'post_author_id': post_data.author_id,
                    'commenter': commenter,
                    'user_id':self.author_id,
                    'post_id':self.post_id,
                    'comment_author_image': user_data.image_url,
                    'status':200
                 }
            
                return json_comment


    def job_json(self):
        comm = Users.query.filter_by(id = self.author_id).first()
        commen = comm.username

        job_j ={
                          "status":200,
                          "job_url":url_for('jobs.get_job', job_id=self.job_id),
                          "comment_body":self.body,
                          "job_id":self.job_id,
                          "author_id" :self.author_id,
                          "comment_id" : self.id,
                          "timestamp": self.timestamp,
                          "user_id": self.author_id,
                          "author_url": url_for('accounts.get_user', id=self.author_id),
                          'user_id':self.author_id,
                          'author_image': comm.image_url,
                          'job_comment_url': url_for('jobs.single_job_comment', comment_id=self.id)
                          }
        return job_j


        if self.status ==1:
            return jsonify("this comment doesn't exist")

  

################################# likes ###########################################################



class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    liker = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    

    def to_json(self):
        user_data = Users.query.filter_by(id = self.liker).first()
        json_like = {
            'post_id':self.post_id,
            'user_id': self.liker,
            'user_image_url': user_data.image_url,
            'like_id': self.id,
            'post_url': url_for('posts.get_post', post_id=self.post_id),
            'user_url': url_for('accounts.get_user', id=self.liker),
            'status':200
        }
        return json_like


class flags_(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.VARCHAR(100), db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    
   
    def to_json(self):
        json_flag = {
            'post_id': self.post_id,
            'user_id' : self.user,
            'flag_id': self.id,
            'post_url': url_for('posts.get_post', post_id=self.post_id),
            'user_url': url_for('accounts.get_user', user_id=self.user),
            'status':200
        }
        return json_flag

#################################### jobs ###################################################
class job_status:
    Active: 0
    deleted: 1
    bid_closed: 2

class Jobs(db.Model):
    """
     job Model for storing job related details 
        
    """
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.VARCHAR(200))
    job_body = db.Column(db.VARCHAR(200))
    job_post_category = db.Column(db.VARCHAR(200))
    job_image_url = db.Column(db.VARCHAR(200))
    bid_winner = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    timestamp =db.Column(db.VARCHAR(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    share = db.Column(db.Integer, db.ForeignKey('share.id'))
    bids = db.Column(db.Integer, db.ForeignKey('job_bid.id'))
    def to_json(self):
        if self.status ==0:
           self.status='active'
        if self.status ==2:
           self.status ="hidden"
        if job_bid.query.filter_by(job_id = self.id).first() is None:
            self.bids = 0
        if self.bid_winner is None:
            self.bid_winner = 0


        json_job_post = {
            'job_id': self.id,
            'job_url': url_for('jobs.get_job', job_id=self.id),
            'job_title': self.job_title,
            'job_body': self.job_body,
            'author_id': self.author_id,
            'timestamp': self.timestamp,
            'bids': self.bids,
            'job_image_url' : self.job_image_url,
            'author_url': url_for('accounts.get_user', user_id=self.author_id),
            'bid_winner' : self.bid_winner,
            'state':self.status,
            'status':200
        }
        return json_job_post




################################# job_bids ###########################################################


class job_bid(db.Model):
    """
     job bid  Model for storing job related details 
        
    """
    __tablename__ = 'job_bid'
    id = db.Column(db.Integer, primary_key=True)
    bid_body = db.Column(db.VARCHAR(200))
    bid_ammount= db.Column(db.VARCHAR(100))
    timestamp = db.Column(db.VARCHAR(200))
    status = db.Column(db.Integer, default=0)
    author_id = db.Column(db.VARCHAR(200), db.ForeignKey('users.id'))
    job_id = db.Column(db.VARCHAR(200), db.ForeignKey('jobs.id'))



    def to_json(self):
        jobs_ = Jobs.query.filter_by(id=self.job_id).first()
        json_bid = {
            'job_url': url_for('jobs.get_job', job_id=self.job_id),
            'job_data': jobs_.job_body,
            'bid_url': url_for('jobs.get_bid', bid_id=self.id),
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
        posts = Posts.query.filter_by(post_category=self.interest_).count()
        jobs = Jobs.query.filter_by(job_post_category=self.interest_).count()
        json_interests = {
            'interest_id':self.id,
            'interest':self.interest_,
            'posts': posts,
            'jobs': jobs,
            'status':200

        }
        return json_interests


################################# shares ###########################################################

class Share(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    status = db.Column(db.Integer)

   
   
    def post_json(self):
         
         if self.post_id is not None:
            shared_post =Posts.query.filter_by(id = self.post_id).first()
            json_share = {
                'share_id':self.id,
                'post_url': url_for('posts.get_post',post_id=self.post_id),
                'user_url': url_for('accounts.get_user', user_id=self.user),
                'user_id' :self.user,
                'shared_post' :shared_post.body, 
                'post_image_url': shared_post.post_image_url,
                'post_id' : self.post_id, 
                'status': 200
            }
            return json_share
            
    def job_json(self):
        if self.job_id  is  not None:
            shared_job =Jobs.query.filter_by(id = self.job_id).first()
            json_share = {
                'share_id':self.id,
                'job_url': url_for('jobs.get_job',job_id=self.job_id),
                'user_url': url_for('accounts.get_user', user_id=self.user),
                'user_id':self.user,
                'shared_job': shared_job.job_body,
                'job_image_url': shared_job.job_image_url,
                'job_id':self.job_id,
                'status': 200
            }
            return json_share


def initialize():
    db.connect()
    db.create_tables([Notification,Follows,Users,Story,Posts,Comments,Likes,flags_,Jobs,Job_bid,Interests,Share], safe=True)
    db.close()




