from flask import render_template, request
from treatments import app, db
from treatments.models import Client, Treatment, Lash, Brow, Type


# homepage
@app.route('/')
def home():
    return render_template('index.html')


# template for creating a new client
@app.route('/clients/new', methods=['GET'])
def new_client():
    return render_template('add_client.html')


# API endpoint for creating a new client
@app.route('/clients', methods=['POST'])
def create_client():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    client = Client(name=name, email=email, phone=phone)
    db.session.add(client)
    db.session.commit()
    return render_template(
        'client_created.html',
        message='Client created successfully.'
    ), 201


# template for getting all clients
@app.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)


# template for creating a new treatment
@app.route('/treatments/new', methods=['GET'])
def new_treatment():
    return render_template('new_treatment.html')


# endpoint for creating a new treatment
@app.route('/treatments', methods=['POST'])
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
        'treatment_created.html',
        message='Treatment created successfully.'
    ), 201


# template for getting all treatments
@app.route('/treatments', methods=['GET'])
def get_treatments():
    treatments = Treatment.query.all()
    return render_template('treatments.html', treatments=treatments)


# template for creating a new type
@app.route('/types/new', methods=['GET'])
def new_type():
    return render_template('new_type.html')


# endpoint for creating a new type
@app.route('/types', methods=['POST'])
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
def get_types():
    types = Type.query.all()
    return render_template('types.html', types=types)
