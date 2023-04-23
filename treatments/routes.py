from flask import render_template, request
from treatments import app, db
from treatments.models import Client, Treatment, Lash, Brow, Type
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash


# homepage
@app.route('/')
def home():
    return render_template('index.html')


# template for creating a new client
@app.route('/clients/new', methods=['GET'])
@login_required
def new_client():
    return render_template('add_client.html')


# API endpoint for creating a new client
@app.route('/clients', methods=['POST'])
@login_required
def create_client():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    client = Client(name=name, email=email, phone=phone)
    db.session.add(client)
    db.session.commit()
    return render_template(
        'clients.html',
        message='Client created successfully.'
    ), 201


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


# login template for beauticians
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
