from flask import render_template, request, flash, redirect, url_for, session
from treatments import app, db
from treatments.models import Client, User
from flask_login import (
    login_user,
    logout_user,
    login_required,
    LoginManager,
    current_user
)
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


# about us
@app.route('/about')
def about():
    return render_template('about.html')


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


# logout the user
@app.route('/logout')
@login_required
def logout():
    # Clear Flask message flashing system
    session.pop('_flashes', None)
    logout_user()
    return redirect(url_for('home'))


# register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        # Check if user with the provided email already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            flash('An account with this email already exists.', 'error')
            return render_template('register.html')

        # Create the new user
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# creating a new client
@app.route('/clients/new', methods=['GET'])
def new_client():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        clients = user.clients
        return render_template('add_client.html', clients=clients)
    else:
        return redirect(url_for('register'))


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

        user = User.query.filter_by(id=current_user.id).first()

        # Check if a client with the same email already exists
        existing_client = Client.query.filter_by(
            email=email,
            user_id=current_user.id).first()
        if existing_client:
            toast_success = {
                'toast': 'A client with this email already exists!',
                'class': 'red'
            }
            clients = user.clients
            return render_template(
                'clients.html',
                clients=clients,
                toast_success=toast_success
            )

        client = Client(name=name, email=email, phone=phone)
        client.lash_type = lash_type
        client.lash_notes = lash_notes
        client.brow_type = brow_type
        client.brow_notes = brow_notes
        client.user = user

        db.session.add(client)
        db.session.commit()
        toast_success = {
            'toast': 'Client created successfully!',
            'class': 'green'
        }

        clients = user.clients
        return render_template(
            'clients.html',
            clients=clients,
            toast_success=toast_success
        )


# get all clients
@app.route('/clients', methods=['GET'])
def get_all_clients():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        clients = user.clients
        toast_success = request.args.get('toast_success')
        return render_template(
            'clients.html',
            clients=clients,
            toast_success=toast_success)
    else:
        return redirect(url_for('register'))


# get a specific client
@app.route('/client/<int:client_id>')
@login_required
def edit_client(client_id):
    client = Client.query.get(client_id)
    return render_template('edit_client.html', client=client)


# update client information if changed
@app.route('/client/<int:client_id>/update', methods=['POST'])
@login_required
def update_client(client_id):
    client = Client.query.get(client_id)
    if client:
        client.name = request.form['name']
        client.email = request.form['email']
        client.phone = request.form['phone']
        client.lash_type = request.form.get('lash_type')
        client.lash_notes = request.form.get('lash_notes')
        client.brow_type = request.form.get('brow_type')
        client.brow_notes = request.form.get('brow_notes')

        db.session.commit()
        toast_success = {
            'toast': 'Client updated successfully!',
            'class': 'green'
        }

        user = User.query.filter_by(id=current_user.id).first()
        clients = user.clients
        return render_template(
            'clients.html',
            clients=clients,
            toast_success=toast_success
        )


# deleting client from database
@app.route('/client/<int:client_id>/delete', methods=['POST'])
@login_required
def delete_client(client_id):
    client = Client.query.get(client_id)
    if client:
        db.session.delete(client)
        db.session.commit()
        toast_success = {
            'toast': 'Client deleted successfully!',
            'class': 'green'
        }
    else:
        toast_success = {'toast': 'Client not found', 'class': 'red'}
    # fetch the updated list of clients
    user = User.query.filter_by(id=current_user.id).first()
    clients = user.clients
    return render_template(
        'clients.html',
        clients=clients,
        toast_success=toast_success
    )
