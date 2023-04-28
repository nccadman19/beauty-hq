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
    lashes = db.relationship(
        "Lash",
        backref="client",
        cascade="all, delete",
        lazy=True
    )
    brows = db.relationship(
        "Brow",
        backref="client",
        cascade="all, delete",
        lazy=True
    )

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.name


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


class Treatment(db.Model):
    TREATMENT_TYPES = [
        ('L', 'Lashes'),
        ('B', 'Brows'),
        ('BL', 'Both'),
    ]

    class Lash(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        client_id = db.Column(
            db.Integer,
            db.ForeignKey('client.id'),
            nullable=False
            )
        type = db.Column(db.String(2), nullable=False)
        lash_type = db.Column(db.String(2), nullable=True)
        notes = db.Column(db.Text, nullable=True)

        def __repr__(self):
            return f"<Lash {self.id}>"

    class Brow(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        client_id = db.Column(
            db.Integer,
            db.ForeignKey('client.id'),
            nullable=False
            )
        type = db.Column(db.String(2), nullable=False)
        brow_type = db.Column(db.String(2), nullable=True)
        notes = db.Column(db.Text, nullable=True)

        def __repr__(self):
            return f"<Brow {self.id}>"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(2), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    lash_id = db.Column(db.Integer, db.ForeignKey('lash.id'), nullable=True)
    lash = db.relationship("Lash", backref="treatment", uselist=False)
    brow_id = db.Column(db.Integer, db.ForeignKey('brow.id'), nullable=True)
    brow = db.relationship("Brow", backref="treatment", uselist=False)

    def __repr__(self):
        return f"<Treatment {self.id}>"
