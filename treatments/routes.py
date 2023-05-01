from flask import render_template, request, flash, redirect, url_for, session
from treatments import app, db
from treatments.models import Client, Treatment, User
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    db.create_all()


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
            return redirect(url_for('get_clients'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    # Clear Flask message flashing system
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('home'))


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
@app.route('/new_treatment', methods=['GET', 'POST'])
def new_treatment():
    if request.method == 'POST':
        treatment_type = request.form['type']
        notes = request.form['notes']
        if treatment_type == 'lashes':
            lash_type = request.form['lash_type']
            # create a new LashTreatment object with the given lash and notes
        elif treatment_type == 'brows':
            brow_type = request.form['brow_type']
            # create a new BrowTreatment object with the given brow and notes
        elif treatment_type == 'both':
            lash_type = request.form['lash_type']
            brow_type = request.form['brow_type']
            # create a new LashBrowTreatment object with the given lash brow
        # and notes. redirect to a page confirming the treatment was added
        return redirect(url_for('get_clients'))
    else:
        return render_template('new_treatment.html')


# template for getting all treatments
@app.route('/treatments', methods=['GET'])
@login_required
def get_treatments():
    treatments = Treatment.query.all()
    return render_template('clients.html', treatments=treatments)
