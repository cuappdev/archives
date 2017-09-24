import bcrypt
from . import *

class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    apps = db.relationship('App', secondary=users_to_apps,
                           backref=db.backref('users'))

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = bcrypt.hashpw(kwargs.get('password'), bcrypt.gensalt())
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password, self.password)
        return self.password == pwhash

# define many-to-many relationship
users_to_apps = db.Table('user_to_apps',
                         db.Column('user_id',
                                   db.Integer,
                                   db.ForeignKey('user.id')),
                         db.Column('app_id',
                                   db.Integer,
                                   db.ForeignKey('app.id'))
                        )
