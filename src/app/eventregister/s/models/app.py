from . import *

class App(Base):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    secret_key = db.Column(db.String(255), unique=True, nullable=False)
    addresses = db.relationship('Event_Type', backref='app')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.secret_key = hashlib.sha1(os.urandom(64)).hexdigest()
