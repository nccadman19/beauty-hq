from treatments import db
from flask import Flask
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


class Client(db.Model):
    # schema for the Client model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    lash_type = db.Column(db.String(20), nullable=True)
    lash_notes = db.Column(db.Text, nullable=True)
    brow_type = db.Column(db.String(20), nullable=True)
    brow_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.name

    @property
    def formatted_lash_type(self):
        if self.lash_type == 'classic':
            return 'Classic'
        elif self.lash_type == 'hybrid':
            return 'Hybrid'
        elif self.lash_type == 'russian':
            return 'Russian'
        else:
            return 'N/A'

    @property
    def formatted_brow_type(self):
        if self.brow_type == 'brow_tint':
            return 'Wax & Tint'
        elif self.brow_type == 'lamination':
            return 'Lamination'
        else:
            return 'N/A'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(50), nullable=False)
    last_name = db.Column(db.VARCHAR(50), nullable=False)
    email = db.Column(db.VARCHAR(120), unique=True, nullable=False)
    password = db.Column(db.VARCHAR(300), nullable=False)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(id):
        return User.query.get(int(id))
