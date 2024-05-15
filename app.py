from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGO_URI'])
db = client.security_agency

class ClientForm(FlaskForm):
    client_id = IntegerField('Client ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    contract_id = IntegerField('Contract ID', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = ClientForm()
    if form.validate_on_submit():
        client_id = form.client_id.data
        name = form.name.data
        contract_id = form.contract_id.data
        db.clients.insert_one({"_id": client_id, "name": name, "contract_id": contract_id})
        flash('Client added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_client.html', form=form)

@app.route('/update_client', methods=['GET', 'POST'])
def update_client():
    form = ClientForm()
    if form.validate_on_submit():
        client_id = form.client_id.data
        name = form.name.data
        db.clients.update_one({"_id": client_id}, {"$set": {"name": name}})
        flash('Client updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('update_client.html', form=form)

@app.route('/delete_client', methods=['GET', 'POST'])
def delete_client():
    form = ClientForm()
    if form.validate_on_submit():
        client_id = form.client_id.data
        db.clients.delete_one({"_id": client_id})
        flash('Client deleted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('delete_client.html', form=form)

@app.route('/view_clients')
def view_clients():
    clients = db.clients.find()
    return render_template('view_clients.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
