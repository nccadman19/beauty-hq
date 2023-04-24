from flask import render_template, request, flash, redirect, url_for
from treatments import app, db
from treatments.models import Client, Treatment, Lash, Brow, Type, User
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# homepage
@app.route('/')
def home():
    return render_template('index.html')


# error handler
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# login template for beauticians
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get_by_email(email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return render_template('clients.html')
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')


# template for creating a new client
@app.route('/clients/new', methods=['GET'])
@login_required
def new_client():
    return render_template('add_client.html')


# API endpoint for creating a new client
@app.route('/clients', methods=['POST'])
@login_required
def create_client():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        client = Client(name=name, email=email, phone=phone)
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('get_clients'))
    else:
        clients = Client.query.all()
        return render_template('clients.html', clients=clients)


# template for getting all clients
@app.route('/clients', methods=['GET'])
@login_required
def get_clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)


# template for creating a new treatment
@app.route('/treatments/new', methods=['GET'])
@login_required
def new_treatment():
    return render_template('new_treatment.html')


# endpoint for creating a new treatment
@app.route('/treatments', methods=['POST'])
@login_required
def create_treatment():
    treatment_name = request.form.get('treatment_name')
    treatment = Treatment(treatment_name=treatment_name)
    db.session.add(treatment)
    db.session.commit()

    # create lash treatment
    lash_type = request.form.get('lash_type')
    if lash_type:
        lash = Lash(type_id=treatment.id, lash_type=lash_type)
        db.session.add(lash)

    # create brow treatment
    brow_type = request.form.get('brow_type')
    if brow_type:
        brow = Brow(type_id=treatment.id, brow_type=brow_type)
        db.session.add(brow)

    db.session.commit()

    return render_template(
        'clients.html',
        message='Treatment added successfully.'
    ), 201


# template for getting all treatments
@app.route('/treatments', methods=['GET'])
@login_required
def get_treatments():
    treatments = Treatment.query.all()
    return render_template('clients.html', treatments=treatments)


# template for creating a new type
@app.route('/types/new', methods=['GET'])
@login_required
def new_type():
    return render_template('clients.html')


# endpoint for creating a new type
@app.route('/types', methods=['POST'])
@login_required
def create_type():
    treatment_id = request.form.get('treatment_id')
    type_name = request.form.get('type_name')
    type = Type(treatment_id=treatment_id, type_name=type_name)
    db.session.add(type)
    db.session.commit()
    return render_template(
        'type_created.html',
        message='Type created successfully.'
    ), 201


# template for getting all types
@app.route('/types', methods=['GET'])
@login_required
def get_types():
    types = Type.query.all()
    return render_template('clients.html', types=types)
