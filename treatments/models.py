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
    # schema for the Category model
    id = db.Column(db.Integer, primary_key=True)
    treatment_name = db.Column(db.String(25), unique=True, nullable=False)
    lash_type = db.Column(db.String(10), nullable=False)
    brows_type = db.Column(db.String(10), nullable=False)
    microblading_type = db.Column(db.String(10), nullable=False)
    types = db.relationship(
        "Type",
        backref="treatment",
        cascade="all, delete",
        lazy=True
    )

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.treatment_name


class Type(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    type_description = db.Column(db.Text, nullable=False)
    treatment_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "treatment.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Task: {1}".format(
            self.id, self.type_name
        )


class Lash(db.Model):
    # schema for the Lash model
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "type.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    client_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "client.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "Lash treatment ID: {0} for client ID: {1}".format(
            self.type_id, self.client_id
        )


class Brow(db.Model):
    # schema for the Brow model
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "type.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )
    client_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "client.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "Brow treatment ID: {0} for client ID: {1}".format(
            self.type_id, self.client_id
        )
