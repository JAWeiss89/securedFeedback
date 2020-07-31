from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """ User Model """
    __tablename__= "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    username = db.Column(db.String(20),
                         nullable=False,
                         unique=True)

    password = db.Column(db.Text,
                         nullable=False)

    email = db.Column(db.String(50),
                         nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                           nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """ Formats user data and hashes sensitive info so that it's suitable to store in database. Returns user"""
       
        hashed = bcrypt.generate_password_hash(password)

        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        
        # returns user instance of user with hashed password
        return cls(username=username, password=hashed_utf8, email= email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """ Validates that user exists in db & password is correct. Returns user instance if authenticated or False if not"""

        found_user = User.query.filter_by(username=username).first()

        if found_user and bcrypt.check_password_hash(found_user.password, password):
            return found_user
        else :
            return False



class Feedback(db.Model):
    """ Feedback Model """
    __tablename__= "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    title = db.Column(db.String(100),
                      nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)

    username = db.Column(db.Text,
                         db.ForeignKey('users.username'))
    
    user = db.relationship('User', backref='feedback')



