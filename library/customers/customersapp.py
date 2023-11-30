import logging
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date
from os import environ

# Configurazione del logging
logging.basicConfig(filename='app.log', level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    surname = db.Column(db.String(80), unique=True, nullable=False)
    birthdate = db.Column(Date, nullable=False)                         # date(1990, 1, 1)  "1987-06-01"
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'surname': self.surname, 'birthdate': self.birthdate, 'email': self.email}

db.create_all()

# create a test route
@app.route('/test', methods=['GET'])
def test():
    app.logger.info('Test route accessed')
    return make_response(jsonify({'message': 'test route'}), 200)


# create a user
@app.route('/customers', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = Customer(name=data['name'], surname=data['surname'], birthdate=data['birthdate'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        app.logger.info('User created: %s', new_user.id)
        return make_response(jsonify({'message': 'user created'}), 201)
    except Exception as e:
        app.logger.error('Error creating user: %s', str(e))
        return make_response(jsonify({'message': 'error creating user'}), 500)


# get all users
@app.route('/customers', methods=['GET'])
def get_users():
    try:
        users = Customer.query.all()
        app.logger.info('Retrieved all users')
        return make_response(jsonify([user.json() for user in users]), 200)
    except Exception as e:
        app.logger.error('Error getting users: %s', str(e))
        return make_response(jsonify({'message': 'error getting users'}), 500)


# get a user by id
@app.route('/customers/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = Customer.query.filter_by(id=id).first()
        if user:
            app.logger.info('Retrieved user by id: %s', user.id)
            return make_response(jsonify({'user': user.json()}), 200)
        app.logger.warning('User not found by id: %s', id)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        app.logger.error('Error getting user by id: %s', str(e))
        return make_response(jsonify({'message': 'error getting user'}), 500)
    

# update a user
@app.route('/customers/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = Customer.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.surname = data['surname']
            user.birthdate = data['birthdate']
            user.email = data['email']
            db.session.commit()
            app.logger.info('User updated: %s', user.id)
            return make_response(jsonify({'message': 'user updated'}), 200)
        app.logger.warning('User not found for update by id: %s', id)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        app.logger.error('Error updating user: %s', str(e))
        return make_response(jsonify({'message': 'error updating user'}), 500)
    

# delete a user
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = Customer.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except Exception as e:
    print(str(e))
    return make_response(jsonify({'message': 'error deleting user'}), 500)
  

# delete a user
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = Customer.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            app.logger.info('User deleted: %s', user.id)
            return make_response(jsonify({'message': 'user deleted'}), 200)
        app.logger.warning('User not found for delete by id: %s', id)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        app.logger.error('Error deleting user: %s', str(e))
        return make_response(jsonify({'message': 'error deleting user'}), 500)
