from flask import render_template, request, flash, redirect, url_for, session
from treatments import app, db
from treatments.models import Client, User
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
            return redirect(url_for('get_all_clients'))
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
        lash_type = request.form.get('lash_type')
        lash_notes = request.form.get('lash_notes')
        brow_type = request.form.get('brow_type')
        brow_notes = request.form.get('brow_notes')

        client = Client(name=name, email=email, phone=phone)
        client.lash_type = lash_type
        client.lash_notes = lash_notes
        client.brow_type = brow_type
        client.brow_notes = brow_notes

        db.session.add(client)
        db.session.commit()

        flash('Client created successfully.', 'success')

        return redirect(url_for('get_all_clients'))


# template for getting all clients
@app.route('/clients', methods=['GET'])
@login_required
def get_all_clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)


# template for getting a specific client
@app.route('/client/<int:client_id>')
@login_required
def get_client(client_id):
    client = Client.query.get(client_id)
    return render_template('client.html', client=client)
